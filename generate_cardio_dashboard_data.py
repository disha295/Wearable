# Full script: generate_cardio_dashboard_data.py logic for saving cardio metric exports

import pandas as pd
import os
from datetime import datetime, timedelta

def convert_and_export_cardio_data(cleaned_csv_dataframes, export_dir):
    """
    Converts Apple Health cardiovascular metrics from raw format into:
    - Timestamped time-series data
    - Z-score with rolling stats
    - Exported as CSVs per metric for visualization
    """
    def prepare_df(df, date_col='endDate'):
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df[date_col], unit='ns')
        df = df[['timestamp', 'value']].dropna().sort_values('timestamp')
        df['rolling_mean'] = df['value'].rolling(window=7, min_periods=1).mean()
        df['rolling_std'] = df['value'].rolling(window=7, min_periods=1).std()
        df['zscore'] = (df['value'] - df['rolling_mean']) / df['rolling_std']
        return df

    os.makedirs(export_dir, exist_ok=True)
    
    cardio_metrics = {
        'RestingHeartRate': 'restingheartrate_zscore.csv',
        'HeartRateVariabilitySDNN': 'hrv_sdnn_zscore.csv',
        'HeartRateRecoveryOneMinute': 'hr_recovery_zscore.csv',
        'VO2Max': 'vo2max_zscore.csv'
    }

    exported_files = []
    for key, filename in cardio_metrics.items():
        if key in cleaned_csv_dataframes:
            df = cleaned_csv_dataframes[key]
            df_clean = prepare_df(df)
            filepath = os.path.join(export_dir, filename)
            df_clean.to_csv(filepath, index=False)
            exported_files.append(filepath)

    return exported_files
