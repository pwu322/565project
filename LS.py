import re
input = open('hal.txt')  #import the input file

def get_type(argument): #input is string, output is type #
    switcher = {
        "ADD": 0,
        "AND": 1,
        "MUL": 2,
        "ASR": 3,
        "LSR": 4,
        "LOD": 5,
        "BNE": 6,
        "STR": 7,
        "SUB": 8,
        "NEG": 9,
        "DIV": 10,
    }
    return switcher.get(argument)


class node:
    def __init__(self,id):
        self.id = id
        self.child = []
        self.parent = []
        self.asap = 0
        self.alap = 0

ops = []  ## list of nodes
for line in input:
    newline = line.strip()
    if "label" in newline:
       type = get_type(newline[:3])
       id = int(re.search(r'\d+',newline).group())
       ops.append(node(id))
    
input.seek(0) #read the file again by reset the read

depend = []
for line in input:
    newline = line.strip()
    if "->" in newline:
        indexes = list(map(int,re.findall(r'\d+',newline)))
        depend.append(indexes)



for i in depend:  ## i is each depency line
    parent = i[0]   #parent number
    child = i[1]
    (ops[parent-1].child).append(ops[child-1])  #parent nodes' child list update
    (ops[child-1].parent).append(ops[parent-1]) #update nodes' parent list

for op in ops:
    for j in op.child:
        print(j.id)