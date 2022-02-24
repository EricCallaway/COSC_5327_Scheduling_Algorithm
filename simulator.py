import enum
import fileinput
import sys
from matplotlib.cbook import print_cycles
from numpy import *
import numpy
import os


# Process Class
class Process:
    def __init__(self, p_id, arrive, priority, cpu_time, state):
        self.p_id = p_id
        self.arrive = arrive
        self.priority = priority
        self.cpu_time = cpu_time
        self.state = state
    
    

# Reads the file and enumerates the lines. 
def read_file(file_path):
    list_of_processes = []
    try:
        with open(file_path, "r") as data:
            for index, line in enumerate(data):
                if index == 0:
                    num_processes = line
                else:
                    process = Process(index, line[:1], line[2:3], line[4:], 0)
                    list_of_processes.append(process)
                print("Line {}: {}". format(index, line.strip()))
    except FileNotFoundError:
        list_of_processes = None
    return num_processes, list_of_processes

def pre_priority(self):
    pass

def round_robin(self):
    pass




def scheduling_process(num_processes, list_of_processes):
    start_time = []
    exit_time =[]
    s_time = 0
    current_num_processes = num_processes
    list_of_processes.sort(key = lambda process : process.arrive) #Sort list by arrival time
    print("The following processes are sorted by arrival time:")
    for index, p in enumerate(list_of_processes):
        print("Process ID: {}\nProcess Arrival Time: {}\nProcess Priority: {}\nProcess CPU_Time: {}\n".format(p.p_id, p.arrive, p.priority, p.cpu_time))



    # while current_num_processes > 0:
    #     ready_queue = []
    #     normal_queue = []
    #     temp = []
    #     for i in range(len(list_of_processes)):
    #         pass






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
    print("The number of processes to be processed: {}".format(num_processes))
    for index, p in enumerate(list_of_processes):
        print("Process ID: {}\nProcess Arrival Time: {}\nProcess Priority: {}\nProcess CPU_Time: {}\n".format(p.p_id, p.arrive, p.priority, p.cpu_time))
    
    run = scheduling_process(num_processes, list_of_processes)

main()




    

