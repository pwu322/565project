import re
input = open('hal.txt')

def get_type(argument):
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


for line in input:
    newline = line.strip()
    if "label" in newline:
       type = get_type(newline[:3])
       id = int(re.search(r'\d+',newline).group())
       #print(type) 
       print(id)




#class node:
#    def __init__(self,id):
"""        self.id = id
    self.child = []
    self.parent = []
    self.asap = 0
    self.alap = 0
"""

