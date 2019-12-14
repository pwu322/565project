import LS_extend
from LS_extend import ops, file1, resources, metric_selection   #import LS.py from the same folder, viarables
import os.path
from os import path
import csv                               #use csv as output
                                    
if not os.path.exists('Output_Extended/'):        #generate an output folder       
    os.mkdir('Output_Extended/')

dirName = 'Output_Extended/'+ str(metric_selection) 
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
result_schtime = ["schd_time"]
result_energy = ["total energy"]
result_energy_delay_product = ["energy delay product"]

#run list scheduling algorithm without REST
LS_extend.List_Scheduling(ops,metric_selection)            #without REST
dp = LS_extend.DP(ops, ops[-1].schd_time)
lp = LS_extend.LP(ops, ops[-1].schd_time)
total_energy = dp + lp
result_energy.append(total_energy)        #append the energy for each graph
result_energy_delay_product.append(total_energy*ops[-1].schd_time)    

#update values for each list
for op in ops.values():
    result_nodes.append(op.id)
    result_asap.append(op.asap)
    result_alap.append(op.alap)
    result_REST.append(op.rest)
    result_E_REST.append(op.e_rest)
    result_schtime.append(op.schd_time) 
    
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
    csv_writer.writerow(result_schtime)
    csv_writer.writerow(result_energy)
    csv_writer.writerow(result_energy_delay_product)