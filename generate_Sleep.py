# generate_sleep_dashboard_data.py
import pandas as pd
import os
from datetime import datetime, timedelta

def convert_and_export_sleep_data(cleaned_csv_dataframes, export_dir):
    sleep_df = cleaned_csv_dataframes['SleepAnalysis'].copy()

    # ✅ 1. Filter valid sleep types (exclude InBed, Awake)
    valid_stages = [
        'HKCategoryValueSleepAnalysisAsleepUnspecified',
        'HKCategoryValueSleepAnalysisAsleepCore',
        'HKCategoryValueSleepAnalysisAsleepDeep',
        'HKCategoryValueSleepAnalysisAsleepREM'
    ]
    sleep_df = sleep_df[sleep_df['value'].isin(valid_stages)]

    # ✅ 2. Convert timestamps from nanoseconds to datetime
    sleep_df['start'] = pd.to_datetime(sleep_df['startDate'], unit='ns')
    sleep_df['end'] = pd.to_datetime(sleep_df['endDate'], unit='ns')

    # ✅ 3. Compute duration in minutes and day reference
    sleep_df['duration_minutes'] = (sleep_df['end'] - sleep_df['start']).dt.total_seconds() / 60
    sleep_df['date'] = sleep_df['end'].dt.date

    # ✅ 4. Aggregate sleep per night
    daily_sleep = sleep_df.groupby('date').agg({'duration_minutes': 'sum'}).reset_index()
    daily_sleep['timestamp'] = pd.to_datetime(daily_sleep['date'])
    daily_sleep = daily_sleep[['timestamp', 'duration_minutes']].rename(columns={'duration_minutes': 'value'})

    # ✅ 5. Compute rolling stats
    daily_sleep['rolling_mean'] = daily_sleep['value'].rolling(window=7, min_periods=1).mean()
    daily_sleep['rolling_std'] = daily_sleep['value'].rolling(window=7, min_periods=1).std()
    daily_sleep['zscore'] = (daily_sleep['value'] - daily_sleep['rolling_mean']) / daily_sleep['rolling_std']

    # ✅ 6. Export to CSV
    output_path = os.path.join(export_dir, 'sleep_analysis_zscore.csv')
    daily_sleep.to_csv(output_path, index=False)
    return output_path
