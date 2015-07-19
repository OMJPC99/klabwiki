import os
import re
import sys

groups = set()
out_file_name = 'group_list.txt' # sys.argv[1]
os.system('aws s3 ls s3://klabwiki/splits/ > raw_list.txt')

read_file = open('raw_list.txt', 'r')
write_file = open(out_file_name, 'w')

for line in read_file:
    match = re.search('[a-zA-Z_]*split_xml_\d+', line)
    if not match: continue
    else: match = match.group()
    if match not in groups: groups.add(match)

for group in groups:
    write_file.write(group + '\n')

read_file.close()
write_file.close()
os.system('rm raw_list.txt')
