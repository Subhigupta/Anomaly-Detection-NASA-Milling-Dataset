import pickle
import matplotlib.pyplot as plt
import pandas as pd
import os

#Visualizing the trend of all sensors data for first experimental run
def first_exp_run(mill_data):
    fig, ax = plt.subplots()

    ax.plot(mill_data[0,0]['smcAC'], label='smcAC')
    ax.plot(mill_data[0,0]['smcDC'], label='smcDC')
    ax.plot(mill_data[0,0]['vib_table'], label='vib_table')
    ax.plot(mill_data[0,0]['vib_spindle'], label='vib_spindle')
    ax.plot(mill_data[0,0]['AE_table'], label='AE_table')
    ax.plot(mill_data[0,0]['AE_spindle'], label='AE_spindle')

    plt.legend()
    plt.savefig(os.path.join(".gitignore" ,"First experimental run.png"))

#Visualizing the trend of all sensors data for first five experimental run
def first_five_exp_run(mill_data):
    for iteration in range(5):
        fig, ax = plt.subplots()

        ax.plot(mill_data[0,iteration]['smcAC'], label='smcAC')
        ax.plot(mill_data[0,iteration]['smcDC'], label='smcDC')
        ax.plot(mill_data[0,iteration]['vib_table'], label='vib_table')
        ax.plot(mill_data[0,iteration]['vib_spindle'], label='vib_spindle')
        ax.plot(mill_data[0,iteration]['AE_table'], label='AE_table')
        ax.plot(mill_data[0,iteration]['AE_spindle'], label='AE_spindle')

        plt.legend()
        plt.savefig(f"plot_{iteration}.png")
        plt.close()

#Visualizing the trend of all sensors data for all experimental runs
def all_exp_run(mill_data):
    for iteration in range(167):
        fig, ax = plt.subplots()

        ax.plot(mill_data[0,iteration]['smcAC'], label='smcAC')
        ax.plot(mill_data[0,iteration]['smcDC'], label='smcDC')
        ax.plot(mill_data[0,iteration]['vib_table'], label='vib_table')
        ax.plot(mill_data[0,iteration]['vib_spindle'], label='vib_spindle')
        ax.plot(mill_data[0,iteration]['AE_table'], label='AE_table')
        ax.plot(mill_data[0,iteration]['AE_spindle'], label='AE_spindle')

        plt.legend()
        plt.savefig(f"plot_{iteration}.png")
        plt.close()

#Storing the case, run and VB values in a dictionary
def VB_data(mill_data,fields):
    VB_field=fields[2]
    case_field=fields[0]
    run_field=fields[1]

    VB_array=[]
    case_array=[]
    run_array=[]

    dict={}
    for iter in range(167):
        VB_array.append(mill_data[0,iter][VB_field][0][0])
        case_array.append(mill_data[0,iter][case_field][0][0])
        run_array.append(mill_data[0,iter][run_field][0][0])

    dict['case']=case_array
    dict['VB']=VB_array
    dict['run']=run_array

    return dict,VB_array

#There are total 16 cases.
#Each case has few experimental runs. 
#For those experimental runs there are VB values.
#First, Visualizing VB values vs all the case values
def VB_plot(mill_data,fields):
    dict,VB_array=VB_data(mill_data,fields)
    data=pd.DataFrame(dict)
    plt.plot(VB_array,'o')
    plt.ylabel('VB measured for all experimental runs')
    plt.xlabel('Number of experiments conducted')
    plt.savefig(os.path.join("Plots_for_VB_data","VB_for_all_plots"))

    return data

#Now, visualizing VB trends under each case
def VB_plots_case(data):
    for iter in range(1,17):
        data_iter=data[data['case']==iter]
        plt.plot(data_iter['VB'],'o',label=f'Case {iter}')
        plt.ylabel('VB measured for all experimental runs')
        plt.xlabel('Number of experiments conducted')
        plt.legend()
        plt.savefig(f"plot_{iter}.png")
        plt.close()

#If we see from VB plots generated for all the cases. 
#Case13 seems to overshoot.
#So visualizing all the sensors trends for case1 and case 13
def VB_indexes_case1_case13(mill_data,fields,data):
    sensor_fields=fields[7:13]
    num_runs_case1=data[data['case']==1]['run']
    indexes_case1=data[data['case']==1].index

    num_runs_case13=data[data['case']==13]['run']
    indexes_case13=data[data['case']==13].index

    return sensor_fields,indexes_case1,indexes_case13

def VB_case1_case13_plots(sensor_fields,indexes_case1,indexes_case13,mill_data):
    for sensor in sensor_fields:
        fig, ax = plt.subplots()
        count=0
        for index in indexes_case1:
            count=count+1
            ax.plot(mill_data[0,index][sensor], label=f"{sensor} Run {count}")
            plt.legend()
        
        plt.savefig(f"plot_case 1_{sensor}.png")
        plt.close()


    for sensor in sensor_fields:
        fig, ax = plt.subplots()
        count=0
        for index in indexes_case13:
            count=count+1
            ax.plot(mill_data[0,index][sensor], label=f"{sensor} Run {count}")
            plt.legend()
        
        plt.savefig(f"plot_case 13_{sensor}.png")
        plt.close()

    return indexes_case1,indexes_case13

def main_data_analysis():

    with open('mill_data.pkl', 'rb') as f:
        mill_data = pickle.load(f)

    fields= mill_data.dtype.names

    #first_exp_run(mill_data)      #commented as plots have been generated
    #first_five_exp_run(mill_data) #commented as plots have been generated
    #all_exp_run(mill_data)        #commented as plots have been generated
    data=VB_plot(mill_data,fields)
    print(data)
    #VB_plots_case(data)           #commented as plots have been generated
    sensor_fields,indexes_case1,indexes_case13=VB_indexes_case1_case13(mill_data,fields,data)
    #VB_case1_case13_plots(sensor_fields,indexes_case1,indexes_case13,mill_data) #commented as plots have been generated

    indexes_case1_case13=(indexes_case1,indexes_case13)
    #Store the tuple to a file
    with open('indexes_case1_case13.pkl', 'wb') as f:
        pickle.dump(indexes_case1_case13, f)

    with open('data.pkl','wb') as f:
        pickle.dump(data, f)
