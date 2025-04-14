import os
import numpy as np
import pandas as pd
import pytz
import neurokit2 as nk
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# --- ECG Parsing and Preprocessing ---

def load_and_parse_ecg_files(directory):
    local_tz = pytz.timezone('America/Chicago')
    ecg_records = []

    for file in os.listdir(directory):
        if not file.endswith(".csv"):
            continue

        with open(os.path.join(directory, file), 'r') as f:
            lines = f.readlines()

        patient = lines[0].split(',')[1].strip()
        recorded_date = pd.to_datetime(lines[2].split(',')[1].strip(), errors='coerce')
        classification = lines[3].split(',')[1].strip()
        ecg_data = [float(line.strip().replace(',', '.')) for line in lines[13:] if line.strip()]

        if recorded_date.tzinfo is None:
            recorded_date = recorded_date.tz_localize('UTC')
        recorded_date = recorded_date.astimezone(local_tz)

        ecg_records.append({
            'patient': patient,
            'recorded_date': recorded_date,
            'classification': classification,
            'ecg_data': ecg_data
        })

    return pd.DataFrame(ecg_records)

# --- Signal Filtering ---

def bandpass_filter(data, lowcut=0.5, highcut=50.0, fs=512, order=5):
    nyquist = 0.5 * fs
    b, a = butter(order, [lowcut / nyquist, highcut / nyquist], btype='band')
    return filtfilt(b, a, data)

def preprocess_signals(df, fs=512):
    df = df[df['classification'] != 'Poor Recording'].copy()
    df['filtered_ecg'] = df['ecg_data'].apply(lambda x: bandpass_filter(x, fs=fs))
    return df

# --- HRV Feature Extraction ---

def detect_r_peaks(filtered_ecg, threshold=0.5):
    peaks, _ = find_peaks(filtered_ecg, height=threshold)
    return peaks

def compute_rr_intervals(r_peaks, fs=512):
    if isinstance(r_peaks, (list, np.ndarray)) and len(r_peaks) > 1:
        return np.diff(r_peaks) * (1000 / fs)
    return np.array([])

def filter_rr_outliers(rr_intervals, min_rr=300, max_rr=2000):
    return rr_intervals[(rr_intervals >= min_rr) & (rr_intervals <= max_rr)]

def calculate_sdnn(rr_intervals):
    return np.std(rr_intervals) if len(rr_intervals) > 1 else np.nan

def calculate_rmssd(rr_intervals):
    rr_diff = np.diff(rr_intervals)
    return np.sqrt(np.mean(rr_diff ** 2)) if rr_diff.size > 0 else np.nan

def calculate_pnn50(rr_intervals):
    rr_diff = np.abs(np.diff(rr_intervals))
    return np.sum(rr_diff > 50) / len(rr_diff) * 100 if rr_diff.size > 0 else np.nan

def calculate_frequency_hrv(rr_intervals):
    if len(rr_intervals) > 1:
        fft_result = np.fft.fft(rr_intervals)
        fft_freq = np.fft.fftfreq(len(rr_intervals))
        power = np.abs(fft_result) ** 2
        lf = np.sum(power[(fft_freq > 0.04) & (fft_freq < 0.15)])
        hf = np.sum(power[(fft_freq > 0.15) & (fft_freq < 0.4)])
        return lf, hf
    return np.nan, np.nan

def extract_hrv_features(df, fs=512):
    df['r_peaks'] = df['filtered_ecg'].apply(detect_r_peaks)
    df['rr_intervals'] = df['r_peaks'].apply(lambda x: compute_rr_intervals(x, fs))
    df['rr_intervals_filtered'] = df['rr_intervals'].apply(filter_rr_outliers)
    df['sdnn'] = df['rr_intervals_filtered'].apply(calculate_sdnn)
    df['rmssd'] = df['rr_intervals_filtered'].apply(calculate_rmssd)
    df['pnn50'] = df['rr_intervals_filtered'].apply(calculate_pnn50)
    df[['lf_power', 'hf_power']] = df['rr_intervals_filtered'].apply(
        lambda x: pd.Series(calculate_frequency_hrv(x)))
    return df

# --- Optional: HRV Extraction with NeuroKit2 ---

def extract_hrv_neurokit(filtered_ecg, sampling_rate=512):
    try:
        if len(filtered_ecg) < 100:
            return pd.Series(dtype='object')

        # Normalize signal
        normalized_ecg = (filtered_ecg - np.mean(filtered_ecg)) / np.std(filtered_ecg)

        # Use explicit method for stability
        signals, info = nk.ecg_process(normalized_ecg, sampling_rate=sampling_rate, method='neurokit')

        if 'ECG_Cleaned' not in signals.columns or len(signals['ECG_Cleaned']) == 0:
            return pd.Series(dtype='object')

        hrv_metrics = nk.hrv_time(info['ECG_Rpeaks'], sampling_rate=sampling_rate, show=False)
        return pd.Series({
            **hrv_metrics.iloc[0].to_dict(),
            'nk_signals': signals.to_dict(orient='list')
        })
    except Exception as err:
        print(f"NeuroKit2 failed: {err}")
        return pd.Series(dtype='object')

        signals, info = nk.ecg_process(filtered_ecg, sampling_rate=sampling_rate)

        if 'ECG_Cleaned' not in signals.columns or len(signals['ECG_Cleaned']) == 0:
            return pd.Series(dtype='object')

        hrv_metrics = nk.hrv_time(info['ECG_Rpeaks'], sampling_rate=sampling_rate, show=False)
        return pd.Series({
            **hrv_metrics.iloc[0].to_dict(),
            'nk_signals': signals.to_dict(orient='list')
        })
    except Exception:
        return pd.Series(dtype='object')

def integrate_neurokit_hrv(df):
    def extract_and_separate(signal):
        result = extract_hrv_neurokit(signal)
        if isinstance(result, pd.Series):
            hrv_data = result.drop('nk_signals') if 'nk_signals' in result else result
            nk_signals = result.get('nk_signals', {})
            return pd.Series({**hrv_data.to_dict(), 'nk_signals': nk_signals})
        return pd.Series(dtype='object')

    hrv_features = df['filtered_ecg'].apply(extract_and_separate)
    return pd.concat([df.reset_index(drop=True), hrv_features.reset_index(drop=True)], axis=1)

# --- Visualization Utilities ---

def plot_custom_rpeaks(ecg_signal, r_peaks, title="Filtered ECG with R-peaks"):
    if len(ecg_signal) == 0 or len(r_peaks) == 0:
        print("No valid custom signal or R-peaks to plot.")
        return

    plt.figure(figsize=(12, 4))
    plt.plot(ecg_signal, label='Filtered ECG')
    plt.plot(r_peaks, [ecg_signal[i] for i in r_peaks], "ro", label='R-peaks')
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_ecg_with_rpeaks(signals_dict, sample_rate=512, title="ECG with R-peaks"):
    ecg_cleaned = signals_dict.get('ECG_Cleaned', [])
    rpeaks_mask = np.array(signals_dict.get('ECG_Rpeaks', []))

    if not ecg_cleaned or not rpeaks_mask.any():
        print("Invalid signals for plotting.")
        return

    plt.figure(figsize=(12, 4))
    plt.plot(ecg_cleaned, label='ECG Cleaned')
    plt.plot(rpeaks_mask, [ecg_cleaned[i] for i in rpeaks_mask], "ro", label='R-peaks')
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_hrv_trend(df, metric='HRV_RMSSD'):
    if metric in df.columns:
        plt.figure(figsize=(10, 4))
        plt.plot(df['recorded_date'], df[metric], marker='o')
        plt.title(f"Trend of {metric} over time")
        plt.xlabel("Date")
        plt.ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"Metric '{metric}' not found in DataFrame.")

# --- HRV Anomaly Detection ---

def detect_hrv_anomalies(df, baseline_label='Sinus Rhythm'):
    baseline_df = df[df['classification'] == baseline_label]
    if len(baseline_df) >= 5:
        rmssd_thresh = baseline_df['rmssd'].mean() + 2 * baseline_df['rmssd'].std()
        pnn50_thresh = baseline_df['pnn50'].mean() + 2 * baseline_df['pnn50'].std()
        sdnn_thresh  = baseline_df['sdnn'].mean()  + 2 * baseline_df['sdnn'].std()
    else:
        rmssd_thresh, pnn50_thresh, sdnn_thresh = 150, 70, 100

    def classify_alert(row):
        if row['rmssd'] > rmssd_thresh or row['pnn50'] > pnn50_thresh or row['sdnn'] > sdnn_thresh:
            return 'HRV Alert'
        return 'Stable'

    df['hrv_alert'] = df.apply(classify_alert, axis=1)
    return df

# --- Pipeline Runner ---

def build_ecg_pipeline(directory):
    df = load_and_parse_ecg_files(directory)
    df = preprocess_signals(df)
    df = extract_hrv_features(df)
    df = integrate_neurokit_hrv(df)  # Add NeuroKit2 HRV metrics
    df = detect_hrv_anomalies(df)
    return df

# Example usage
if __name__ == '__main__':
    ecg_folder = './apple_health_export/electrocardiograms'
    ecg_df = build_ecg_pipeline(ecg_folder)
    ecg_df.to_csv('cleaned_ecg_features.csv', index=False)
    print("ECG data processing complete. Cleaned data saved to 'cleaned_ecg_features.csv'.")
    print(ecg_df.head())

    # Example visualization usage (optional):
    if 'nk_signals' in ecg_df.columns and isinstance(ecg_df.iloc[0]['nk_signals'], dict) and len(ecg_df.iloc[0]['nk_signals']) > 0:
        example_signals = ecg_df.iloc[0]['nk_signals']
        plot_ecg_with_rpeaks(example_signals)
    else:
        print("No valid nk_signals found, using custom signal for plotting.")
        plot_custom_rpeaks(ecg_df.iloc[0]['filtered_ecg'], ecg_df.iloc[0]['r_peaks'])

    plot_hrv_trend(ecg_df, metric='rmssd')
