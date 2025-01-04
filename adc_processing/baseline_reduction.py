import pandas as pd

def process_channel(df, channel, window_size=100):
    """
    Processes a single channel from the DataFrame to perform baseline reduction.

    Args:
        df (pd.DataFrame): DataFrame containing 'Channel' and 'ADC Values'.
        channel (int): The specific channel to process.
        window_size (int): Window size for rolling median baseline. Default is 100.
    
    Returns:
        pd.DataFrame: DataFrame with adjusted ADC values and baseline for the channel.
        int: Count of values below a specific threshold.
    """

    adc_values_series = df[df['Channel'] == channel]['ADC Values']
    if adc_values_series.empty:
        print(f"Channel {channel} not found in DataFrame.")
        return None 
    
    adc_values = adc_values_series.iloc[0]
    adc_series = pd.Series(adc_values)
    rolling_median_baseline = adc_series.rolling(window=window_size, min_periods=1).median()
    adjusted_adc = adc_series - rolling_median_baseline
    count = (adjusted_adc < 20).sum()
    
    return pd.DataFrame({
        'Channel': [channel],
        'Baseline': [rolling_median_baseline.tolist()],
        'Adj_ADCs': [adjusted_adc.tolist()],
        'Timestamps': [df[df['Channel'] == channel]['Timestamps'].iloc[0]]
    }), count
