import numpy as np
def threshold_adj_adcs(df, threshold):
    """
    Applies a threshold to the adjusted ADC values.
    Args:
        df (pd.DataFrame): DataFrame containing 'Adj_ADCs'.
        threshold (int): Threshold value for ADC filtering. Default is 50.
    
    Returns:
        pd.DataFrame: DataFrame with 'Thresholded_Adj_ADCs' column added.
    """
    thresholded_adj_adcs = []
    for adj_adc_list in df['Adj_ADCs']:
        thresholded_list = [(value if value >= threshold else 0) for value in adj_adc_list]
        thresholded_adj_adcs.append(thresholded_list)
    # for i in thresholded_adj_adcs:
    #     print( np.sum(np.array(i) != 0))  
    df['Thresholded_Adj_ADCs'] = thresholded_adj_adcs
    #print(len(df[df['Channel']==7655]['Thresholded_Adj_ADCs'].values[0]))
    return df
