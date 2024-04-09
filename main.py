import pickle
from Step1_Data_Profiling import main_data_profiling
from Step2_Data_Analysis import main_data_analysis
from Step3_Feature_Extraction import main_features_extraction

#call the data profiling function
main_data_profiling()

#call the analysis functions
main_data_analysis()

main_features_extraction()

