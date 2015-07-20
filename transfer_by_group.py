import os
import re
import sys


def transfer(aws_line):
    m = re.search('[a-zA-Z_]*split_xml_.*', aws_line).group()
    if not os.path.isdir('transfers'): os.mkdir('transfers')
    os.system('aws s3 cp s3://klabwiki/splits/%s transfers/' % m)

group = sys.argv[1]
os.system('aws s3 ls s3://klabwiki/splits/ > raw_list.txt')
with open('raw_list.txt', 'r') as read_file:
    for line in read_file:
        match = re.search('[a-zA-Z_]*split_xml_\d+', line)
        if not match: continue
        else: match = match.group()

        if match[:len(group)] == group:
            transfer(line)
if not os.path.isdir('unzipped'): os.mkdir('unzipped')
for file_name in os.listdir('transfers/'):
    os.system('7z e transfers/%s -ounzipped/' % file_name)
    os.system('rm transfers/%s' % file_name)
os.system('rm raw_list.txt')
