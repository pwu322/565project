#generate stats.csv for all the inputs

import csv
import os
from os import listdir
from os import path

metric_selection = ['0.0','0.1','0.2','0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']

# #stats.csv is for all the input, check if the file exist. If it is existed, delete it
# if path.exists("stats.csv"):
#     os.remove('stats.csv')


for para in metric_selection:
    Output_dir = 'Output_Extended/'+ str(para) + '/'
    output_files = [f for f in listdir(Output_dir) if f.endswith(".csv")]

    file_name = ["file name"]
    ASAP = ["ASAP"]
    ALAP = ["ALAP"]
    latency = ["latency "] 
    energy = ["energy"]
    energy_delay_product = ["energy delay product"]
    

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
                    latency.append(line[-1])
                if i == 8:
                    energy.append(line[-1])
                if i == 9:
                    energy_delay_product.append(line[-1])
        j += 1
    
    header = [para]
    with open('stats_extended.csv', 'a+') as f:
        csv_writer = csv.writer(f, delimiter=',',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(header)

    with open('stats_extended.csv', 'a+') as f:
        csv_writer = csv.writer(f, delimiter=',',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(file_name)
        csv_writer.writerow(ASAP)
        csv_writer.writerow(latency)
        csv_writer.writerow(ALAP)
        csv_writer.writerow(energy)
        csv_writer.writerow(energy_delay_product)

print(*file_name)
print(*ASAP)
print(*ALAP)
print(*latency)
print(*energy_delay_product)