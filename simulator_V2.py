import enum
import fileinput
import sys
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
    



# Reads the file and enumerates the lines. 
def read_file(file_path):
    temp = []
    list_of_processes = []
    try:
        with open(file_path, "r") as data:
            for index, line in enumerate(data):
                if index == 0:
                    num_processes = line
                else:
                    p_id = index
                    arrive = line[:1]
                    priority = line[2:3]
                    cpu_time = line[4:6]
                    state = 0
                    temp.extend([p_id, arrive, priority, cpu_time, state])
                    list_of_processes.append(temp)
                print("Line {}: {}". format(index, line.strip()))
    except FileNotFoundError:
        list_of_processes = None
    return num_processes, list_of_processes

# def pre_priority(list_of_processes):
#     ready_queue = []
#     normal_queue = []
#     sequence_of_processes = []
#     start_time = []
#     s_time = 0
#     list_of_processes.sort(key = lambda process : process.arrive) # Sort processes by arrival time
#     for index, k in enumerate(list_of_processes):
#         while s_time < int(list_of_processes[index].arrive):
#             s_time += 1
#         start_time.append(s_time)
#         ready_queue.append(list_of_processes[index])
#         if len(ready_queue) == 0 and len(normal_queue) == 0:
#             break

#         if len(ready_queue) != 0:
#             for priority in ready_queue:
#                 # temp = ready_queue[i]
#                 # print("This is the element in the ready queue: {}".format(temp))
#                 print(priority)
#                 print(list_of_processes[index])
#                 if list_of_processes[index] == priority:                    # Process is already in the ready queue
#                     normal_queue.append(list_of_processes)                  # Add to normal queue
#                     break                  
#                 elif list_of_processes[index].priority < priority:         # Incoming item is greater priority than current item in ready Q
#                     print("{} is of higher priority than {}".format(list_of_processes[index], priority))
#                 #     list_of_processes[index] = ready_queue[i-1]         # Shift ready Q
#                 # else:
#                 #      break

            
            
                


        
        
         

# def round_robin(self):
#     pass

# def priortiy_sort(self):
#     return self.sort(key = lambda process : process.priority)




# def scheduling_process(num_processes, list_of_processes):
    start_time = []
    exit_time =[]
    s_time = 0
    sequence_of_processes = []
    current_num_processes = int(num_processes)
    list_of_processes.sort(key = lambda process : process.arrive) #Sort list by arrival time
    print("The following processes are sorted by arrival time:")
    for index, p in enumerate(list_of_processes):
        print("Process ID: {}\nProcess Arrival Time: {}\nProcess Priority: {}\nProcess CPU_Time: {}\n".format(p.p_id, p.arrive, p.priority, p.cpu_time))

    while current_num_processes > 0:
        ready_queue = []
        normal_queue = []
        temp = []
        for index, p in enumerate(list_of_processes):                           # Loop through list of processes
            if int(p.arrive) <= s_time and p.state == 0:                        # if arrival time is less than or equal to start time, and the processes state is 0 (unifinished)
                temp.append(p)                                                  # Add process to temp list
                print("This is the temporary list: {}".format(temp[index].p_id))
                temp = priortiy_sort(temp)                                      # Sort by priority
                ready_queue.append(temp)                                        # Add temp list to ready queue. Do I need this?
                print("This is the ready queue: {}".format(ready_queue[index]))
                temp = []                                                       # Empty temp list
            elif p.state == 0:                                                  # Else (arrival time is greater than start time) and state is still unfinished add to normal queue
                temp.append(p)
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:                    # If ready queue and normal queue are empty, break out of loop (back in while loop)      
            break
        if len(ready_queue) != 0:                                               # If ready queue is not empty
            start_time.append(s_time)                                           # Add starting time to start_time list
            s_time += 1                                                         # Increase start time by one
            e_time = s_time                                                     # Assign val of s_time to e_time
            exit_time.append(e_time)                                            # Add e_time to exit_time list
            sequence_of_processes.append(ready_queue[0].p_id)                   # Add current p_id to sequence of processes list
            for index, k in enumerate(list_of_processes):                       # Loop through list of processes
                if(int(list_of_processes[index].p_id) == int(ready_queue[0].p_id)):     # If the current element in the list of processes is the same as the first element in the ready queue break out of loop into outer for loop
                    break
            list_of_processes[index].cpu_time -= 1      #Subtract one from cpu burst time for this process
            if list_of_processes[index].cpu_time == 0:                          # If cpu time is 0 (the process is complete)
                list_of_processes[index].state = 1                              # Set state to one
                list_of_processes[index].exit_time = e_time                     # Assign exit time to value of e_time
        if len(ready_queue) == 0:                                               # If ready queue is empty but normal queue is not
            normal_queue.sort(key = lambda process : process.arrive)            # Sort normal queue
            if s_time < normal_queue[0].arrive:                                 # If start time is less than the arrival time of item in normal queue
                s_time = normal_queue[0].arrive                                # Assign arrival time to start time
            start_time.append(s_time)                                           # Add this start time to the list of start times
            s_time += 1                                                         # Increment start time by one
            e_time = s_time                                                     # Assign exit time val of start time
            exit_time.append(e_time)                                               # Add e_time to exit time list
            sequence_of_processes.append(normal_queue[0].p_id)                  # Add current p_id to sequence of processes list
            for index, k in enumerate(list_of_processes):                       # Loop through list of processes
                if list_of_processes[index].p_id == normal_queue[0].p_id:       # If p_id is the same as p_id in normal queue break out of for loop
                    break
            list_of_processes[index].cpu_time -= 1                              # Subtract one from cpu_time
            if list_of_processes[index].cpu_time == 0:                          # If cpu time is zero then the process is finished. 
                list_of_processes[index].state = 1
                list_of_processes[index].exit_time = e_time
        current_num_processes -= 1
    return sequence_of_processes, start_time, exit_time
    







    
    # sequence_of_processes, start_time, exit_time = scheduling_process(num_processes, list_of_processes)
    # pre_priority(list_of_processes)

main()




    

