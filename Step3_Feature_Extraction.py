import pickle
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from scipy.fft import fft
from scipy.signal import welch



def frequency_features(signal):
    # Assuming 'signal' contains the vibration data
    # Assuming 'nperseg' is the length of each segment
    # Assuming 'noverlap' is the overlap between segments
    
    # Initialize an empty list to store spectral kurtosis values for each segment
    spec_kurtosis_segments = []
    noverlap=90
    nperseg=180

    # Calculate the number of segments
    num_segments = (len(signal) - noverlap) // (nperseg - noverlap)

    # Loop over each segment
    for i in range(num_segments):
        # Extract the current segment
        segment = signal[i * (nperseg - noverlap): i * (nperseg - noverlap) + nperseg]
        #print(i,len(segment))

        # Compute power spectral density using Welch method
        freqs, psd = welch(segment, nperseg=nperseg)

        # Compute kurtosis of the power spectrum
        spec_kurtosis = kurtosis(psd, fisher=False)  # Fisher's definition of kurtosis

        # Append the spectral kurtosis to the list
        spec_kurtosis_segments.append(spec_kurtosis)

    # Convert the list of spectral kurtosis values into a numpy array
    spec_kurtosis_segments = np.array(spec_kurtosis_segments)

    # Example of feature analysis
    #print("Spectral Kurtosis for each segment:", spec_kurtosis_segments)
    #print(len(spec_kurtosis_segments))

    SK_Mean=np.mean(spec_kurtosis_segments)
    SK_Std=np.std(spec_kurtosis_segments)
    SK_Kurt=kurtosis(spec_kurtosis_segments)
    SK_Skewness=skew(spec_kurtosis_segments)

    return SK_Mean, SK_Std, SK_Kurt,SK_Skewness

def features_extracted(vib_table_case1_run1_array,vib_spindle_case1_run1_array,
                       vib_table_case13_run1_array,vib_spindle_case13_run1_array):

    features_dict={}
    variable_names=['table','spindle']
    cases=['case1','case13']

    # Two vibration arrays for each case
    case_data = {
        'case1': {
            'table': vib_table_case1_run1_array,
            'spindle': vib_spindle_case1_run1_array
        },
        'case13': {
            'table': vib_table_case13_run1_array,
            'spindle': vib_spindle_case13_run1_array
        }
    }

    for case in cases:
        case_results={}
        for variable in variable_names:
            vib_array=case_data[case][variable]
            statistics_results={}

            statistics_results['mean']=np.mean(vib_array)
            statistics_results['std_dev']=np.std(vib_array)
            statistics_results['kurt']=kurtosis(vib_array)
            statistics_results['skewness']=skew(vib_array)
            statistics_results['rms']=np.sqrt(np.mean(vib_array**2))
            statistics_results['peak_to_peak']=np.max(vib_array)-np.min(vib_array)
            statistics_results['crest_factor'] = np.max(np.abs(vib_array)) / statistics_results['rms']
            statistics_results['shape_factor'] = statistics_results['rms']/statistics_results['mean']
            statistics_results['impulse_factor'] = (np.max(np.abs(vib_array)) / statistics_results['mean'])
            statistics_results['margin_factor']=np.max(np.abs(vib_array))//(np.mean(np.sqrt(vib_array)))**2
            statistics_results['energy']=np.sum(vib_array**2)

            SK_Mean, SK_Std, SK_Kurt,SK_Skewness=frequency_features(vib_array)
            statistics_results['SK_Mean']=SK_Mean
            statistics_results['SK_Std']=SK_Std
            statistics_results['SK_Kurt']=SK_Kurt
            statistics_results['SK_Skewness']=SK_Skewness            

            # Store the result dictionary under variable name
            case_results[f"{case}_vib_{variable}"] = statistics_results
        
        features_dict[f"{case}"]=case_results
    
    return features_dict

def vib_array(mill_data,indexes_case1,indexes_case13):
    #taking the vibration data of first experimental run from case study 1
    #taking first index from indexes_case1 list
    vib_table_case1_run1=mill_data[0,indexes_case1[0]]['vib_table']  
    vib_spindle_case1_run1=mill_data[0,indexes_case1[0]]['vib_spindle']

    #taking the vibration data of first experimental run from case study 13
    #taking first index from indexes_case13 list
    vib_table_case13_run1=mill_data[0,indexes_case13[0]]['vib_table']
    vib_spindle_case13_run1=mill_data[0,indexes_case13[0]]['vib_spindle']

    vib_table_case1_run1_array=vib_table_case1_run1.flatten()
    vib_spindle_case1_run1_array=vib_spindle_case1_run1.flatten()

    vib_table_case13_run1_array=vib_table_case13_run1.flatten()
    vib_spindle_case13_run1_array=vib_spindle_case13_run1.flatten()

    features_dict= features_extracted(vib_table_case1_run1_array,vib_spindle_case1_run1_array,vib_table_case13_run1_array,vib_spindle_case13_run1_array)

    return features_dict

def main_features_extraction():
    with open('mill_data.pkl', 'rb') as f:
        mill_data = pickle.load(f)

    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)

    with open('indexes_case1_case13.pkl', 'rb') as f:
        indexes_case1_case13= pickle.load(f)

    indexes_case1,indexes_case13=indexes_case1_case13
    features_dict=vib_array(mill_data,indexes_case1,indexes_case13)

    extracted_features_dict={'case1_vib_table_features':features_dict['case1']['case1_vib_table'], 
                'case1_spindle_table_features':features_dict['case1']['case1_vib_spindle'],
                'case13_vib_table_features':features_dict['case13']['case13_vib_table'],
                'case13_spindle_table_features':features_dict['case13']['case13_vib_spindle']}
    extracted_features_data=pd.DataFrame(extracted_features_dict)
    print(extracted_features_data)

    with open('extracted_features_data.pkl', 'wb') as f:
        pickle.dump(extracted_features_data, f)