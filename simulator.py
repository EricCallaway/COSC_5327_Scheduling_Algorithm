import enum
import fileinput
import sys
from matplotlib.cbook import print_cycles
from numpy import *
import numpy
import os


# Process Class
class Process:
    def __init__(self, p_id, arrive, priority, cpu_time):
        self.p_id = p_id
        self.arrive = arrive
        self.priority = priority
        self. cpu_time = cpu_time
    
    

# Reads the file and enumerates the lines. 
def read_file(file_path):
    rec = 2
    list_of_processes = []
    try:
        with open(file_path, "r") as data:
            for index, line in enumerate(data):
                if index == 0:
                    num_processes = line
                else:
                    process = Process(index, line[:1], line[2:3], line[4:])
                    list_of_processes.append(process)
                print("Line {}: {}". format(index, line.strip()))
    except FileNotFoundError:
        rec = None
    return rec, num_processes, list_of_processes




def main():
    # Grabs the second command line argument (file name)
    file_path = sys.argv[1]
    # Checks if the file exists
    if not os.path.isfile(file_path):
        print("File path {} does not exist. Exiting...".format(file_path))
        sys.exit()
    # Pass file into read_file function
    record, num_processes, list_of_processes = read_file(file_path)
    print("The number of processes to be processed: {}".format(num_processes))
    for index, p in enumerate(list_of_processes):
        print("Process ID: {}\nProcess Arrival Time: {}\nProcess Priority: {}\nProcess CPU_Time: {}\n".format(p.p_id, p.arrive, p.priority, p.cpu_time))

main()




    

