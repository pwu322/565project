This is the ML_RCS algorithm with REST implimentation. Results are saved in the Output folder.

1.To run one benchmark:
    go to command line, and go to the directory of this folder
    Enter:   
        python3 LS.py number1 number2
    number1 represents which file to run, ranges from 0 to total input size -1
    number2 is the resource constraint coefficent, could be 0.01,0.05,0.1,0.2,...,0.9,1
    For example: python3 LS.py 0 0.01 , 0 is the first input .txt to the LS algorithm, while 0.01 is the coeficcient to multiply the total resource constraints

2.To run all benchmarks:
    --clear all the output information first:
    Enter:
        python3 LS.py clearall
    --Set up permission on the sell script script.sh:
    Enter:
        chmod +x script.sh
    --run all the benchmarks with different number2(resource constraint coefficient), repeat this step for all the coefficient needed
    Enter:
        ./script.sh number2

3.To get resource constraints if you want to run by yourself(****Notice this is not necessary. The resource constraints are already added to each input DFG)
    Enter:
        python3 MRLCS.py number1




*****************************************************************************************************************************
To run the extended algorithm, similar files are written. LS_extended added the selection metric to the existed list scheduling algorithm. It sorts the available nodes in U based on : slacks * metric + (1-metric) * e_rest, metric is from 0 to 1. When metric = 0, select base on e_rest. When metric = 1, select base on slacks


1.To run one benchmark:
    go to command line, and go to the directory of this folder
    Enter:   
        python3 LS_extended.py number1 number3
    number1 represents which file to run, ranges from 0 to total input size - 1
    number3 is the selection metric, ranging from 0 0.1 0.2 ... 1 (we keep resource constraint as a constant 0.5)
    For example: python3 LS.py 0 1 , 0 is the first input .txt to the extended LS algorithm. While 1 is the metric sorting the available nodes in U. Sort U base on slacks

2.To run all benchmarks:
    --clear all the output information first:
    Enter:
        python3 LS_extended.py clearall
    --Set up permission on the sell script script.sh:
    Enter:
        chmod +x script_extended.sh
    3.Run all the benchmarks with different number3(selection metric). Repeat this step for all the metric wanted.
    Enter:
        ./script_extended.sh number3



*******************************************************************************************************************************
Checker for the LS.py result (ML_RCS) 
---python3 checker.py number1 number2
number1 is the file, number2 is resource constraint parameters. number1 ranges from 0 to 14. number 2 ranges from 0.01 to 1. You can type in which file to check

Checker for the MRLCS.py result (MR_LCS) 
---python3 checker_MRLCS.py number 1 number2