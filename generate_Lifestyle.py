import pandas as pd
import os
from datetime import datetime, timedelta

def convert_and_export_lifestyle_data(cleaned_csv_dataframes, export_dir):
    lifestyle_metrics = {
        'TimeInDaylight': 'time_in_daylight_zscore.csv',
        'HeadphoneAudioExposure': 'headphone_audio_zscore.csv',
        'EnvironmentalAudioExposure': 'env_audio_exposure_zscore.csv',
    }

    exported = []

    for key, filename in lifestyle_metrics.items():
        df = cleaned_csv_dataframes[key].copy()

        # ✅ Parse timestamp and aggregate daily total
        df['timestamp'] = pd.to_datetime(df['endDate'])
        df['date'] = df['timestamp'].dt.date
        df['value'] = df['value'].astype(float)

        daily_df = df.groupby('date').agg({'value': 'sum'}).reset_index()
        daily_df['timestamp'] = pd.to_datetime(daily_df['date'])
        daily_df = daily_df[['timestamp', 'value']]

        # ✅ Compute rolling window stats and z-score
        daily_df['rolling_mean'] = daily_df['value'].rolling(window=7, min_periods=1).mean()
        daily_df['rolling_std'] = daily_df['value'].rolling(window=7, min_periods=1).std()
        daily_df['zscore'] = (daily_df['value'] - daily_df['rolling_mean']) / daily_df['rolling_std']

        # ✅ Save to export directory
        out_path = os.path.join(export_dir, filename)
        daily_df.to_csv(out_path, index=False)
        exported.append(out_path)

    return exported
