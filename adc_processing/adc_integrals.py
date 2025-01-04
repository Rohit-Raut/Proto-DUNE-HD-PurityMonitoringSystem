import numpy as np
import pandas as pd

def calculate_adc_integrals(df):
    """
    Calculates ADC integrals by summing the ADC values across adjacent channels.

    Args:
        df (pd.DataFrame): DataFrame containing 'Thresholded_Adj_ADCs' and 'Channel'.
    
    Returns:
        pd.DataFrame: DataFrame containing the calculated ADC integrals for each channel.
    """
    channel_to_adc = {row['Channel']: np.array(row['Thresholded_Adj_ADCs']) for _, row in df.iterrows()}
    adc_integral_list = []
    
    for channel in df['Channel']:
        adc_current = channel_to_adc.get(channel)
        adc_prev = channel_to_adc.get(channel - 1)
        adc_next = channel_to_adc.get(channel + 1)
        
        if adc_current is None or adc_prev is None or adc_next is None:
            continue
        adc_integral = np.zeros_like(adc_current)
        for i in range(len(adc_current)):
            if adc_current[i]>=adc_prev[i] and adc_current[i]>=adc_next[i]:
                adc_integral[i] = adc_current[i]+adc_prev[i]+adc_next[i]
            else:
                #print("Channel",channel, adc_current[i], adc_prev[i], adc_next[i])
                adc_integral[i]=0
        adc_integral_list.append({
            'Channel': channel,
            'ADC_Integral': adc_integral.tolist()
        })
    
    return pd.DataFrame(adc_integral_list)
