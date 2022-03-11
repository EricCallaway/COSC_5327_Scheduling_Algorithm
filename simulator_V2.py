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
                elif index < 101:
                    p_id = int(index)
                    arrive = int(line[:1])
                    priority = int(line[2:3])
                    cpu_time = line[4:6]
                    cpu_time.strip("\n")
                    cpu_time = int(cpu_time)
                    cpu_time2 = cpu_time
                    state = 0
                    process_data.append([p_id, arrive, priority, cpu_time, state, cpu_time2])
                else:
                    sys.exit("Sorry. The limit is 100 processes.\nPlease try again with 100 or less processes.")
                    break
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
    Quant = 2
    ans = input("Note that in the event of Round Robin scheduling, the default Quantum time is {}.\nWould you like to change the default Quantum time?\n(y/n): ".format(Quant))
    if ans.lower() == 'y':
        Quant = int(input("Please select the desired Quantum time: "))
    print("This is the process data sorted by arrival time: {}".format(process_data)) # Sort by arrival time
    while 1:
        ready_q = []
        normal_q = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3],
                             process_data[i][5]])
                ready_q.append(temp)
                temp = []
            elif process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4],
                             process_data[i][5]])
                normal_q.append(temp)
                temp = []
        if len(ready_q) == 0 and len(normal_q) == 0:
            break
        if len(ready_q) != 0:
            ready_q.sort(key = lambda process : process[2])
            # Loop through ready q. If the priority of the first element is repeated, then add all elements with the same priority to a RR Q
            RR_Q = check_RR(ready_q)
            if len(RR_Q) > 1:
                index = 0
                while len(RR_Q) > 0:
                    # If the element we are looking at's CPU time is greater than or equal to the Quant do this operation
                    if RR_Q[index][3] >= Quant:
                        s_time += Quant
                        e_time = s_time
                        exit_time.append(e_time)
                        for i in range(Quant):
                            sequence_of_process.append(RR_Q[index][0])
                        for k in range(len(process_data)):
                            if process_data[k][0] == RR_Q[index][0]:
                                break
                        process_data[k][3] -= Quant
                        RR_Q[index][3] = process_data[k][3]
                        if(process_data[k][3] == 0):
                            process_data[k][4] = 1
                            process_data[k].append(e_time)
                    # If the Remaining CPU time on this element is less than the Quant but not zero, do this operation
                    elif RR_Q[index][3] < Quant and RR_Q[index][3] > 0:
                        s_time += RR_Q[index][3]
                        e_time = s_time
                        exit_time.append(e_time)
                        for i in range(RR_Q[index][3]):
                            sequence_of_process.append(RR_Q[index][0])
                        for k in range(len(process_data)):
                            if (process_data[k][0] == RR_Q[index][0]):
                                break
                        process_data[k][3] -= RR_Q[index][3]
                        RR_Q[index][3] = process_data[k][3]
                        if process_data[k][3] == 0:
                            process_data[k][4] = 1
                            process_data[k].append(e_time)
                    if RR_Q[index][3] == 0:
                        del RR_Q[index]
                    # Ensures the index loop around list properly
                    index += 1
                    if (index > len(RR_Q) - 1):
                        index = 0
            # If there is no need to round robin, then continue with preemptive priority
            else:
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
                process_data[k].append(e_time)
    t_time = calculateTurnaroundTime(process_data)
    w_time = calculateWaitingTime(process_data)
    print("The average turnaround time is : {}".format(t_time))
    print("The average waiting time is : {}".format(w_time))
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

def check_RR(ready_q):
    round_robin_q = []
    for i in range(len(ready_q)):
        if ready_q[i][2] == ready_q[0][2]:
            round_robin_q.append(ready_q[i])
    return round_robin_q

main()



    

