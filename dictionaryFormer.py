#This program processes data in the outCorrect file and puts entities into a list with all positions they occur

full_dict = {}

with open('outCorrect.txt') as file:
	itfile = iter(file)
	for line in itfile:
		#print(line)
		#print(line[:6])
		if "PERSON" in line[6:] or "PROPER" in line[6:]:
			print('MATCH' + line[6:])
			#continue
			#name = line.split("content: ")
			name = line[4:]
			print("NAME: " + name)
			#continue
			next(itfile)
			#offset = line.split("begin_offset: ")
			offset = line[14:]
			print('NAME: ' + name + ' - OFFSET: ' + offset)
			if name not in full_dict:
				full_dict[name] = [offset]
			else:
				full_dict[name] = [full_dict[name], offset]
				
print(full_dict.keys())