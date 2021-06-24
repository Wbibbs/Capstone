import re
import os
import time


texts = []
input_path = "C:\\Users\\Wingwong\Desktop\\testdata\\"
output_path = "C:\\Users\\Wingwong\\Desktop\\outputdata\\"
start_time = time.time() * 1000

#List to hold all processed texts in title___author___date format
processed_texts = []

#Read in all filenames
#for file in os.listdir(input_path):
	#texts.append(file)

#Read in only X+1 number of files
X = 4
for file in os.listdir(input_path):
	if X == 0:
		break
	else:
		texts.append(file)

#Loop to read all texts, and cut header/footer and find author,title and release date
for text in texts:
	#Define text variable to be used and overwritten
	full_text = ''
	
	#Open and read file
	with open(str(input_path + text), 'r+', encoding='utf8', errors="surrogateescape") as t:
		for line in t:
			full_text += line

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
	full_text = full_text.replace("\n", '')
	full_text = re.sub(r'.*?START OF THIS PROJECT GUTENBERG EBOOK', ' ', full_text)
	full_text = re.sub(r'End of the Project Gutenberg EBook.*?', ' ', full_text)
	
	#Write to file with file_name
	output_file = output_path + str(file_name) + '.txt'
	out = open(output_file, 'w+', encoding='utf8', errors="surrogateescape")
	out.write(full_text)
	out.close()

end_time = time.time() * 1000

#Divide by 1000 for seconds and divide by 60 for minutes
time = ((end_time - start_time) / 1000) / 60

output_path += 'listoftexts.txt'

out = open(output_path, 'w+', encoding='utf8', errors="surrogateescape")
for text in processed_texts:
	out.write(text + '\n')
out.write('\n\n\n\nTIME TO PROCESS ' + str(len(processed_texts)) + ' TEXTS: ' + str(time) + ' minutes')

