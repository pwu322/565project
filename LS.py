import re
from collections import defaultdict

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
		self.schd_time = 0       #schedule time after LS for each node
		self.slacks = -1         #slacks used in List scheduling algorithm

class FU:
	def __init__(self,type):
		self.type = type
		self.spower = 0.0
		self.dpower = 0
		self.delay = 0
		self.constraint = 4      #resource constraints for each FU

ops = {}                         #dictionary of nodes, key is id, node is content
resources  = []                  #list of FU types

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
	   ops[id] = op
	
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
	(ops[parent].child).append(ops[child])  #parent nodes' child list update
	(ops[child].parent).append(ops[parent]) #update nodes' parent list

# DEBUG
for n in ops.values():
	s = 'id: '+ str(n.id)+', type: '+str(n.type)+', type delay: '+str(resources[n.type].delay)
	print(s)


#--------------------------------------here comes List Scheduling algorithm---------------------------------------------------


#calculate upperbound of altency constraint
lamda = 0                                                         #initialize upperbound latency to 0 first
for i in ops.values():
	lamda += resources[i.type].delay 

queue = []                                                       #BFS queue, BFS bottom up
def ALAP(ops_list):
	for i in ops_list.values():                                  #traverse of all the nodes in input                                     
		if not i.child:                                           # if the node has no children
			i.alap = lamda + 1 - resources[i.type].delay          #calculate alap to all the leaves of the graph
			#print("node" + str(i.id) + "   alap: "+ str(i.alap) )
			queue.extend(i.parent)
	while queue: 
		op =  queue.pop(0)
		children_alap = []                                        
		for j in  op.child:                                        #store ALAP time of all children belong to i  in a list
			children_alap.append(j.alap)                          
		if 0 in children_alap:                                     #if the children's alap is not computed yet, put it back in the queue
			queue.append(op)
		else:
			op.alap = min(children_alap) -  resources[op.type].delay  #update nodes' ALAP time based on 
			queue.extend(op.parent)                                   #put node's parents in the queue
			#print("node" + str(op.id) + "   alap: "+ str(op.alap) )                            

ALAP(ops)                                                            #pdate the ALAP time of the node dictionary

#to make the calcuation easier, add an dummy node to the bottom of the graph which connects to all ouputnodes
dummy_node = node(-1)
ops[-1] = dummy_node
dummy_node.alap = lamda + 1

for i in ops.values():                                  #traverse of all the nodes in input                                     
	if not i.child and i.id != -1: 
		i.child.append(dummy_node)
		dummy_node.parent.append(i)   

def List_Scheduling(ops_list):
	cc = 1
	U = []                             	#list of available nodes of the type
	T = defaultdict(list)				#list of operations in progrees of the same type
	while dummy_node.schd_time == 0:
		for r in resources:                	#for each resource type
			U = []                                    #available operands(nodes) of current resource type, is a list of available-nodes-list of each type
			for op in ops_list.values():              # op is operands of certain type 
				parents_running = 0
				if op.type == r.type:                 #current type
					parent_schd = []                  #put node op's parent's chedule time in a list, then sort later
					for i in op.parent:
						if i.schd_time + resources[i.type].delay > cc:            #if the node's parents are still running then do not schedule
							parents_running = 1
						else: 	
							parent_schd.append(i.schd_time)
					#if the node doesn't have parent, or its parent not scheduled , and parent node is not already scheduled at curent cc, then add into U
					if ((not op.parent) or 0 not in parent_schd) and cc not in parent_schd and op.schd_time == 0 and parents_running == 0:  #if op are roots or it's parent already scheduled, then op is ready				
						U.append(op)                  #put "ready nodes" list of current type in U
						op.slacks = op.alap - cc      #compute slacks for nodes in U of current type
			U.sort(key = lambda x: x.slacks, reverse=False)               #sort U by its slack

			if T[r.type]:
				T[r.type] = [ op for op in T[r.type] if (cc - (op.schd_time + r.delay)) != 0]  #if the node finish running, then remove it from T
				# DEBUG
				# for op in T[r.type]:
				#	print("still running: "+str(op.id)+" at cc "+str(cc))

			to_be_scheduled = U[0:(r.constraint - len(T[r.type]))]                #pick the  A - T number of nodes that have smallest slacks in U
			for op in to_be_scheduled:                                            #schedule the nodes that are ready
				op.schd_time = cc
				#print("scheduled : "+str(op.id)+" at cc "+str(cc))
			T[r.type].extend(to_be_scheduled)                                     #T is the operands in process
		counter = 0
		for op in dummy_node.parent:                                              #dummy node is only scheduled when all parents are scheduled
			print("node" + str(op.id)+ "    delay :" +str(resources[op.type].delay))
			if op.schd_time != 0 and (op.schd_time + resources[op.type].delay <= cc): #cc = max(parent schedule time + parent delay) among all parents
				counter += 1			
		if counter == len(dummy_node.parent):
			dummy_node.schd_time = cc                                             #schedule dummy node at cc

		cc+=1

List_Scheduling(ops)
#DEBUG
#for i in ops.values():
	#print("node" + str(i.id) + "   alap: "+ str(i.alap) + "   number of children:" + str(len(i.child)) + "	schd time: " + str(i.schd_time) )   
