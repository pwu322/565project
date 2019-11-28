import re
from collections import defaultdict

input = open('Inputs/hal.txt')  #import the input file
para = open('Inputs/para_new.txt')

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
        self.distance = 0
        self.rest = -1
        self.e_rest = -1
        self.rfg_child = []
        self.rfg_parent = []

class FU:
    def __init__(self,type):
        self.type = type
        self.spower = 0.0
        self.dpower = 0
        self.delay = 0
        self.constraint = 1      #resource constraints for each FU

ops = {}                         #dictionary of nodes, key is id, node is content
resources  = []                  #list of FU types

#-------------------------files reading-------------------------------------

# read the FUs description from para_new.txt and create resouces list
for line in para:
    newline = line.strip()
    if "type" in newline:
        idx = list(map(int,re.findall(r'\d+',newline)))
        type = idx[0]
        res = FU(type)                                          # create FU and assign type
        resources.append(res)                                   # append FU to resource list
    elif "spower" in newline:
        type = int(re.search(r'\d+',newline).group())
        spower = float(re.search(r'\d+.\d+', newline).group())  # get spower from para file
        resources[type].spower = spower                         # assign spower to FU in resource list
    elif "dpower" in newline:
        idx = list(map(int,re.findall(r'\d+',newline)))
        type = idx[0]                           
        dpower = idx[1]                                         # get dpower from para file             
        resources[type].dpower = dpower                         # assign dpower to FU in resource list
    elif "delay" in newline:
        idx = list(map(int,re.findall(r'\d+',newline)))
        type = idx[0]
        delay = idx[1]                                          # get delay from para file
        resources[type].delay = delay                           # assign delay to FU in resource list   

# DEBUG
#for r in resources:
#   s = 'Type: '+ str(r.type)+', dpower: '+str(r.dpower)+', spower: '+str(r.spower)+', delay: '+str(r.delay)
#   print(s)


# read the nodes from the input file and create list of nodes
for line in input:
    newline = line.strip()
    if "label" in newline:
       restype = get_type(newline[:3])
       id = int(re.search(r'\d+',newline).group())
       op  = node(id)                                           # create node and assign its id
       op.type = restype                                        # assign node type
       ops[id] = op
    
input.seek(0) #read the file again by reset the read

depend = []
# read the dependencies from the input file and assign children and parents to each node
for line in input:
    newline = line.strip()
    if "->" in newline:
        indexes = list(map(int,re.findall(r'\d+',newline)))     #get all the integers from newline
        depend.append(indexes)                                  # assign list of indexes read from input file to dependencies list

# assign children and parents to each node by reading from the dependency list
for i in depend:  ## i is each depency line
    parent = i[0]   #parent number
    child = i[1]
    (ops[parent].child).append(ops[child])  #parent nodes' child list update
    (ops[child].parent).append(ops[parent]) #update nodes' parent list

# DEBUG
#for n in ops.values():
#    s = 'id: '+ str(n.id)+', type: '+str(n.type)+', type delay: '+str(resources[n.type].delay)
#    print(s)


#--------------------------------------here comes List Scheduling algorithm---------------------------------------------------


#calculate upperbound of altency constraint
lamda = 0                                                         #initialize upperbound latency to 0 first
for i in ops.values():
    lamda += resources[i.type].delay 


def ALAP(ops_list):
    queue = []                                                        #BFS queue, bottom upqueue = []
    for i in ops_list.values():                                   #traverse of all the nodes in input                                     
        if not i.child:                                           # if the node has no children
            i.alap = lamda + 1 - resources[i.type].delay          #calculate alap to all the leaves of the graph
            #print("node" + str(i.id) + "   alap: "+ str(i.alap) )
            queue.extend(i.parent)
    while queue: 
        op =  queue.pop(0)
        children_alap = []
        for j in  op.child:                                           #store ALAP time of all children belong to i  in a list
            children_alap.append(j.alap)                          
        if 0 in children_alap:                                        #if the children's alap is not computed yet, put it back in the queue
            queue.append(op)
        else:
            op.alap = min(children_alap) -  resources[op.type].delay  #update nodes' ALAP time based on 
            queue.extend(op.parent)                                   #put node's parents in the queue
            #print("node" + str(op.id) + "   alap: "+ str(op.alap) )                            

ALAP(ops)                                                             #update the ALAP time of the node dictionary

#calcuate distance of a node from the imaginary output node
def get_distance(ops_list):
    queue = []                                                        #BFS queue, bottom up
    for i in ops_list.values():                                   #traverse of all the nodes in input
        if not i.child:                                           # if the nodes are leaves of the graph
            i.distance = resources[i.type].delay                  #calculate distance of all the leaves of the graph
            #print("node" + str(i.id) + "   alap: "+ str(i.alap) )
            queue.extend(i.parent)                                #push the children of those nodes in the queue
    while queue: 
        op =  queue.pop(0)
        children_distance = []                                        
        for j in  op.child:                                                  #store distance of all children belong to i  in a list
            children_distance.append(j.distance)
        if 0 in children_distance:                                           #if the children's distance is not computed yet, put it back in the queue
            queue.append(op)
        else:
            op.distance = max(children_distance) + resources[op.type].delay  #otherwise, update nodes' distance  based on  max idstance + delay
            queue.extend(op.parent)                                          #put node's parents in the queue
            #print("node" + str(op.id) + "   alap: "+ str(op.alap) )                            

get_distance(ops)  

#########################################
def ASAP(ops_list):
    queue = []                                                         #BFS queue, top-down
    for i in ops_list.values():                                        #traverse of all the nodes in input                                     
        if not i.parent:                                               # if the node has no children
            i.asap = 1          #calculate asap to all the roots of the graph
            #print("node" + str(i.id) + "   asap: "+ str(i.asap) )
            queue.extend(i.child)
    while queue:
        op =  queue.pop(0)
        if op.asap == 0:
            parent_asap = []
            parent_finish = []                                             #list for speculative finish time of all parents
            for j in  op.parent:                                           #store ASAP time of all parent of i  in a list
                parent_asap.append(j.asap)                                             #
                parent_finish.append(resources[j.type].delay + j.asap)
                #print(*parent_finish)
            if 0 in parent_asap:                                           #if the parent's asap is not computed yet, put it back in the queue
                queue.append(op)
                #print("put  " + str(i.id) + " back")
            else:                
                op.asap = max(parent_finish)    #update nodes' ASAP time based on the latest finish time
                for i in op.child:
                    if i.asap == 0:
                        queue.append(i)                                    #put node's children in the queue
                #print("node" + str(op.id) + "   asap: "+ str(op.asap) )                            

ASAP(ops)

#-----------------------------------------REST algorithm --------------------------------- 

#to make the calcuation easier, add an dummy node to the bottom of the graph which connects to all ouputnodes
dummy_node = node(-1)
ops[-1] = dummy_node
dummy_node.alap = lamda + 1

for i in ops.values():                                  #connect dummy node to the graph                                     
    if not i.child and i.id != -1: 
        i.child.append(dummy_node)
        dummy_node.parent.append(i) 

levels = defaultdict(list)

# function to define the levels of the graph: 
#   each entry of the dictionary represent the level with its nodes
def get_levels(ops_list):
    k = 1
    for op in ops_list.values():                        # we start from level 1 adding all the input nodes in the graph
        if not op.parent:
            levels[k].append(op)

    while(levels[k]):                                   # when we get to the last level, since we are not adding the dummy node, we will get to an empty level
        k += 1                                          # we increment the level
        for op in levels[k-1]:                          # and for each element in the previous level, we add all its children to the new level
            for i in op.child:
                if i not in levels[k] and i.id != -1:   # for each child node, if the child is not already in the list of the specific level, add it (don't add dummy node)
                    levels[k].append(i)

get_levels(ops)

# DEBUG
# k = 1
# for oplist in levels.values():
#     if oplist:
#         print("level "+str(k)+": ")
#     for op in oplist:
#         print("- node: "+str(op.id))
#     k += 1

last_level = len(levels.values())                       # last level of the circuit graph (dummy node level)

visited = defaultdict(list)                             # dictionary where all the visited nodes (i.e. rest already computed) are divided by type

def REST(ops_list):

    k = 1
    for op in levels[k]:
        op.rest = 1
        visited[op.type].append(op)                     # for each resource type, we have a list of visited nodes in the dictionary, from which we can easily extract the eligible parent nodes in the dfg
        visited[op.type].sort(key = lambda x: x.rest, reverse=True) # sort the values by rest in descending order, so we can pick easily the ones with the highest rest

    k += 1
    while(k < last_level):                  # top bottom part of the algorithm: rest evaluation
        for op in levels[k]:
            filtered_visited = list(filter(lambda x: x.id != op.id, visited[op.type]))
            op.rfg_parent.extend(filtered_visited[0:resources[op.type].constraint]) # we pick a number of nodes with highest rest that is equal to the resource constraint and set them as parents of the given node
            
            # DEBUG
            # for i in op.rfg_parent:
            #     print("op.id: " + str(op.id) + "  PARENT ID: "+str(i.id))

            if not op.rfg_parent:
                op.rest = max(1, op.asap)   # if there are no parents in the rfg graph, we symbolically add a dummy node with rest = 1 and delay = 0, so the max is between 1 (1+0, only parent) and the asap time of the node
            else:
                for p in op.rfg_parent:     # we set op as child in the resource flow graph of its rfg parents
                    p.rfg_child.append(op)
                rest_plus_delay = []        # utility list that contains all the values of delay+rest of the rfg parents
                for i in op.rfg_parent:     
                    rest_plus_delay.append(i.rest + resources[i.type].delay)
                # DEBUG 
                # print("node: "+str(op.id)+"       min rest_plus_delay: "+str(min(rest_plus_delay))+"  asap: "+str(op.asap))
                op.rest = max(min(rest_plus_delay), op.asap)    # as defined in the algorithm, we select the max value among the minimum rest+delay of the parents and the node's asap
                op.e_rest = op.rest
        
        for op in levels[k]:
            if op not in visited[op.type]:  # if not present in the visited dictionary, we add the node to the list of the visited nodes of that type
                visited[op.type].append(op)
                visited[op.type].sort(key = lambda x: x.rest, reverse=True) # we sort again the values by rest in descending order

            # DEBUG
            # for i in visited[op.type]:
            #       print("VISITED OF TYPE: "+str(op.type)+" -> "+str(i.id)) 

        k += 1

    # DEBUG
    # for op in ops.values():
    #    print("node"+str(op.id)+"   rest: "+str(op.rest))

    k = last_level-1
    while(k >0):                           # bottom-up part of the algorithm: e-rest evaluation
        for op in levels[k]:
            for p in op.parent:
                e_rest_children = []        # utility list that contains all the values of delay-e_rest of the rfg children 
                
                for c in p.child:
                    e_rest_children.append(c.e_rest - resources[p.type].delay)        # ??????????????????????node 3 
                
                p.e_rest = max(min(e_rest_children), p.e_rest)
                if p.e_rest != p.rest:
                    diff = p.e_rest - p.rest    # save the difference between rest and e_rest to propagate it in the graph
                    #print("difference: "+str(diff))
                    #p.rest = p.e_rest           # and update the e_rest value of the node
                    parents_to_update = []      # list of parents to update
                    parents_to_update.extend(p.parent)  # initialized to the parents of the updated node
                    while(parents_to_update):   # until we reach the first level of the graph
                        i = parents_to_update.pop(0)    # we pop the first element from the list
                        i.e_rest += diff          # we update the rest value with the difference computed before
                        for j in i.parent:  # we visit all the parents in the resource flow graph and check if their rest was not updated to see if it needs to be updated
                            if j.e_rest == j.rest:
                                parents_to_update.append(j)

                #for op in ops.values():         # reset the e_rest values to be same as rest values in all the graph
                #    op.e_rest = op.rest
        k -= 1


REST(ops)

for op in ops.values():
    print("node"+str(op.id)+"   e-rest: "+str(op.e_rest))


#-----------------------------------------------------------------------------------------------

def List_Scheduling(ops_list):
    cc = 1
    U = []                              #list of available nodes of the type
    T = defaultdict(list)               #list of operations in progrees of the same type
    while dummy_node.schd_time == 0:
        for r in resources:                 #for each resource type
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

            # DEBUG
            # if U:
	           #  print("unsorted U:")
	           #  for i in U:
	           #  	print("node: "+str(i.id)+"	slack: "+str(i.slacks)+"	e_rest: "+str(i.e_rest))

			# sort U by its slack and e_rest: when two nodes have the same slack, they are sorted based on e-rest to break ties
            U.sort(key = lambda x: (x.slacks, x.e_rest), reverse=False)

            # DEBUG
            # if U:
	           #  print("sorted U:")
	           #  for i in U:
	           #  	print("node: "+str(i.id)+"	slack: "+str(i.slacks)+"	e_rest: "+str(i.e_rest))

            if T[r.type]:
                T[r.type] = [ op for op in T[r.type] if (cc - (op.schd_time + r.delay)) != 0]  #if the node finish running, then remove it from T
                # DEBUG
                # for op in T[r.type]:
                #   print("still running: "+str(op.id)+" at cc "+str(cc))

            to_be_scheduled = U[0:(r.constraint - len(T[r.type]))]                #pick the  A - T number of nodes that have smallest slacks in U
            for op in to_be_scheduled:                                            #schedule the nodes that are ready
                op.schd_time = cc
                #print("scheduled : "+str(op.id)+" at cc "+str(cc))
            T[r.type].extend(to_be_scheduled)                                     #T is the operands in process
        counter = 0
        for op in dummy_node.parent:                                              #dummy node is only scheduled when all parents are scheduled
            #print("node" + str(op.id)+ "    delay :" +str(resources[op.type].delay))
            if op.schd_time != 0 and (op.schd_time + resources[op.type].delay <= cc): #cc = max(parent schedule time + parent delay) among all parents
                counter += 1            
        if counter == len(dummy_node.parent):
            dummy_node.schd_time = cc                                             #schedule dummy node at cc

        cc+=1

List_Scheduling(ops)
#DEBUG
for i in ops.values():
    print("node" + str(i.id) + "   asap: "+ str(i.asap) + "   number of children:" + str(len(i.child)) + " schd time: " + str(i.schd_time) )  
    # 

#DEBUG
#for i in ops.values():
#   print("node" + str(i.id) + "   distance: "+ str(i.distance) + "   number of children:" + str(len(i.child)) + "  schd time: " + str(i.schd_time) )  
     

