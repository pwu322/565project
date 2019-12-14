
#*********************************** checker for LS.py (ML_RCS) *****************************************
# This is checker file to check is list scheduling algorithm result satisfies the following requirement:
# 1. check if the scheduling time of each node is >= its parents' scheduling time + delay
# 2. check if the scheduling time + delay of each node is <= its children's scheduling time
# 3. check if the scheduling time of each node is between its ASAP and ALAP
# 4. for each clock cycle, check if the number of busy FUs is at most equal to the resource constraints


import MRLCS
from MRLCS import ops, file1, resources      #import LS.py from the same folder, viarables
import os.path
from os import path
import operator 
from collections import defaultdict

errors = []						# error logs list
dummy = 0						# dummy node

MRLCS.List_Scheduling(ops)

for op in ops.values():
	if op.id == -1:
		dummy = op 				# set the dummy node
	if op.parent:
		for i in op.parent:
			if op.schd_time < i.schd_time + resources[i.type].delay:			# check if the scheduling time of each node is >= its parents' scheduling time + delay
				errors.append("[ERROR]: precedence constraint not satisfied for node "+str(op.id)+": wrong scheduling with respect to parent nodes.")
	if op.child:
		for i in op.child:
			if op.schd_time + resources[op.type].delay > i.schd_time:			# check if the scheduling time + delay of each node is <= its children's scheduling time
				errors.append("[ERROR]: precedence constraint not satisfied for node "+str(op.id)+": wrong scheduling with respect to children nodes.")
	if op.schd_time > op.alap or op.schd_time < op.asap:						# check if the scheduling time of each node is between its ASAP and ALAP
		errors.append("[ERROR]: scheduling time of node "+str(op.id)+" not consistent with respect to its ALAP or ASAP time.")

T = defaultdict(list)

for cc in range(1, dummy.schd_time + 1):										# for each clock cycle, check if the number of busy FUs is at most equal to the resource constraints
	for r in resources:
		if T[r.type]:
			T[r.type] = [ op for op in T[r.type] if (cc - (op.schd_time + r.delay)) != 0] # remove op if op finishes running

		for op in ops.values():
			if op.type == r.type and op.schd_time == cc:                        # add op to T if it is scheduled
				T[r.type].append(op)

		if len(T[r.type]) > r.constraint:
			errors.append("[ERROR]: resource constraints not satisfied for resource type "+str(r.type)+" at cc "+str(cc)+".")

# eventually print all the error logs if present
if len(errors) == 0:
	print("List scheduling executed successfully: all constraints are satisfied.")
else: 
	print("List scheduling executed with errors: some constraints are not satisfied (see below):")
	for e in errors:
		print(e)