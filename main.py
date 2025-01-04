import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from adc_processing.data_reader import read_binary_file
from adc_processing.baseline_reduction import process_channel
from adc_processing.thresholding import threshold_adj_adcs
from adc_processing.cosmic_removal import remove_cosmic_events
from adc_processing.adc_integrals import calculate_adc_integrals
from adc_processing.adc_area_calculation import adc_area
from adc_processing.plot import plot
from adc_processing.plot import plot_adc
from adc_processing.plot import track_reconstruction

def main(input_file, start_channel, end_channel, output_file):
    print(f"Reading binary data from {input_file}...")
    df = read_binary_file(input_file)
    results = pd.DataFrame()
    for channel in range(start_channel, end_channel+1):
        data, _ = process_channel(df, channel)
        if data is not None:
            results = pd.concat([results, data], ignore_index=True)
        # raw_data_channel,_ = process_channel(df,channel)
    raw_results = results.copy()
    track_reconstruction(raw_results)
    print(len(results[results['Channel']==7655]['Adj_ADCs'].values[0]))
    print("Applying threshold to adjusted ADC values...")
    thresholded_results = threshold_adj_adcs(results,0)
    # plot_adc_heatmap(thresholded_results)
    print("Removing cosmic events from data...")
    cleaned_results = remove_cosmic_events(thresholded_results)
    #plot(thresholded_results,results)
    print("Applying zero threshold to adjusted ADC values for area calculation...")
    raw_results_zero_threshold = threshold_adj_adcs(raw_results, threshold=50)

    print("Calculating ADC integrals...")
    adc_integral_df = calculate_adc_integrals(cleaned_results)
    print("Calculating ADC integrals for raw data...")
    raw_adc_integral_df = calculate_adc_integrals(raw_results_zero_threshold)
    adc_integral_df = adc_integral_df.sort_values('Channel').reset_index(drop=True)
    print("Calculating ADC areas...")
    raw_adc_integral_df = raw_adc_integral_df.sort_values('Channel').reset_index(drop=True)
    csv_output_file = os.path.splitext(output_file)[0] + "_adc_integrals.csv"
    print(f"Saving ADC integrals to {csv_output_file}.csv...")
    #raw_adc_integral_df.to_csv("filetest.csv",index=False)
    area_results_df = adc_area(adc_integral_df, raw_adc_integral_df)
    #plot_adc(area_results_df,7655)
    #adc_integral_df.to_csv(csv_output_file, index=False)
    # print(f"Saving processed data to {output_file}...")
    # np.save(output_file, cleaned_results.to_dict(orient='list'))
    adc_areas_csv = os.path.splitext(output_file)[0] + "_adc_areas.csv"
    print(f"Saving ADC areas to {adc_areas_csv}...")
    #area_results_df.to_csv(adc_areas_csv, index=False)
    print("Processing complete!")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 main.py <input_file> <start_channel> <end_channel> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    start_channel = int(sys.argv[2])
    end_channel = int(sys.argv[3])
    output_file = sys.argv[4]


    main(input_file, start_channel, end_channel, output_file)    
