from hdf5libs import HDF5RawDataFile
import daqdataformats 
import detchannelmaps
from fddetdataformats import WIBEthFrame
from rawdatautils.unpack.wibeth import np_array_adc, np_array_timestamp
import numpy as np
import pandas as pd
import struct

#FILE = "np04hd_raw_run028526_0000_dataflow5_datawriter_0_20240801T063811.hdf5"
FILE= "np04hd_raw_run028526_0000_dataflow6_datawriter_0_20240801T063811.hdf5"
def save_to_binary(output_file: str, df: pd.DataFrame) -> None:
    with open(output_file, "wb") as f:
        for _, row in df.iterrows():
            channel = row['Channel']
            adc_values = row['ADC Values']
            timestamps = row['Timestamps']
            
            # Write the channel number as an unsigned integer (4 bytes)
            f.write(struct.pack('I', channel))
            
            # Write the length of the ADC values array as an unsigned integer (4 bytes)
            f.write(struct.pack('I', len(adc_values)))
            
            # Write each ADC value as an unsigned short (2 bytes) and corresponding timestamp as unsigned long (8 bytes)
            for adc, timestamp in zip(adc_values, timestamps):
                f.write(struct.pack('H', adc))  # ADC value
                f.write(struct.pack('Q', timestamp))  # Timestamp
    
    print(f"Binary data written to {output_file}")
    
def main() -> None:
    h5_file = HDF5RawDataFile(FILE)
    chmap = detchannelmaps.make_map("PD2HDChannelMap")
    fragment_dataset_paths = h5_file.get_all_fragment_dataset_paths()
    chan_dict = {}
    trig = []
    test = []

    for path in fragment_dataset_paths:
        if not path.endswith("WIBEth"): continue
        # Load the WIBEth fragment
        frag = h5_file.get_frag(path)
        wib_frame = WIBEthFrame(frag.get_data())
        daq_header = wib_frame.get_daqheader()
        crate, slot, stream = daq_header.crate_id, daq_header.slot_id, daq_header.stream_id
        if crate != 2: continue
        offline_channels = [
            chmap.get_offline_channel_from_crate_slot_stream_chan(crate, slot, stream, chan)
            for chan in range(64)
        ]
        #begin = frag.get_window_begin()
        #end = frag.get_window_end()
        #trig.append([frag.get_window_begin(), frag.get_window_end()])
        #trigger_window = end-begin
        #test.append(trigger_window)
        adcs_check = np_array_adc(frag).shape[0]
        test.append(adcs_check)
        adcs = np_array_adc(frag)
        timestamps = np_array_timestamp(frag)
        #frag.get_window_begin())
        #end_1.append(frag.get_window_end())
        j = 0
        for i in range(64):
            j +=1
            channel = offline_channels[i]
            #IF YOU WANT TO PROCESS JUST 7600 TO 7680 HERE IS THE COURSE
            if channel<7600 or channel>7680:
                continue
            begin = frag.get_window_begin()
            end = frag.get_window_end()
            trig.append([frag.get_window_begin(), frag.get_window_end()])
            adc_value_array = adcs[:, i].tolist()  # Extract all ADC values for the ith channel
            timestamp_array = timestamps.tolist()  # Extract all corresponding timestamps
            
            if channel not in chan_dict:
                chan_dict[channel] = {'adcs': [], 'timestamps': []}
            
            # Add ADC values and corresponding timestamps to the channel
            chan_dict[channel]['adcs'].extend(adc_value_array)
            chan_dict[channel]['timestamps'].extend(timestamp_array)
            
            # Print statement to observe the population process
            #print(f"Channel {channel}: Added {len(adc_value_array)} ADC values and {len(timestamp_array)} timestamps.")

    # Prepare the data for DataFrame
    print(len(test))
    print(j)
    data = []
    for channel, data_dict in chan_dict.items():
        #if 7645<=channel<=7665:
        adc_values = data_dict['adcs']
        timestamps = data_dict['timestamps']
        data.append([channel, adc_values, timestamps])
    
    df = pd.DataFrame(data, columns=['Channel', 'ADC Values', 'Timestamps'])

    # Printing DataFrame preview to see the final structure
    #print("DataFrame preview:")
    #print(df.head())

    save_to_binary("dataflow5_T063811_7600-7680.npy", df)
    print("Complete!")

if __name__ == "__main__":
    main()





