
import os, re

def clean_file(input_name, output_name, clean=False, input_directory='split_xml/', output_directory='clean_xml/'):
    # 'ip_regex' matches IPs such as 192.168.0.0 or anonymous ones like 192.168.0.xxx
    ip_regex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\w{1,3}")

    # If the specified output directory does not exist, this makes it
    os.system('mkdir ' + output_directory)

    # Use grep to reduce to relevant information faster than python can
    print 'Finding IPs, user names, and journal citations for "%s"' % input_name
    os.system('grep -o -E "\{\{cite journal.*?\}\}|<ip>.*?</ip>|<username>.*?</username>|<timestamp>.*?</timestamp>" ' + input_directory + input_name + " > " + output_directory + "semi_clean_" + input_name + ".xml")

    if clean:
        os.system('rm ' + input_directory + input_name)

    # Takes grep's semi-cleaned file, and extracts the necessary information
    parse_citations(output_directory + "semi_clean_" + input_name + ".xml",
                    output_directory + output_name)
    os.system('rm ' + output_directory + "semi_clean_" + input_name + ".xml")


# Takes grep's semi-cleaned file, and extracts the necessary information
def parse_citations(input_file, output_file):
    input_read = open(input_file, 'r')              # input scanner
    output_write = open(output_file, 'w')           # output file writer
    unique_cite = open('unique_citations.txt', 'w') # force creation of new document
    unique_cite.close()
    citation_count = 0                              # number of citations in the document

    output_write.write('<root>\n')
    output_write.write('    <revision>\n')
    output_write.write('        ' + input_read.readline())
    for line in input_read:
        if '<ip>' in line:
            output_write.write('        ' + line)
        elif '<username>' in line:
            output_write.write('        ' + line)
        elif '<timestamp>' in line:
            output_write.write('    </revision>\n')
            output_write.write('    <revision>\n')
            output_write.write('        ' + line)
        else:
            # Prints a count every 1000 citations encountered
            citation_count += 1
            if citation_count % 1000 == 0:
                print 'Citations found:', citation_count
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('{', '')
            line = line.replace('\n', '')

            # Break on the attribute delimiter for citation format
            attributes = line.split('|')
            desired_attributes = ['journal', 'author', 'last', 'first', 'year', 'volume', 'issue', 'pages']
            acquired_attributes = parse_citation(attributes, desired_attributes)
            year = ''
            i = 0
            for c in iter(acquired_attributes[4]):
                year += c
                i += 1
                if i % 4 == 0: year += ' '
            acquired_attributes[4] = year
            if not duplicate_cite(acquired_attributes):
                output_write.write('        <cite_journal>\n')
                output_write.write('            <name>' + acquired_attributes[0] + '</name>\n')
                output_write.write('            <year>' + acquired_attributes[4] + '</year>\n')
                output_write.write('        </cite_journal>\n')

    output_write.write('    </revision>\n')
    output_write.write('</root>')
    input_read.close()
    output_write.close()


def parse_citation(attributes, desired_attributes):
    acquired_attributes = [''] * len(desired_attributes)

    index = 0
    for i in range(0, len(desired_attributes)):
        for attribute in attributes:
            match = re.search('\s*' + desired_attributes[i] + '\s*=\s*', attribute)
            if match:
                try:
                    index = attribute.index('}')
                except:
                    index = -1
                if index != -1 and match.end() != index:
                    value = attribute[match.end():index]
                elif match.end() != len(attribute):
                    value = attribute[match.end():len(attribute)]
            else:
                value = ''
            acquired_attributes[i] += value
    return acquired_attributes


def duplicate_cite(citation):
    unique_cite = open('unique_citations.txt', 'r')
    for line in unique_cite:
        past_cite = line[0:len(line)-1].split('|')
        match = True
        for i in range(0, len(past_cite)):
            if (past_cite[i] != '') and (past_cite[i] != citation[i]):
                match = False
            if not match:
                break
        if match:
            return True
    unique_cite.close()
    citation = '|'.join(citation)
    with open('unique_citations.txt', 'a') as cite_writer:
        cite_writer.write(citation + '\n')
    return False

#clean_file('Wikipedia-20150619203602.xml', 'cleaned_test.xml', input_directory='', output_directory='')
