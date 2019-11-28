import re
import string
import os
from os import listdir

Input_dir = "/Users/pwu27/Desktop/MR_LCS/Input_Files/DFG_Files"
Resource_result_dir = "/Users/pwu27/Desktop/Fall"

input_files = [f for f in listdir(Input_dir) if f.endswith(".txt")]
res_consts_files = [f for f in listdir(Resource_result_dir ) if f.endswith(".txt") ]

write = {}
for f in input_files:
    i = 0
    f_name = re.sub('.txt', '', f)                #file name without.txt
    for res in res_consts_files:
        if f_name not in res:                     # 2 files are different
            i += 1
        else:
            break
    if(i != len(res_consts_files)):               #input file name match the resource result file
        print(res_consts_files[i]) 
        print(f)
        #get resource constrints from the resource files
        os.chdir(Resource_result_dir)                          #go to directory
        txt_res = open(res_consts_files[i],'r')                #read the files
        for line in txt_res:
            newline = line.strip()
            if "Function" in newline:
                idx = list(map(int,re.findall(r'\d+',newline)))
                write[idx[0]] = idx[1]
        txt_res.close()                                         # close the file
        #DEBUG
        for i in write.keys():
            print("for type " + str(i)+ " resource constraint is: "+ str(write[i]))
        #write the resource constraints to the input files
        os.chdir(Input_dir)
        txt_files = open(f,"a")                                #import the input file
        txt_files.write("for type " + str(i)+ " resource constraint is: "+ str(write[i]))  # python will convert \n to os.linesep
        txt_files.close()                                      # close the file
    else:
        print ("not found " )#+ str(f))  


# for res in res_consts_files:
#     i = 0
#     for f in input_files:
#         f_name = re.sub('.txt', '', f)
#         if f_name in res:
#             i = 1
#     if(i ):
#         print("found")
#     else:
#         print ("not found " + str(res))  
        
        
print(len(input_files))    
    #txtfiles = open('f')  #import the input file
