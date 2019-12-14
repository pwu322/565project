#generate stats.csv for all the inputs

import csv
import os
from os import listdir
from os import path

parameter_resource_constraint = ['0.01','0.05','0.1','0.2','0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']

# #stats.csv is for all the input, check if the file exist. If it is existed, delete it
# if path.exists("stats.csv"):
#     os.remove('stats.csv')


for para in parameter_resource_constraint:
    Output_dir = 'Output/'+ str(para) + '/'
    output_files = [f for f in listdir(Output_dir) if f.endswith(".csv")]


    file_name = ["file name"]
    ASAP = ["ASAP"]
    ALAP = ["ALAP"]
    latency_without_REST = ["latency without REST"]
    latency_with_REST = ["latency with REST"]
    energy_without_REST = ["energy without REST"]
    energy_delay_product_with_REST = ["energy delay product with REST"]
    energy_delay_product_without_REST = ["energy delay product without REST"]
    energy_with_REST = ["energy with REST"]


    j = 0
    while j < len(output_files):
        with open(Output_dir + output_files[j] ,'rt') as f:
            csvfile = csv.reader(f)
            i = 0
            for line in csvfile:
                i += 1
                if i == 1:
                    file_name.append(line[0])
                if i == 3:
                    ASAP.append(line[-1])
                if i == 4:
                    ALAP.append(line[-1])
                if i == 7:
                    latency_without_REST.append(line[-1])
                if i == 10:
                    latency_with_REST.append(line[-1])
                if i == 8:
                    energy_without_REST.append(line[-1])
                if i == 11:
                    energy_with_REST.append(line[-1])
                if i == 9:
                    energy_delay_product_without_REST.append(line[-1])
                if i == 12:
                    energy_delay_product_with_REST.append(line[-1])
        j += 1
    
    header = [para]
    with open('stats.csv', 'a+') as f:
        csv_writer = csv.writer(f, delimiter=',',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(header)

    with open('stats.csv', 'a+') as f:
        csv_writer = csv.writer(f, delimiter=',',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(file_name)
        csv_writer.writerow(ASAP)
        csv_writer.writerow(latency_with_REST)
        csv_writer.writerow(latency_without_REST)
        csv_writer.writerow(ALAP)
        csv_writer.writerow(energy_without_REST)
        csv_writer.writerow(energy_delay_product_without_REST)
        csv_writer.writerow(energy_with_REST)
        csv_writer.writerow(energy_delay_product_with_REST)


print(*file_name)
print(*ASAP)
print(*ALAP)
print(*latency_without_REST)
print(*latency_with_REST)
        
#stats.csv is for all the input, check if the file exist
# if not path.exists("stats.csv"):
#     header = [parameter_resource_constraint[0]]
#     with open('stats.csv', 'w') as f:
#         csv_writer = csv.writer(f, delimiter=',',
#             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         csv_writer.writerow(header)
# else:
#     with open('stats.csv', 'a+') as f:
#         csv_writer = csv.writer(f, delimiter=',',
#         quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         csv_writer.writerow(file_name)
#         csv_writer.writerow(ASAP)
#         csv_writer.writerow(latency_with_REST)
#         csv_writer.writerow(latency_without_REST)
#         csv_writer.writerow(ALAP)



