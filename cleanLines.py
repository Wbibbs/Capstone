# THIS SCRIPT CLEANS ALL DATA RETRIEVED FROM GOOGLE NLP TO BE USED IN getMaps.py
import os
inPath = "F:\\SmallSetTest\\split\\data\\frontupout\\"
outPath = "F:\\SmallSetTest\\split\\data\\frontupoutcleaned\\"

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


for filename in os.listdir(inPath):
	with open(inPath + filename, "r+") as file:
		lastline = ''
		with open(outPath + filename, "w+") as out:
			#for line in file.readlines():
		
			for line in file:
				#currpos = file.tell()
				if 'type:' in line:
					try: # Get next line to see if it contains object information
						nextline = next(file)
					
						if 'type:' in nextline: # If object information is in the next line, write the next line and skip current line
							out.writelines(nextline)
							#file.seek(currpos)
						else:
							out.writelines(line)
							out.writelines(nextline)
					except Exception as e:
						print(e)
				else:
					out.writelines(line)
			#for line in file:
				#if 'OTHER' in line or 'LOCATION' in line or 'WORK_OF_ART' in line or 'CONSUMER_GOOD' in line:
					#if 'type' in lastline.lower():
					#	#print('type in ',line)
					#	pass
				#	else:
			#			out.writelines(line)
			#	else:
				#	out.writelines(line)
			#	lastline = line