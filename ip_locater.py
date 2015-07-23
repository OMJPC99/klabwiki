import os
import re
import sys
import urllib


def locate(university):
	print 'University:',university
	reader = open('university_data/'+university.replace(' ', '_').replace('/', '_')+'.xml', 'r')
	scan = False
	latitude = ''
	longitude = ''
	for line in reader:
		line = line.lstrip()
		if 'location>' in line:
			scan = not scan
		if scan and '<lat>' in line:
			print line
			latitude = re.search(r"[-+]?\d*\.\d+|\d+", line).group()
		if scan and '<lng>' in line:
			print line
			longitude = re.search(r"[-+]?\d*\.\d+|\d+", line).group()
	return (longitude, latitude)


def file_locate(in_file_name, out_file_name):
	print 'Scanning %s...' % in_file_name
	reader = open(in_file_name, 'r')
	writer = open(out_file_name, 'w')
	writer.write('IP|LONGITUDE|LATITUDE|UNIVERSITY|USERNAME|TIME|JOURNAL_NAME|JOURNAL_YEAR|JOURNAL_PMID|JOURNAL_DOI|CITE_PMID|CITE_DOI|PAGE_ID\n')
	for line in reader:
		tokens = line.split('|')
		coords = locate(tokens[1])
		p_tokens = [tokens[0], coords[0], coords[1], tokens[1]] + tokens[4:]
		writer.write('|'.join(p_tokens))
	reader.close(); writer.close()

def directory_locate(in_directory, out_directory):
	os.system('mkdir ' + out_directory)
	for file_name in os.listdir(in_directory):
		file_locate(in_directory + file_name, out_directory + 'located_' + file_name)


directory_locate(sys.argv[1], sys.argv[2])
