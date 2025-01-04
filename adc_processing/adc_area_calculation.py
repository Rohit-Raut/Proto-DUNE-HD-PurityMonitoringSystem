import numpy as np
import pandas as pd
def adc_expansion(df, raw_data, expansion_points = 3):
    df_processed = df.copy()
    df_processed = df_processed.sort_values('Channel').reset_index(drop=True)
    channels = df_processed['Channel'].tolist()
    channel_to_index = {channel: idx for idx, channel in enumerate(channels)}
    channels_to_process = channels[1:-1]  # Ignore first and last channel
    result = []
    raw_data = raw_data.sort_values('Channel').reset_index(drop=True)
    for channel in channels_to_process:
        idx = channel_to_index[channel]
        adc_current = np.array(df_processed.at[idx,'ADC_Integral'])
        raw_data_arr = np.array(raw_data.at[idx,'ADC_Integral'])
        start_index = 0
        while start_index < len(adc_current):
            while start_index < len(adc_current) and adc_current[start_index] == 0:
                start_index += 1
            if start_index >= len(adc_current):
                break  
            end_index = start_index
            while end_index < len(adc_current) - 1 and adc_current[end_index + 1] != 0:
                end_index += 1
            expanded_start = max(0,start_index-expansion_points)
            expanded_end = min(len(adc_current)-1, end_index+expansion_points)
            for idx_in_full in range(expanded_start, expanded_end+1):
                if adc_current[idx_in_full]==0:
                    adc_current[idx_in_full]=raw_data_arr[idx_in_full]
            start_index = end_index + 1
        df_processed.at[idx,'ADC_Integral'] = adc_current
    return df_processed


def adc_area(adc_integral, raw_int):
    df=  adc_expansion(adc_integral, raw_int)
    area_results = []
    df_processed = df.copy()
    channels = df_processed['Channel'].tolist()
    channel_to_index = {channel: idx for idx, channel in enumerate(channels)}
    channels_to_process = channels  # Process all channels

    for channel in channels_to_process:
        idx = channel_to_index[channel]
        adc_current = np.array(df_processed.at[idx, 'ADC_Integral'])

        start_index = 0
        while start_index < len(adc_current):
            zero_count = 0
            while start_index < len(adc_current) and adc_current[start_index] == 0:
                start_index += 1
            if start_index >= len(adc_current):
                break
            end_index = start_index
            end_count =0
            #while end_index < len(adc_current) - 1 and adc_current[end_index + 1] != 0:
            while end_index < len(adc_current) - 1 and end_count<6:
                end_index += 1
                if adc_current[end_index] ==0:
                    end_count +=1
            chunk = adc_current[start_index:end_index + 1]
            #rea = chunk[0] if len(chunk) == 1 else np.sum(chunk)
            peak = np.max(chunk)
            mean = np.mean(chunk)
            std = np.std(chunk)
            filtered_chunk = chunk[(chunk>=peak-2*std)&(chunk<=peak+2*std)]
            area = np.sum(filtered_chunk)
            # if channel ==7655:
            #     print(f"chunk: {chunk}, filtered_chunk: {filtered_chunk} mean: {mean}, area: {area}, std: {std}")
            #area = np.sum(chunk)
            if area<50 or area >5000:
                start_index=end_index+1
                #print(f"Area Is less than 1:{channel}, {area}")
                continue
            area_results.append({'Channel': channel, 'Area': area})
            start_index = end_index + 1
    area_results_df = pd.DataFrame(area_results)
    x = (area_results_df['Channel'] == 7655).sum()
    print(f"Debugging Total Signal: {x}")
    return area_results_df