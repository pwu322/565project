This is the ML_RCS algorithm with REST implimentation. Results are saved in the Output folder.

To run one benchmark:
    go to command line, and go to the directory of this folder
    Enter:   
        python3 LS.py number1 number2
    number1 ranges from 0 to total input size -1
    number2 is the resource constraint coefficent, could be 0.01,0.05,0.1,0.2,...,0.9,1
    For example: python3 LS.py 0 0.01 , 0 is the first input .txt to the LS algorithm, while 0.01 is the coeficcient to multiply the total resource constraints

To run all benchmarks:
    1.clear all the output informtion first:
    Enter:
        python3 LS.py clearall
    2.Set up permision on the sell script script.sh:
    Enter:
        chmod +x script.sh
    3.run all the benchmarks with a nmber2(resource constraint coefficent)
    Enter:
        ./script.sh number2

To get resource constraints if you want to run by yourself(****Notice this is not neccessary. The resource constraints are already added to each input DFG)
    Enter:
        python3 MRLCS.py number1


    