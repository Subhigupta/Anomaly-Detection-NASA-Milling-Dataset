from Step3_Feature_Extraction import frequency_features
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis
import os

with open('mill_data.pkl', 'rb') as f:
        mill_data = pickle.load(f)

def time_domain_features(signal):
    mean=np.mean(signal)
    std_dev=np.std(signal)
    kurt=kurtosis(signal)
    skewness=skew(signal)
    rms=np.sqrt(np.mean(signal**2))
    peak_to_peak=np.max(signal)-np.min(signal)
    crest_factor = np.max(np.abs(signal)) /rms
    shape_factor = rms/mean
    impulse_factor = (np.max(np.abs(signal)) / mean)
    margin_factor=np.max(np.abs(signal))//(np.mean(np.sqrt(signal)))**2
    energy=np.sum(signal**2)

    return mean,std_dev,kurt,skewness,rms,peak_to_peak,crest_factor,shape_factor,impulse_factor,margin_factor,energy


def func(sensor_field):
    new_SK_Mean=[]
    new_SK_Std=[]
    new_SK_Kurt=[]
    new_SK_Skewness=[]
    new_mean=[]
    new_std_dev=[]
    new_kurt=[]
    new_skewness=[]
    new_rms=[]
    new_peak_to_peak=[]
    new_crest_factor=[]
    new_shape_factor=[]
    new_impulse_factor=[]
    new_margin_factor=[]
    new_energy=[]

    for run in range(167):
        signal_data=mill_data[0,run][sensor_field]
        signal_data=signal_data.flatten()
        #print(signal_data.shape)
        SK_Mean, SK_Std, SK_Kurt,SK_Skewness=frequency_features(signal_data)
        mean,std_dev,kurt,skewness,rms,peak_to_peak,crest_factor,shape_factor,impulse_factor,margin_factor,energy=time_domain_features(signal_data)
        
        new_SK_Mean.append(SK_Mean)
        new_SK_Std.append(SK_Std)
        new_SK_Kurt.append(SK_Kurt)
        new_SK_Skewness.append(SK_Skewness)
        new_mean.append(mean)
        new_std_dev.append(std_dev)
        new_kurt.append(kurt)
        new_skewness.append(skewness)
        new_rms.append(rms)
        new_peak_to_peak.append(peak_to_peak)
        new_crest_factor.append(crest_factor)
        new_shape_factor.append(shape_factor)
        new_impulse_factor.append(impulse_factor)
        new_margin_factor.append(margin_factor)
        new_energy.append(energy)
        
    # for feature in features_list:
    #     name=f"new_{feature}"
    #     dict[f"{feature}_{sensor_field}"]=name
    dict[f"SK_Mean_{sensor_field}"]=new_SK_Mean
    dict[f"SK_Std_{sensor_field}"]=new_SK_Std
    dict[f"SK_Kurt_{sensor_field}"]=new_SK_Kurt
    dict[f"SK_Skewness_{sensor_field}"]=new_SK_Skewness
    dict[f"mean_{sensor_field}"]=new_mean
    dict[f"std_dev_{sensor_field}"]=new_std_dev
    dict[f"kurt_{sensor_field}"]=new_kurt
    dict[f"skewness_{sensor_field}"]=new_SK_Skewness
    dict[f"rms_{sensor_field}"]=new_rms
    dict[f"peak_to_peak_{sensor_field}"]=new_peak_to_peak
    dict[f"crest_factor_{sensor_field}"]=new_crest_factor
    dict[f"shape_factor_{sensor_field}"]=new_shape_factor
    dict[f"impulse_factor_{sensor_field}"]=new_impulse_factor
    dict[f"margin_factor_{sensor_field}"]=new_margin_factor
    dict[f"energy_{sensor_field}"]=new_energy

def plots(total_extracted_features,sensor_fields,features_list):
     for sensor_field in sensor_fields:
          for feature in features_list:
               column_name=f"{feature}_{sensor_field}"
               plt.plot(range(0,167),total_extracted_features[column_name],label=column_name)
               plt.xlabel("Experiment runs")
               plt.ylabel(column_name)
               plt.legend()
               plt.savefig(os.path.join("Feature_Extraction_Plots",column_name))
               plt.close()
     

features_list=['mean','std_dev','kurt','skewness','rms','peak_to_peak','crest_factor','shape_factor',
               'impulse_factor','margin_factor','energy','SK_Mean', 'SK_Std', 'SK_Kurt', 'SK_Skewness']   

sensor_fields=['vib_table','vib_spindle']

dict={}
fields= mill_data.dtype.names
sensor_fields=fields[9:11]

for sensor_field in sensor_fields:
    print(sensor_field)
    func(sensor_field)

total_extracted_features=pd.DataFrame(dict)
print(total_extracted_features)

# plt.plot(range(0,167),total_extracted_features["SK_Mean_vib_table"])
# plt.xlabel("Experiment runs")
# plt.ylabel("SK_Mean_vib_table")
# plt.show()

plots(total_extracted_features,sensor_fields,features_list)

with open('total_extracted_features.pkl', 'wb') as f:
    pickle.dump(total_extracted_features, f)

