'''
System resource manager engine.  Handles the logic for process and resource usage.
Created by: Charles Dodge
Class: CIS 452
Professor: Greg Wolffe
'''

import sys
import GUI
import time

#initialize file with system args
f1 = sys.argv[1]

#readlines of assigned file and store into variable "file"
with open(f1) as f:
    file = f.readlines()

#strip file of \n character
file = [end.strip().split() for end in file]

num_processes = int(file[0][0])
num_resources = int(file[1][0])

dict_processes = {}
dict_resources = {}

process_state = {}
resource_state = {}

#create list of instructions
instructions = []
for i in range(2, len(file)):
    instructions.append(file[i])

#print(num_processes)
#print(num_resources)
#print(instructions)

#create dictionary of process names and states
def create_processes(num_processes):
    i = 0
    while i <= (num_processes - 1):
        dict_processes['p' + str(i)] = 'p' + str(i)
        process_state['p' + str(i)] = 0
        i+=1

#create dictionary of resource names and states
def create_resources(num_resources):
    i = 0
    while i <= (num_resources - 1):
        dict_resources['r' + str(i)] = 'r' + str(i)
        resource_state['r' + str(i)] = 0
        i += 1

create_processes(num_processes)
create_resources(num_resources)
#print(dict_processes)
#print(dict_resources)

#read each instruction individually to determine what happens next
def read_instructions(instructions):

    G = GUI.draw_plot_first(dict_processes, dict_resources)

    for i in instructions:

        time.sleep(int(sys.argv[2]))
        print(i[0] + ' ' + i[1] + ' ' + i[2])

        #request conditions if found in instructions
        if "requests" in i:

            #print("i[0] = ",i[0])
            #print("i[2] = ", i[2])
            #print(dict_resources[i[2]])
            #print('resource state = ', resource_state[i[2]])

            # display line from r to p unless r:1
            if resource_state[i[2]] == 0:
                print(i[0] + ' now owns ' + i[2] + '\n')
                resource_state[i[2]] = 1
                G.add_edge(i[2], i[0])
                GUI.draw_plot(G, dict_processes, dict_resources)

            #if resource is blocked, add line from p to r
            elif resource_state[i[2]] == 1:
                print('process ' + i[0] + ' is blocked\n')
                G.add_edge(i[0], i[2])
                process_state[i[0]] = 1
                dict_processes[i[0]] = i[0] + '\nBLOCKED'
                GUI.draw_plot(G, dict_processes, dict_resources)

        #release resource conditions if found in instructions
        else:
            #delete line from r to p
            resource_state[i[2]] = 0
            G.remove_edge(i[2], i[0])
            print('resource ' + i[2] + ' has been released\n')

            for j in G.edges:
                if i[2] in j:
                    G.add_edge(j[1],j[0])
                    G.remove_edge(j[0], j[1])
                    dict_processes[j[0]] = j[0]
                    resource_state[j[1]] = 1
                    process_state[j[0]] = 0
                    print('process ' + j[0] + ' is now unblocked and owns ' + j[1] + '\n')
                    break

            GUI.draw_plot(G, dict_processes, dict_resources)

    #print("g edges = ", G.edges)

read_instructions(instructions)
