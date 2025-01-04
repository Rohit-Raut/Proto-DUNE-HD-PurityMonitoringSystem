import struct
import pandas as pd

def read_binary_file(file_path):
    """
    Reads binary .npy data file and returns a DataFrame with channel, ADC values, and timestamps.

    Args:
        file_path (str): Path to the binary file.
    
    Returns:
        pd.DataFrame: DataFrame containing 'Channel', 'ADC Values', and 'Timestamps'.
    """
    data = []
    
    with open(file_path, "rb") as f:
        while True:
            channel_data = f.read(4)
            if not channel_data:
                break
            channel = struct.unpack('I', channel_data)[0]
            num_adcs = struct.unpack('I', f.read(4))[0]
            
            adc_values = []
            timestamps = []
            
            for _ in range(num_adcs):
                adc_value = struct.unpack('H', f.read(2))[0]
                timestamp = struct.unpack('Q', f.read(8))[0]
                adc_values.append(adc_value)
                timestamps.append(timestamp)
            data.append([channel, adc_values, timestamps])
    
    return pd.DataFrame(data, columns=['Channel', 'ADC Values', 'Timestamps'])
