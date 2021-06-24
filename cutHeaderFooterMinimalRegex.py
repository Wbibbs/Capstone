import re
import os
import time
import pandas as pd

texts = []
input_path = "C:\\Users\\X\Desktop\\testdata\\"
output_path = "C:\\Users\\X\\Desktop\\outputdata\\"
start_time = time.time() * 1000

#List to hold all processed texts in title___author___date format
processed_texts = []

#Read in all filenames
#for file in os.listdir(input_path):
	#texts.append(file)

#Read in only X number of files
X = 2
for file in os.listdir(input_path):
	#if X == 0:
		#break
	#else:
	texts.append(file)

#Loop to read all texts, and cut header/footer and find author,title and release date
for text in texts:
	#Define text variable to be used and overwritten
	full_text = ''
	num_of_lines = 0
	#Open and read file
	with open(str(input_path + text), 'r+', encoding='utf8') as t:
		for line in t:
			full_text += line
			num_of_lines += 0
			
	#Read first N lines
	start_lines = 25
	head = ''
	
	with open(str(input_path + text)) as t:
		head = [next(t) for x in range(start_lines)]
		
	#Convert from list to string
	converted_head = ''
	for line in head:
		converted_head += line
	

	#Find title, author and release date
	title = re.search(r'^Title: .*?\n', full_text, re.MULTILINE)
	author = re.search(r'^Author: .*?\n', full_text, re.MULTILINE)
	release = re.search(r'^Release Date: .*?\n', full_text, re.MULTILINE)

	if title:
		title = title.group(0)[7::]
		title = title.replace('\n', '')

	if author:
		author = author.group(0)[8::]
		author = author.replace('\n', '')

	if release:
		release = release.group(0)[14::]
		release = release.replace('\n', '')
		release = re.sub('\[.*\]', '', release)
		release = release.replace(',', '')
	
	file_name = title + '___' + author + '___' +  release
	
	#Add file to processed_texts list
	processed_texts.append(file_name)
	
	#Replace newline characters and remove footer and header
	#full_text = full_text.replace("\n", '')
	#full_text = re.sub(r'.*?START OF THIS PROJECT GUTENBERG EBOOK', ' ', full_text)
	#full_text = re.sub(r'END OF THIS PROJECT GUTENBERG EBOOK .*?', ' ', full_text)
	
	#Write to file with file_name
	output_file = output_path + str(file_name) + '.txt'
	
	footer = 365
	
	num_lines = 0
	with open(str(input_path + text), 'r+', encoding='utf8') as t:
		num_lines = t.readlines()
		
	with open(output_file, 'w+', encoding='utf8') as out:
		out.writelines(num_lines[25:-footer])
	
	#out = open(output_file, 'w+', encoding='utf8')
	#out.write(full_text)
	#out.close()

end_time = time.time() * 1000

#Divide by 1000 for seconds and divide by 60 for minutes
time = ((end_time - start_time) / 1000) / 60

output_path += 'listoftexts.txt'

out = open(output_path, 'w+', encoding='utf8')
for text in processed_texts:
	out.write(text + '\n')
out.write('\n\n\n\nTIME TO PROCESS ' + str(len(processed_texts)) + ' TEXTS: ' + str(time) + ' minutes')

