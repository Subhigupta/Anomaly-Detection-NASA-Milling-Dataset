from scipy.io import loadmat 
import pickle

# load mill mat file
mat_data=loadmat("mill.mat")

def main_data_profiling():
    # See the contents of mat_data
    print("Data is in form of",type(mat_data)) # so the mill_data is inside the dictionary.
    print("Keys of dictionary",mat_data.keys()) #the mill_data can be accessed with a key

    # See the contents of the mill_data
    print("Mill data is in form of",type(mat_data['mill']))

    mill_data=mat_data['mill']

    print("mill_data is stored as",mill_data.dtype) # a structured datatype

    print("Field names",mill_data.dtype.names) #to access the field names of a structured datatype use 
                                            #the names attribute of the dtype object

    print("Shape of mil_data",mill_data.shape) #a 2D array

    #Exploring for first experimental run

    #the following commands provide steps to how to access field values of each experimental run
    mill_data[0].shape #a 1D array
    mill_data[0,0]#this gives you the values for only the fields for first row out of total 167 rows.
    mill_data[0,0]['case'][0][0] #to access the values within the field

    # Lets print what is what are the values of the fields for the first row

    # First lets see the operating conditions
    fields= mill_data.dtype.names
    for field in fields[0:7]:
        print(f"Value of {field} is {mill_data[0,0][field][0][0]}")

    #Lets see the shape of 6 sensors data:
    for field in fields[7:]:
        print(f"Shape of {field} is {mill_data[0,0][field].shape}")

    # Store the variable to a file
    with open('mill_data.pkl', 'wb') as f:
        pickle.dump(mill_data, f)

# data_profiling()