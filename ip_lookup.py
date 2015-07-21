
import os
import sys

# ip is a string containing the ip address
def belong_to_university_dig(ip):
    print ip
    os.system('dig -x ' + ip + ' > reverse_lookup.txt')
    output = open('reverse_lookup.txt', 'r')
    university = ''
    scan_line = False
    for line in output:
        if ".edu." in line.lower():
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
        if line[0:7] == "OrgName":
            university = line[8:len(line)]
    output.close()
    os.system('rm info.txt')
    return university

def scan_file(input_file_name, output_file_name):
    print 'Opening read/write files...'
    reader = open(input_file_name, 'r'); writer = open(output_file_name, 'w')
    print 'Performing reverse lookups...'
    for line in reader:
        tokens = line.split('|')
        if tokens[1] == "None": continue
        university = belong_to_university_dig(tokens[1]).lstrip()
        if university == '': continue
        print 'IP:', tokens[1], 'University:', university
        writer.write(tokens[1] + '|' + university + '\n')
    reader.close(); writer.close()

def scan_directory(directory_name):
    if directory_name[len(directory_name)-1] != "/": directory_name += '/'
    for file_name in os.listdir(directory_name):
        os.system('cp %s%s ./%s' % (directory_name, file_name, file_name))
        count_ips(file_name)
        scan_file(file_name, 'searched_' + file_name)
        os.system('mkdir searched')
        os.system('mv searched_%s searched/searched_%s' % (file_name, file_name))

def count_ips(input_file_name):
    print 'Counting IPs in file'
    total = 0
    with open(input_file_name, 'r') as reader:
        for line in reader:
            if line.split('|')[1]:
                total += 1
                sys.stdout.write('\rIPs found: %d' % total)
    print '\n'
scan_directory(sys.argv[1], 'searched_' + sys.argv[1])