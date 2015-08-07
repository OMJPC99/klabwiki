import os
import re
import sys


def clean_directory(input_directory, output_directory):
    print 'Cleaning directory:', input_directory
    if not os.path.isdir(output_directory): os.mkdir(output_directory)
    index = 0
    last_page_id = ''
    print 'Building file list...(this may take a while)'
    file_list = os.listdir(input_directory)
    print 'Beginning iteration across files...'
    for file_name in sorted(file_list):
        # Move file into current directory for processing for the sake of easier file path operations
        os.system('mv %s%s ./' % (input_directory, file_name))
        last_page_id = clean_file(file_name, output_directory +'clean_%s' % file_name)
        index += 1
        cur_file_num += 1
	os.system('mv %s %s' % (file_name, input_directory))


def clean_file(input_file_name, output_file_name, last_page_id=''):
    print 'Grepping %s for IPs, user names, and journal citations' % input_file_name
    os.system('LC_ALL=C grep -o -E "\{\{cite journal.*?\}\}|\{\{cite pmid.*?\}\}|\{\{cite doi.*?\}\}|<ip>.*?</ip>|' +
              '<username>.*?</username>|<timestamp>.*?</timestamp>|<page>|<id>.*?</id>" %s > grepped.xml' % (input_file_name))

    print 'Generating final clean xml for %s' % input_file_name
    last_page_id = format_file('grepped.xml', output_file_name)
    os.system('rm grepped.xml')
    return last_page_id


def format_file(input_file_name, output_file_name, last_page_id=''):
    input_reader = open(input_file_name, 'r')
    output_writer = open(output_file_name, 'w')
    with open('unique_citations.txt', 'w') as uc: print 'Creating file for citations...'
    with open('unique_ids.txt', 'w') as ui: print 'Creating file for id citations...'
    if last_page_id == '': scan_for_page_id = True
    else: scan_for_page_id = False
    citation_count = 0
    first_revision = True

    output_writer.write('<root>\n')
    for line in input_reader:
        if '<ip>' in line:
            output_writer.write('\t\t' + line)
        elif '<page>' in line:
            scan_for_page_id = True
        elif scan_for_page_id and '<id>' in line:
            last_page_id = re.search('\d+', line).group()
            scan_for_page_id = False
        elif '<username>' in line:
            output_writer.write('\t\t' + line)
        elif '<timestamp>' in line:
            if not first_revision:
		output_writer.write('\t\t<page_id>%s</page_id>\n' % last_page_id) 
		output_writer.write('\t</revision>\n')
	    if first_revision: first_revision = False
	    output_writer.write('\t<revision>\n')
            output_writer.write('\t\t' + line)
        elif 'cite journal' in line:
            ms = re.findall('\{\{cite journal.*?\}\}', line)
            #if len(ms) > 1: print ms
            for m in ms:
                citation_count += 1
                if citation_count % 1000 == 0: print 'Citations found:', citation_count
                punctuation = ["[", "]", "{", "\n"]
                for p in punctuation: m = m.replace(p, '')
                attributes = m.split('|')
                desired_attributes = ['journal', 'author', 'last', 'first', 'year', 'volume', 'issue', 'pages', 'pmid', 'doi']
                acquired_attributes = parse_citation(attributes, desired_attributes)
                if not duplicate_cite(acquired_attributes):
                    output_writer.write('\t\t<cite_journal>\n')
                    output_writer.write('\t\t\t<name>' + acquired_attributes[0] + '</name>\n')
                    output_writer.write('\t\t\t<year>' + acquired_attributes[4] + '</year>\n')
		    output_writer.write('\t\t\t<pmid>' + acquired_attributes[8] + '</pmid>\n')
		    output_writer.write('\t\t\t<doi>' + acquired_attributes[9] + '</doi>\n')
                    output_writer.write('\t\t</cite_journal>\n')
        elif 'cite pmid' in line or 'cite doi' in line:
            punctuation = ["}", "{", "\n"]
            for p in punctuation: line = line.replace(p, '')
            tokens = line.split('|')
            try: id = tokens[1]
            except: 
		print line
		continue
            if not duplicate_cite(tokens, True):
                if 'pmid' in tokens[0]: output_writer.write('\t\t<cite_pmid>' + id + '</cite_pmid>\n')
                else: output_writer.write('\t\t<cite_doi>' + id + '</cite_doi>\n')
    output_writer.write('\t</revision>\n</root>')
    input_reader.close()
    output_writer.close()
    return last_page_id


def parse_citation(attributes, desired_attributes):
    acquired_attributes = [''] * len(desired_attributes)
    # index = 0
    for i in range(len(desired_attributes)):
        for attribute in attributes:
            match = re.search('\s*' + desired_attributes[i] + '\s*=\s*', attribute)
            if match:
                try: index = attribute.index('}')
                except: index = -1
                if index != -1 and match.end() != index: value = attribute[match.end():index]
                elif match.end() != len(attribute): value = attribute[match.end():len(attribute)]
            else: value = ''
            acquired_attributes[i] += value
    return acquired_attributes


def duplicate_cite(citation, doi_or_pmid = False):
    if not doi_or_pmid:
        unique_cite = open('unique_citations.txt', 'r')
        for line in unique_cite:
            past_cite = line[:len(line)-1].split('|')
            match = True
            for i in range(len(past_cite)):
                if (past_cite[i] != '') and (past_cite[i] != citation[i]): match = False
                if not match: break
            if match: return True
        unique_cite.close()
        with open('unique_citations.txt', 'a') as cite_writer: cite_writer.write('|'.join(citation) + '\n')
        return False
    else:
        unique_id = open('unique_ids.txt', 'r')
        for line in unique_id:
            past_id = line[:len(line) - 1].split('|')
            if past_id[0]==citation[0] and past_id[1]==citation[1]: return True
            unique_id.close()
            with open('unique_ids.txt', 'a') as id_writer: id_writer.write('|'.join(citation) + '\n')
            return False


clean_directory('unzipped/', 'cleaned/')
