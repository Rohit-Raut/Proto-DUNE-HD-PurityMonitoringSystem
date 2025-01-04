import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd

def plot(dfx, dfy):
    channel_to_plot = 7655
    channel_data = dfx[dfx ['Channel'] == channel_to_plot]
    if not channel_data.empty:
       # original_adc_values_series = dfy[dfy['Channel'] == channel_to_plot]['ADC Values'].iloc[0]
        baseline = dfx[dfx['Channel'] == channel_to_plot]['Thresholded_Adj_ADCs'].iloc[0]
        adc_values = dfy[dfy['Channel'] == channel_to_plot]['Adj_ADCs'].iloc[0]
        plt.figure(figsize=(15, 10))
        plt.subplot(3, 1, 1)
        plt.plot(adc_values, label='Original ADC Values', color='blue')
        #plt.plot(baseline, label='Rolling Baseline', color='red', linestyle='--')
        plt.title(f'Channel {channel_to_plot} - Original ADC Values')
        plt.xlabel('Index [512ns/ticks]')
        plt.ylabel('ADC Value')
        plt.legend()
        #plt.xlim((130000,140000))
        # plt.xscale('log')
        plt.grid(True)
        plt.subplot(3, 1, 2)
        plt.plot(baseline, label='After Thresholding at 100ADC count', color='green')
        plt.title(f'Channel {channel_to_plot} -after thresholding at 100ADC count')
        plt.xlabel('Index [512ns/ticks]')
        plt.ylabel('ADC Value (Adjusted)')
        plt.legend()
        #plt.xlim((130000,140000))
        plt.grid(True)
        plt.subplot(3, 1, 3)
        plt.plot(adc_values, label='Original ADC Values', color='blue', alpha=0.5)
        plt.plot(baseline, label='Thresholded ADC values', color='green', alpha=0.7)
        plt.title(f'Channel {channel_to_plot} - Overlay of Original and Thresholded at 100ADCs count')
        plt.xlabel('Index [512ns/ticks]')
        plt.ylabel('ADC Value')
        plt.legend()
        #plt.xlim((130000,140000))
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No data found for channel {channel_to_plot}.")


def plot_adc(area_results_df, channels_to_plot):
    bin_width = 30
    max_area = area_results_df['Area'].max()
    print(f"Max Area: {max_area}")
    bins = np.arange(0, max_area + bin_width, bin_width)
    if channels_to_plot is None:
        channels_to_plot = area_results_df['Channel'].unique()
    else:
        if isinstance(channels_to_plot, int):
            channels_to_plot = [channels_to_plot]
        else:
            channels_to_plot = list(channels_to_plot)
    
    plt.figure(figsize=(10, 6))
    for channel in channels_to_plot:
        channel_data = area_results_df[area_results_df['Channel'] == channel]['Area']
        if channel_data.empty:
            print(f"No data found for Channel {channel}. Skipping.")
            continue
        plt.hist(channel_data, bins=bins, label=f'Channel {channel}', histtype='step', linewidth=1.5)
        print(f"Channel {channel}")
        print(channel_data.describe())
        
    
    plt.xlabel('ADC Area ')
    plt.ylabel('Count')
    plt.title('Bi 207 ADC Integral')
    plt.grid(False)
    plt.xlim((0, 5000))
    plt.legend(title="Channels", loc='best')
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(250))  
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_adc_heatmap(df):
    adc_values = pd.DataFrame(df['Thresholded_Adj_ADCs'].tolist())
    adc_values.index = df['Channel']  # Set channels as index
    plt.figure(figsize=(12, 8))
    plt.imshow(adc_values, aspect='auto', cmap='plasma', interpolation='nearest', origin='lower')
    
    # Add color bar to represent ADC count
    plt.colorbar(label='ADC Count')
    
    # Label axes
    plt.xlabel('Time Frame')
    plt.ylabel('Channel No.')
    plt.title('ADC Counts over Time Frames and Channels')
    
    plt.show()

def track_reconstruction(df):
     #okay firstly lets get the only time/adc count/adc channel info
    df = df.explode(['Timestamps', 'Adj_ADCs']) #Explode the data frameå
    df['Timestamps'] = pd.to_numeric(df['Timestamps'], errors='coerce')
    df['Adj_ADCs'] = pd.to_numeric(df['Adj_ADCs'], errors='coerce')
    t_min = df['Timestamps'].min()
    df['time_index'] = df['Timestamps'] - t_min + 1
    df_pivot = df.pivot(index='time_index', columns='Channel', values='Adj_ADCs')
    adc_array = df_pivot.values
    time_index = df_pivot.index.values
    channel_index = df_pivot.columns.values

    fig, ax =  plt.subplots(figsize=(10,6))
    cax = ax.imshow(
        adc_array, aspect='auto', cmap='plasma', interpolation='nearest', origin='lower'
    )
    ax.set_xticks(np.arange(len(channel_index)))
    ax.set_xticklabels(channel_index, rotation=85, ha='right')
    step = max(1, len(time_index)//10)  # only 10 major ticks
    y_ticks = np.arange(0, len(time_index), step)
    y_labels = [f"{time_index[i]:.0f}" for i in y_ticks]

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)

    ax.set_xlabel('Channel')
    ax.set_ylabel('Time index')
    fig.colorbar(cax, label='ADC Count')
    plt.title('ADC Scatter of (Channel vs. Time)')
    plt.tight_layout()
    plt.savefig('track.png', dpi=500)
    plt.close()


        
        


