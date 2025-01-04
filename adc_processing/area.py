import numpy as np
import pandas as pd

def adc_area(df, raw_data, expansion_points=3):
    df_processed = df.copy()
    df_processed = df_processed.sort_values('Channel').reset_index(drop=True)
    channels = df_processed['Channel'].tolist()
    channel_to_index = {channel: idx for idx, channel in enumerate(channels)}
    channels_to_process = channels[1:-1]  
    result = []

    for channel in channels_to_process:
        idx = channel_to_index[channel]
        adc_current = np.array(df_processed.at[idx, 'ADC_Integral'])
        raw_adc = np.array(raw_data.at[idx, 'ADC_Integral'])
        start_index = 0
        while start_index < len(adc_current):
            while start_index < len(adc_current) and adc_current[start_index] == 0:
                start_index += 1
            if start_index >= len(adc_current):
                break
            end_index = start_index
            while end_index < len(adc_current) - 1 and adc_current[end_index + 1] != 0:
                end_index += 1

            # Expand the chunk by 'expansion_points' on both sides
            expanded_start = max(0, start_index - expansion_points)
            expanded_end = min(len(adc_current) - 1, end_index + expansion_points)
            expanded_chunk = adc_current[expanded_start:expanded_end + 1]
            for i in range(len(expanded_chunk)):
                idx_in_full = expanded_start + i
                if expanded_chunk[i] == 0:
                    expanded_chunk[i] = raw_adc[idx_in_full]
            amplitude = np.max(expanded_chunk)
            area = np.trapz(expanded_chunk, dx=1)
            result.append({
                'Channel': channel,
                'Start Index': start_index,
                'End Index': end_index,
                'Amplitude': amplitude,
                'Area': area
            })
            start_index = end_index + 1

    final_result = pd.DataFrame(result)
    if 7655 in channel_to_index:
        idx_7657 = channel_to_index[7657]
        adc_7657 = np.array(final_result.at[idx_7657, 'Thresholded_Adj_ADCs'])
        non_zero_count = np.sum(adc_7657 != 0)
        print(f"Channel 7657 has {non_zero_count} non-zero values.")
    # group_df = final_result.groupby('Channel').agg({
    #     'Start Index':list,
    #     'End Index': list,
    #     'Amplitude':list,
    #     'Area':list
    # }).reset_index()

    return final_result




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
            
            condition = (adc_current > 50) & (adc_prev > 50) & (adc_next > 50)
            index = np.where(condition)[0]
            if channel==7655:
                print(index, len(index))
            for i in index:
                start_index = i
                zero_count = 0
                if channel==7655:
                    print(adc_prev[i],adc_current[i],adc_next[i])
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
