import LS
from LS import ops, file1, resources, parameter_resource_constraint     #import LS.py from the same folder, viarables
import os.path
from os import path
import csv                               #use csv as output
                                    
if not os.path.exists('Output/'):        #generate an output folder       
    os.mkdir('Output/')

dirName = 'Output/'+ str(parameter_resource_constraint) 
if not os.path.exists(dirName):
    os.mkdir(dirName)                    #generate a folder inside output folder corresponding to parameter of resource constraint we use
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")


#initialize the list then output each list as one line
result_nodes = ["node ID"]
result_asap =["asap"]
result_alap = ["alap"]
result_REST = ["REST"]
result_E_REST = ["E_REST"]
result_schtime_no_rest = ["schd_time without rest"]
result_schtime_rest = ["schd_time with rest"]
result_energy = ["total energy without rest"]
result_energy_rest = ["total energy with rest"]

#run list scheduling algorithm without REST
LS.List_Scheduling(ops,False)            #without REST
dp = LS.DP(ops, ops[-1].schd_time)
lp = LS.LP(ops, ops[-1].schd_time)
total_power = dp + lp
result_energy.append(total_power)        #append the energy for each graph    

#update values for each list
for op in ops.values():
    result_nodes.append(op.id)
    result_asap.append(op.asap)
    result_alap.append(op.alap)
    result_REST.append(op.rest)
    result_E_REST.append(op.e_rest)
    result_schtime_no_rest.append(op.schd_time) 
      

#write files, create a .csv file with the same file name
result = file1.replace(".txt",".csv")        #file name is same except ends with .csv
with open(dirName + '/' + result, 'w') as f:       
    csv_writer = csv.writer(f, delimiter=',',
    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([file1])             #create a .csv file and write the txt file name on first row

#append each row to the existed .csv file
with open(dirName + '/' + result, 'a') as f:      #append the rest of information to .csv file
    csv_writer = csv.writer(f, delimiter=',',
    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(result_nodes)
    csv_writer.writerow(result_asap)
    csv_writer.writerow(result_alap)
    csv_writer.writerow(result_REST)
    csv_writer.writerow(result_E_REST)
    csv_writer.writerow(result_schtime_no_rest)
    csv_writer.writerow(result_energy)

#important: since python always update the mutable object(ops), we have to reset it before another List_Scheduling function call
for i in ops.values():
  i.schd_time = 0                           #reset schedule time to 0
     
#run list scheduling algorithm with REST
LS.List_Scheduling(ops,True)     #run the algorithm again with REST
dp = LS.DP(ops, ops[-1].schd_time)
lp = LS.LP(ops, ops[-1].schd_time)
total_power_rest = dp + lp
result_energy_rest.append(total_power_rest)

for op in ops.values():
    result_schtime_rest.append(op.schd_time)   #update the list for schedule time with rest

with open(dirName + '/' + result, 'a') as f:    
    csv_writer = csv.writer(f, delimiter=',',
    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(result_schtime_rest)   #append the sch time with rest of information to .csv file
    csv_writer.writerow(result_energy_rest)

# # DEBUG
# # print(result_schtime_no_rest)
# # print(result_schtime_rest)


