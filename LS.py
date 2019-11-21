import re
input = open('collapse_pyr_dfg__113.txt')  #import the input file
para = open('para_new.txt')

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
        self.type = -1

class FU:
    def __init__(self,type):
        self.type = type
        self.spower = 0.0
        self.dpower = 0
        self.delay = 0
        self.constraint = 10

ops = []  ## list of nodes
resources  = []  ##list of FU types

# read the FUs description from para_new.txt and create resouces list

for line in para:
	newline = line.strip()
	if "type" in newline:
		idx = list(map(int,re.findall(r'\d+',newline)))
		type = idx[0]
		res = FU(type)		 									# create FU and assign type
		resources.append(res) 									# append FU to resource list
	elif "spower" in newline:
		type = int(re.search(r'\d+',newline).group())
		spower = float(re.search(r'\d+.\d+', newline).group())	# get spower from para file
		resources[type].spower = spower							# assign spower to FU in resource list
	elif "dpower" in newline:
		idx = list(map(int,re.findall(r'\d+',newline)))
		type = idx[0]							
		dpower = idx[1]											# get dpower from para file				
		resources[type].dpower = dpower							# assign dpower to FU in resource list
	elif "delay" in newline:
		idx = list(map(int,re.findall(r'\d+',newline)))
		type = idx[0]
		delay = idx[1]											# get delay from para file
		resources[type].delay = delay							# assign delay to FU in resource list	

# DEBUG
#for r in resources:
#	s = 'Type: '+ str(r.type)+', dpower: '+str(r.dpower)+', spower: '+str(r.spower)+', delay: '+str(r.delay)
#	print(s)

# read the nodes from the input file and create list of nodes
for line in input:
    newline = line.strip()
    if "label" in newline:
       restype = get_type(newline[:3])
       id = int(re.search(r'\d+',newline).group())
       op  = node(id)											# create node and assign its id
       op.type = restype										# assign node type
       ops.append(op)											# append node to list of nodes
    
input.seek(0) #read the file again by reset the read

depend = []
# read the dependencies from the input file and assign children and parents to each node
for line in input:
    newline = line.strip()
    if "->" in newline:
        indexes = list(map(int,re.findall(r'\d+',newline)))     #get all the integers from newline
        depend.append(indexes)									# assign list of indexes read from input file to dependencies list

# assign children and parents to each node by reading from the dependency list
for i in depend:  ## i is each depency line
    parent = i[0]   #parent number
    child = i[1]
    (ops[parent-1].child).append(ops[child-1])  #parent nodes' child list update
    (ops[child-1].parent).append(ops[parent-1]) #update nodes' parent list

# DEBUG
for n in ops:
	s = 'id: '+ str(n.id)+', type: '+str(n.type)+', type delay: '+str(resources[n.type].delay)
	print(s)


######------------here comes List Scheduling algorithm--------------------------------

#to make the calcuation easier, add an dummy node to the bottom of the graph which connects to all ouputnodes
dummy_node = node(0)
#ops.append(dummy_node)

#calculate upperbound of altency constraint
lamda = 0                                                         #initialize upperbound latency to 0 first
for i in ops:
    lamda += resources[i.type].delay 

queue = []
def ALAP(ops_list):
    for i in reversed(ops_list):                                  #bottom up                                      
        if not i.child:                                           # if the node has no children
            i.alap = lamda + 1 - resources[i.type].delay
            print("node" + str(i.id) + "   alap: "+ str(i.alap) )
            queue.extend(i.parent)
    while queue: 
        op =  queue.pop(0)
        children_alap = []                                        
        for j in  op.child:                                        #store ALAP time of all children belong to i  in a list
            children_alap.append(j.alap)                              #bottom up
        op.alap = min(children_alap) -  resources[op.type].delay
        queue.extend(op.parent)
        print("node" + str(op.id) + "   alap: "+ str(op.alap) )                            

"""
def ALAP(ops_list):
    for i in reversed(ops_list):                                  #bottom up
        children_alap = []                                        
        if not i.child:                                           # if the node has no children
            i.alap = lamda + 1 - resources[i.type].delay
            #print("node" + str(i.id) + "   alap: "+ str(i.alap) )
        else: 
            for j in  i.child:                                        #store ALAP time of all children belong to i  in a list
                children_alap.append(j.alap)
            if not 0 in children_alap:                                #if all the children of i are scheduled 
                i.alap = min(children_alap) -  resources[i.type].delay #calculate i's ALAP   
 #       print("node" + str(i.id) + "   alap: "+ str(i.alap) )
 #       print(*children_alap)  
                                      
"""
ALAP(ops)
#for i in ops:
    #print("node" + str(i.id) + "   alap: "+ str(i.alap) + "   number of children:" + str(len(i.child))  )     