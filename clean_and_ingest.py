import sys
import csv

db = sys.argv[1]
output_name = sys.argv[2]
input_file = sys.argv[3]
input_num = sys.argv[4]

with  open(input_num + 'controlFile3.csv','wb') as csvfile:
        cw = csv.writer(csvfile, delimiter='|')
        cw.writerow(["DATABASE ", " %s  " % db , ".//revision"])
        cw.writerow(["FILES ", " /mnt/disk0/summer_wiki/" + input_num + "_cleaned.xml"])
        cw.writerow(["TABLE ", " revisions"])
        cw.writerow(["COLUMN ", " revID ","  INT ", " AUTO_INCREMENT UNIQUE ", " DOC_ID"])
        cw.writerow(["COLUMN ", " ip "," VARCHAR(64) ", " ", " .//ip"])
        cw.writerow(["COLUMN ", " username "," VARCHAR(64) ", " ", " .//username"])
        cw.writerow(["COLUMN ", " time_stamp "," VARCHAR(64) ", " ", " .//timestamp"])
        cw.writerow(["COLUMN ", " journalName "," VARCHAR(128) ", " ", " .//name"])
        cw.writerow(["COLUMN ", " journalYear"," VARCHAR(12) ", " ", " .//year"])

os.system('python grep_cleaner.py ' + input_file + ' ' + input_num)
print 'Ingesting the files now...'
os.system('python UniversalIngest.py ' + input_num + 'controlFile3.csv')
print 'Database has been ingested.\nFiltering database...'
os.system('python filter_database.py ' + db + ' ' + output_name)
print 'Database has been filtered.'

