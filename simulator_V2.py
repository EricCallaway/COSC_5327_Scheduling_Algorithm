from asyncore import read
from concurrent.futures import process
from encodings import normalize_encoding
import enum
import fileinput
from genericpath import exists
# from msilib import sequence
import sys
from tracemalloc import start
from matplotlib.cbook import print_cycles
from numpy import *
import numpy
import os

def main():
    # Grabs the second command line argument (file name)
    file_path = sys.argv[1]
    # Checks if the file exists
    if not os.path.isfile(file_path):
        print("File path {} does not exist. Exiting...".format(file_path))
        sys.exit()
    # Pass file into read_file function
    # Return number of processes and list of the processes
    num_processes, list_of_processes = read_file(file_path)
    pre_priority(num_processes, list_of_processes)
    
    



# Reads the file and enumerates the lines. 
def read_file(file_path):
    process_data = []
    try:
        with open(file_path, "r") as data:
            for index, line in enumerate(data):
                if index == 0:
                    num_processes = int(line)
                else:
                    p_id = int(index)
                    arrive = int(line[:1])
                    priority = int(line[2:3])
                    cpu_time = line[4:6]
                    cpu_time.strip("\n")
                    cpu_time = int(cpu_time)
                    cpu_time2 = cpu_time
                    state = 0
                    process_data.append([p_id, arrive, priority, cpu_time, state, cpu_time2])
                print("Line {}: {}". format(index, line.strip()))
    except FileNotFoundError:
        process_data = None
    return num_processes, process_data

def pre_priority(num_pprocesses, process_data):
    iteration = 0
    start_time = []
    exit_time = []
    s_time = 0
    sequence_of_process = []
    process_data.sort(key=lambda x: x[1])
    print("This is the process data sorted by arrival time: {}".format(process_data)) # Sort by arrival time
    while 1:
        iteration += 1
        print("*************NEW ITERATION # {}**************".format(iteration))
        ready_q = []
        normal_q = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3],
                             process_data[i][5]])
                ready_q.append(temp)
                print("This is the ready_q: {}".format(ready_q))
                temp = []
            elif process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4],
                             process_data[i][5]])
                normal_q.append(temp)
                print("This is the normal_q: {}".format(normal_q))
                temp = []
        if len(ready_q) == 0 and len(normal_q) == 0:
            break
        if len(ready_q) != 0:
            ready_q.sort(key = lambda process : process[2])
            print("This is the ready Q sorted by priority: {}".format(ready_q))
            start_time.append(s_time)
            s_time += 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(ready_q[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == ready_q[0][0]:
                    break
            process_data[k][3] -= 1
            if process_data[k][3] == 0:
                process_data[k][4] = 1
                process_data[k].append(e_time)
        if len(ready_q) == 0:
            normal_q.sort(key = lambda process : process[1])
            if s_time < normal_q[0][1]:
                s_time = normal_q[0][1]
            start_time.append(s_time)
            s_time += 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(normal_q[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_q[0][0]:
                    break
            process_data[k][3] -= 1
            if process_data[k][3] == 0:
                process_data[k][4] = 1
                process_data.append(e_time)
    t_time = calculateTurnaroundTime(process_data)
    w_time = calculateWaitingTime(process_data)
    print("The total turnaround time is : {}".format(t_time))
    print("The total waiting time is : {}".format(w_time))
    printData(process_data, t_time, w_time, sequence_of_process)

def calculateTurnaroundTime(process_data):
    total_turnaround_time = 0
    for i in range(len(process_data)):
        turnaround_time = process_data[i][6] - process_data[i][1]
        total_turnaround_time = total_turnaround_time + turnaround_time
        process_data[i].append(turnaround_time)
    average_turnaround_time = total_turnaround_time / len(process_data)
    return average_turnaround_time

def calculateWaitingTime(process_data):
    total_waiting_time = 0
    for i in range(len(process_data)):
        print(process_data)
        waiting_time = process_data[i][7] - process_data[i][5]
        total_waiting_time = total_waiting_time + waiting_time
        process_data[i].append(waiting_time)
    average_waiting_time = total_waiting_time / len(process_data)
    return average_waiting_time

def printData(process_data, average_turnaround_time, average_waiting_time, seqeuence_of_process):
    process_data.sort(key = lambda process: process[0]) # Sort by P_id
    print("P_ID\tArrival Time\t    Priority\tCurrent CPU BT  \t State\t Original CPU BT   Exit Time     Turnaround Time\t   Waiting Time")
    for i in range(len(process_data)):
        for j in range(len(process_data[i])):
            print(process_data[i][j], end="\t|\t  ")
        print()
    print("Average Turnaroud time: {}".format(average_turnaround_time))
    print("Average Waiting Time: {}".format(average_waiting_time))
    print("Sequence of Processes: {}".format(seqeuence_of_process))
            






main()



    

