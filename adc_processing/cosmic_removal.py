import numpy as np

def remove_cosmic_events(df):
    """
    Removes cosmic events by checking adjacent channels' ADC activities.

    Args:
        df (pd.DataFrame): DataFrame containing 'Channel' and 'Thresholded_Adj_ADCs'.
    
    Returns:
        pd.DataFrame: Processed DataFrame with cosmic events removed.
    """
    df_processed2 = df.copy()
    df_processed = df.sort_values('Channel').reset_index(drop=True)
    channels = df_processed['Channel'].tolist()
    channel_to_index = {channel: idx for idx, channel in enumerate(channels)}
    
    for channel in channels[1:-1]:
        idx = channel_to_index[channel]
        prev_channel = channel - 1
        next_channel = channel + 1

        if prev_channel in channel_to_index and next_channel in channel_to_index:
            idx_prev = channel_to_index[prev_channel]
            idx_next = channel_to_index[next_channel]
            
            adc_current = np.array(df_processed.at[idx, 'Thresholded_Adj_ADCs'])
            adc_prev = np.array(df_processed.at[idx_prev, 'Thresholded_Adj_ADCs'])
            adc_next = np.array(df_processed.at[idx_next, 'Thresholded_Adj_ADCs'])
            for i in range(1,len(adc_current)-1):
                if (adc_current[i]>50 and adc_next[i]> 50 and adc_prev[i]>50) or adc_current[i]> 5000:
                    start_index = i
                    zero_count = 0
                    #while start_index > 0 and adc_current[start_index - 1] != 0:
                    while start_index > 0 and zero_count<100:
                        start_index -= 1
                        if adc_current[start_index]==0:
                            zero_count +=1
                    
                    end_index = i
                    end_zero = 0
                    # while end_index < len(adc_current) - 1 and adc_current[end_index + 1] != 0:
                    while end_index < len(adc_current) - 1 and end_zero <100:
                        end_index += 1
                        if adc_current[end_index]==0:
                            end_zero +=1
                    # if channel ==7655: print(start_index, end_index+1)
                    adc_current[start_index:end_index + 1] = 0
            
            df_processed2.at[idx, 'Thresholded_Adj_ADCs'] = adc_current.tolist()
    test1 = df_processed[df_processed['Channel']==7655]['Thresholded_Adj_ADCs'].values
    test2 = df_processed2[df_processed2['Channel']==7655]['Thresholded_Adj_ADCs'].values
    sum1 = np.count_nonzero(np.hstack(test1)) 
    sum2 = np.count_nonzero(np.hstack(test2))
    print(sum1, sum2)
    return df_processed2
