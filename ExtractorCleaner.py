import re
import os
import time
#import pandas as pd

texts = []
input_path = "F:\\MasterTextFolder\\"
output_path = "F:\\nov5\\"
start_time = time.time() * 1000
duplicates = 0
#Function called when finished with processing, reached either after end of folder filers or after encountering error
#Need to figure out how to handle error without stopping reading
def writeOut(error, file = None):
    #Python isn't playing nice with accessing global time, reimported here
	import time
	global output_path
	global processed_texts
	global start_time
	global duplicates
	end_time = time.time() * 1000

	#Divide by 1000 for seconds and divide by 60 for minutes
	time = ((end_time - start_time) / 1000) / 60

	output_path += 'listoftexts.txt'

	out = open(output_path, 'w+', encoding='utf8', errors='ignore')
	
    
    #Writing error gets last text file, need to find which file to pass instead of last one
	if error:
		out.write('ERROR ENCOUNTERED WHILE PROCESSING TEXTS -- ' + file + '\n\n')
		print('Done with errors')
	
	for text in processed_texts:
		out.write(text + '\n')
        
    #Write process time to overall lit of texts
	out.write('\n\n\n\nTIME TO PROCESS ' + str(len(processed_texts)) + ' TEXTS: ' + str(time) + ' minutes')
	out.write('\nNUMBER OF DUPLICATES: ' + str(duplicates))
	out.write('\nTOTAL NUMBER OF FILES PROCESSED: ' + str(len(processed_texts) + duplicates))




#List to hold all processed texts in title___author___date format
processed_texts = []

#Read in all filenames
#for file in os.listdir(input_path):
	#texts.append(file)

try:
    #Read in all filenames
	for file in os.listdir(input_path):
		texts.append(file)

	#Loop to read all texts, and cut header/footer and find author, title and release date
	for text in texts:
		#Define text variable to be used and overwritten
		full_text = ''
		num_of_lines = 0
        
		#Open and read file
		with open(str(input_path + text), 'r+', encoding='utf8', errors='ignore') as t:
			for line in t:
				full_text += line
				num_of_lines += 0
			
		#Read first start_lines lines and define blank head string to append
		start_lines = 25
		head = ''
	
        #Read up to start_lines and append to head as list
		with open(str(input_path + text), errors='ignore') as t:
			head = [next(t) for x in range(start_lines)]
		
		#Convert from list to string
		converted_head = ''
		for line in head:
			converted_head += line
	

		#Find title, author and release date
		title = re.search(r'^Title: .*?\n', converted_head, re.MULTILINE)
		author = re.search(r'^Author: .*?\n', converted_head, re.MULTILINE)
		release = re.search(r'^Release Date: .*?\n', converted_head, re.MULTILINE)

		if title:
			title = title.group(0)[7::]
			title = title.replace('\n', '')
		else:
			title = 'None'

		if author:
			author = author.group(0)[8::]
			author = author.replace('\n', '')
		else:
			author = 'None'
            
		if release:
			release = release.group(0)[14::]
			release = release.replace('\n', '')
			release = re.sub('\[.*\]', '', release)
			release = release.replace(',', '')
		else:
			release = 'None'
			
		#Remove special characters which might cause file name issues
		disallowed_chars = ['/','\\',':','?','"','<','>','|', '.', '!', '\'', '*', '(', ')', '[', ']']
        
		#This method removes disallowed_chars
		title = ''.join(e for e in title if e not in disallowed_chars)
		author = ''.join(e for e in author if e not in disallowed_chars)
		release = ''.join(e for e in release if e not in disallowed_chars)
		
		#This method removes all special characters, including spaces
		#title = ''.join(e for e in title if e.isalnum())
		#author = ''.join(e for e in author if e.isalnum())
		#release = ''.join(e for e in release if e.isalnum())
	
		file_name = title + '___' + author + '___' +  release
        
        #Check to see if file_name is larger than 250. If yes, cut title to 100 chars
		if (len(file_name) > 250):
			file_name = title[:100] + '___' + author + '___' +  release
        
        #If file_name still larger than 250, force title and author to 100 chars, plus release date
		if (len(file_name) > 250):
			file_name = title[:100] + '___' + author[:100] + '___' +  release
        
		#Add file to processed_texts list
		if file_name not in processed_texts:
			processed_texts.append(file_name)
		else:
			duplicates += 1
	
		#Replace newline characters and remove footer and header
		#full_text = full_text.replace("\n", '')
		#full_text = re.sub(r'.*?START OF THIS PROJECT GUTENBERG EBOOK', ' ', full_text)
		#full_text = re.sub(r'END OF THIS PROJECT GUTENBERG EBOOK .*?', ' ', full_text)
	
		#Write to file with file_name
		output_file = output_path + str(file_name) + '.txt'
	
		footer = 365
		num_lines = 0
        
        #Get number of liens from input text
		with open(str(input_path + text), 'r+', encoding='utf8', errors='ignore') as t:
			num_lines = t.readlines()
		
        #Write file with file_name, ignoring footer and start_lines
		with open(output_file, 'w+', encoding='utf8', errors='ignore') as out:
			out.writelines(num_lines[start_lines:-footer])
	
		#out = open(output_file, 'w+', encoding='utf8')
		#out.write(full_text)
		#out.close()

#Handle exception, write out files and exit script
except Exception as e:
	writeOut(True, file)
	print(e)
	exit()
writeOut(False)