# This script takes entity data and calculates the word distances between them, determining
# if they are related. An association matrix is generated, which can be visualized as a graph
# to showcase relatedness

from itertools import islice
import numpy as np
import scipy.sparse as sp
import statistics
import os
#inFile = open(r"C:\Users\X\Desktop\outText.txt", 'r+')
#infile = open("F:\\SmallSetTest\\split\\data\\frontup\\Classic Myths___Mary Catherine Judd___February 2006___2..dat", 'r+')

indirectory = "F:\\SmallSetTest\\split\\data\\frontupoutcleaned\\"
outdirectory = "F:\\SmallSetTest\\split\\data\\frontupoutcleanedout\\"

types_of_words = ['PROPER', 'PERSON'] # List of words sought after, e.x. proper nouns and person entities for finding all people

bigger_master_dict = dict()

got_match = False
got_content = False
content = ''

list_of_texts = []

for filename in os.listdir(indirectory):
	list_of_texts.append(filename)

# This try except loop counts occurences and distances between given entities. It works, but all numbers are inflated by how many iterations it has. Need to fix this to get more accurate results, or divide by inflation factor
try:
	#with open(r"C:\Users\X\Desktop\outText.txt", 'r+') as inFile:
	for filename in list_of_texts:
		master_dict = dict()
		for line in open(indirectory + filename).readlines():
			if (line[6:len(line) - 1] not in types_of_words):
				if got_match:
					if got_content:
						if content in master_dict: # Check if entity is in dictionary, if yes append to current list
							master_dict[content].append([line[14:len(line) - 1]])
						else: # If not in dictionary, create new entity and set first entry
							#master_dict[content] = [str(line[14:len(line) - 1])]
							master_dict[content] = [str(line[14:len(line) - 1])]
						got_content = False
						got_match = False
					else:
						content = line[10:len(line) - 2].lower()
						got_content = True
				else:
					pass
			else:
				got_match = True
		bigger_master_dict[filename] = master_dict			
		

except StopIteration:
	pass

########################### OLD CODE ###########################
#try:
	#with open(r"C:\Users\X\Desktop\outText.txt", 'r+') as inFile:
	#with infile as inFile:
	#	for line in inFile.readlines():
		#	print(line)
		#	if (line[6:len(line) - 1] not in types_of_words):
		#		if got_match:
		#			if got_content:
		#				if content in master_dict: # Check if entity is in dictionary, if yes append to current list
		#					master_dict[content].append([line[14:len(line) - 1]])
		#				else: # If not in dictionary, create new entity and set first entry
		#					#master_dict[content] = [str(line[14:len(line) - 1])]
				#			master_dict[content] = [str(line[14:len(line) - 1])]
				#		got_content = False
				#		got_match = False
			#		else:
				#		content = line[10:len(line) - 2].lower()
			#			got_content = True
			#	else:
			#		pass
			#else:
			#	got_match = True
				
#except StopIteration:
	#pass
########################### OLD CODE ###########################

# Loop to calculate graph data for all entries in bigger_master_dict
	
	
matrixSize = 0
list_of_keys = []

for key, value in master_dict.items():
	#print (key, value)
	matrixSize += 1
	list_of_keys.append(key)

#print(matrixSize)
#print(list_of_keys)
position = 0 # Check where you are in the current index list

matched_dict = dict()		
offset_check = 4500	

num_of_nouns = 0
edges = dict()
#print(list_of_keys)

for key in list_of_keys:
	num_of_nouns += 1
	for item in master_dict[key]:

		if key not in edges: # -- produces small edge counts
			edges[key] =  [item]
		else:
			edges[key].append(item)
		
		for key2 in list_of_keys:
			for item2 in master_dict[key2]:
			
				#if key not in edges: # -- produces large edge counts
					#edges[key] =  [item]
				#else:
					#edges[key].append(item)
			
				#print(item)
				if int(str(item).strip("['']")) > int(str(item2).strip("['']")):
					if int(str(item).strip("['']")) - int(str(item2).strip("['']")) <= offset_check:
						in_string = str(key + '\t' + key2)
						if in_string not in matched_dict:
							matched_dict[in_string] = 1
						else:
							matched_dict[in_string] = matched_dict[in_string] + 1
				else:
					if int(str(item2).strip("['']")) - int(str(item).strip("['']")) <= offset_check:
						matched_dict[str(key + '\t' + key2)] = 1
						in_string = str(key + '\t' + key2)
						if in_string not in matched_dict:
							matched_dict[in_string] = 1
						else:
							matched_dict[in_string] = matched_dict[in_string] + 1
		
#print(matched_dict)

for key in edges:
	num_of_edges = 0
	for edge in edges[key]:
		num_of_edges += 1
	edges[key] = num_of_edges

max_edges = 0
min_edges = 0
avg_edges = 0
first_run = True
all_edges = [] #numeric value of edges

for key in edges:
	if first_run:
		max_edges = edges[key]
		min_edges = edges[key]
		avg_edges = edges[key]
		first_run = False
	else:
		if edges[key] > max_edges:
			max_edges = edges[key]
		if edges[key] < min_edges:
			min_edges = edges[key]
		all_edges.append(edges[key])
		
count = 0
total = 0
for num in all_edges:
	total += num
	count += 1

avg_edges = total / count

condensed_dict = dict()

#for key in matched_dict:
	#print(key, '\t', matched_dict[key])

outFile = open(r"C:\Users\X\Desktop\outDict.txt", 'r+')

#for key in matched_dict:
	#outFile.write(str(key + '\t' + matched_dict[key] + '\n'))

with open(r"C:\Users\X\Desktop\outFinished.txt", 'w+') as outFile:
	for key in matched_dict:
		outLine = str(str(key) + '\t' + str(matched_dict[key]) + '\n')
		outFile.write(outLine)

unique_edges = 0
with open(r"C:\Users\X\Desktop\outFinished.txt", 'r+') as inFile:
	for line in inFile:
		unique_edges += 1

standard_deviation = 0

standard_deviation = statistics.pstdev(all_edges)
	
print('MAX: ',max_edges,'\nMIN: ',min_edges,'\nAVG: ',avg_edges,'\nUNIQUE: ',unique_edges,'\nSTD DEV: ',standard_deviation)

#print(edges)
#matrix = numpy.zeroes((matrixSize, matrixSize))

#for i,j in d.itervalues(): 
    #matrix[i-1,j-1] = 1
    #matrix[j-1,i-1] = 1



with open(r'C:\Users\X\Desktop\outDict.txt', 'w+') as a:
	a.writelines(master_dict)
	
# TODO: Add dynamic weights to offset_check to have stronger or weaker associations -- may work, may not. Need to check relation or strength for entire paragraph
offset_check = 4500 # Number of characters to check relation between entitie. Any entity at or less than offset_check distance is considered related, and incremented accordingly in an association matrix

#for key in master_dict:
	#for num in master_dict[key]:
		