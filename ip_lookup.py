
import os
import re

# ip is a string containing the ip address
def belong_to_university_dig(ip):
    print ip
    os.system('dig -x ' + ip + ' > reverse_lookup.txt')
    output = open('reverse_lookup.txt', 'r')
    university = ''
    scan_line = False
    for line in output:
        if '.edu.' in line.lower():
            university = university_name(ip)
            break
        # if line == ';; ANSWER SECTION:\n': scan_line == True
        # elif scan_line:
        #     answer = re.search('[\w\.]*?\.\\n', line)
        #     if answer:
        #         answer = answer.group()
        #         if answer[len(answer) - 5:len(answer) - 1] == 'edu.': university = university_name(ip)
        #     break

    output.close()
    os.system('rm reverse_lookup.txt')
    return university

def university_name(ip):
    os.system('whois ' + ip + ' > info.txt')
    output = open('info.txt', 'r')
    university = ''
    for line in output:
        if line[0:7] == 'OrgName':
            university = line[8:len(line)]
    output.close()
    os.system('rm info.txt')
    return university;

