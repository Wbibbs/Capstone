#This program isolates only entity type, content and offset from the Google JSON file

import re
import os

#infile = open("F:\\SmallSetTest\\split\\data\\frontup\\Classic Myths___Mary Catherine Judd___February 2006___2..dat")
#in_data = infile.read()

#out = open("outCorrect.txt", 'w+')


#num = 0

file_names = []

directory = "F:\\SmallSetTest\\split\\data\\frontup\\"
out_directory = "F:\\SmallSetTest\\split\\data\\frontupout\\"

for file in os.listdir(directory):
#for file in open("F:\SmallSetTest\split\", 'w+'):

	if not os.path.isdir(file) or not file == "F:\\SmallSetTest\\split\\data\\frontup\\out\\":
		with open(directory + file, 'r+') as f:
			with open(out_directory + file, 'w+') as out:
				f = f.readlines()
				print('writing to ', str(out_directory + file))
				#print(out_directory + file)
				for line in f:
					#num += 1
					#if num == 25:
						#exit()
					line = line.strip('\n')
					#print(line.strip('\n') + " NEW LINE NEW LINE NEW LINE")
					#print(line)
					if ("content:" in line or 'begin_offset:' in line or 'type:' in line):
						out.write(line.strip() + '\n')
						#print('FOUND MATCH ' + line + '\n')
	else:
		print('Directory found, skipping')

