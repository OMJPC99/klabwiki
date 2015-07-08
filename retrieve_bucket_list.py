import sys
import os
import re

big_file_list_name = sys.argv[1]
small_file_list_name = sys.argv[2]

os.system('aws s3 ls s3://klabwiki/7z_files/ > raw_list.txt')

read_file = open('raw_list.txt', 'r')

file_size_list = []
file_list = []

for line in read_file:
    print line
    file_size = int(re.search(r'\s+\d+\s+', line).group())
    print file_size
    file_size_list.append(file_size)
    file_list.append([file_size, line])

average_size = sum(file_size_list) / len(file_size_list)
print 'Average size:', average_size
big_file_list = open(big_file_list_name, 'w')
small_file_list = open(small_file_list_name, 'w')
big_file_count = 0
small_file_count = 0
for file_tokens in file_list:
    tokens = file_tokens[1].split(' ')
    if file_tokens[0] > average_size:
        big_file_list.write(tokens[len(tokens) - 1])
        big_file_count += 1
    else:
        small_file_list.write(tokens[len(tokens) - 1])
        small_file_count += 1

print 'Big file count:', big_file_count
print 'Small file count:', small_file_count
read_file.close()
big_file_list.close()
small_file_list.close()