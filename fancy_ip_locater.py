import os
import time
import urllib

API_KEY = 'AIzaSyDFH9bLWjpZPYqHdTqHMcG4igt5d66Qfeg'
universities = set()

for file_name in os.listdir('searched'):
	reader = open('searched/' + file_name, 'r')
	for line in reader:
		tokens = line.split('|')
		university = tokens[1]
		if university not in universities:
			universities.add(university)
			print university
	reader.close()

print 'Unique universities: %d' % len(universities)
index = 0
for university in universities:
	#if os.path.exists('university_data/'+university.replace(' ','_').replace('/','_')+'.xml'): continue
	index += 1
	print '%d of %d' % (index, len(universities))
	time.sleep(.5)
	writer = open('university_data/'+university.replace(' ', '_').replace('/','_')+'.xml', 'w')
	response = urllib.urlopen('https://maps.googleapis.com/maps/api/geocode/xml?address='+university.replace(' ','+')+'&key=AIzaSyDFH9bLWjpZPYqHdTqHMcG4igt5d66Qfeg').read()
	writer.write(response)
	writer.close()
