def convert_and_export_activity_data(cleaned_csv_dataframes, export_dir, workout_df):
    import pandas as pd
    import os

    activity_metrics = {
        'AppleExerciseTime': 'exercise_time_zscore.csv',
        'ActiveEnergyBurned': 'active_energy_zscore.csv',
        'DistanceWalkingRunning': 'walking_running_distance_zscore.csv',
    }

    exported = []

    for key, filename in activity_metrics.items():
        df = cleaned_csv_dataframes[key].copy()
        df['timestamp'] = pd.to_datetime(df['endDate'])
        df['value'] = df['value'].astype(float)
        df['date'] = df['timestamp'].dt.date

        if key == 'AppleExerciseTime':
            daily_df = df.groupby('date').size().reset_index(name='value')
        else:
            daily_df = df.groupby('date').agg({'value': 'sum'}).reset_index()

        daily_df['timestamp'] = pd.to_datetime(daily_df['date'])
        daily_df = daily_df[['timestamp', 'value']]
        daily_df['rolling_mean'] = daily_df['value'].rolling(window=7, min_periods=1).mean()
        daily_df['rolling_std'] = daily_df['value'].rolling(window=7, min_periods=1).std()
        daily_df['zscore'] = (daily_df['value'] - daily_df['rolling_mean']) / daily_df['rolling_std']

        out_path = os.path.join(export_dir, filename)
        daily_df.to_csv(out_path, index=False)
        exported.append(out_path)

    # ✅ Workout DF metrics
    workout_df['timestamp'] = pd.to_datetime(workout_df['timestamp'])
    workout_df['date'] = workout_df['timestamp'].dt.date

    workout_daily = workout_df.groupby('date').agg({
        'speed': 'mean',
        'acceleration': 'max',
        'distance': 'sum'
    }).reset_index()

    workout_daily['timestamp'] = pd.to_datetime(workout_daily['date'])

    for col in ['speed', 'acceleration', 'distance']:
        df_metric = workout_daily[['timestamp', col]].rename(columns={col: 'value'})
        df_metric['rolling_mean'] = df_metric['value'].rolling(window=7, min_periods=1).mean()
        df_metric['rolling_std'] = df_metric['value'].rolling(window=7, min_periods=1).std()
        df_metric['zscore'] = (df_metric['value'] - df_metric['rolling_mean']) / df_metric['rolling_std']

        fname = f'workout_{col}_zscore.csv'
        df_metric.to_csv(os.path.join(export_dir, fname), index=False)
        exported.append(fname)

    return exported
