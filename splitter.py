__author__ = 'theodoreando'

import sys
import os

file_count = 0

input_name = sys.argv[1]
MAX_BYTES = int(sys.argv[2])
output_count = sys.argv[3]

input_xml = open(sys.argv[1], 'r')
output_xml = open('split_xml_' + output_count + '_%d.xml' % file_count, 'w')

current_bytes = 0
for line in input_xml:
    output_xml.write(line)
    if current_bytes < MAX_BYTES:
        current_bytes += len(line)
    elif '</rev' in line:
        os.system('aws s3 cp split_xml_' + output_count + '_%d.xml' % file_count + ' s3://klabwiki/splits/')
        current_bytes = 0
        file_count += 1
        output_xml = open('split_xml_' + output_count + '_%d.xml' % file_count, 'w')

input_xml.close()
output_xml.close()
os.system('rm ' + sys.argv[1])