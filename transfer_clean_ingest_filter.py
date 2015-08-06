import sys
import csv
import os

#group = sys.argv[1]
db = sys.argv[1]
output_name = sys.argv[2]

with  open('controlFile3.csv','wb') as csvfile:
        cw = csv.writer(csvfile, delimiter='|')
        cw.writerow(["DATABASE ", " %s  " % db , ".//revision"])
        # cw.writerow(["FILES ", " /mnt/disk0/summer_wiki/" + input_num + "_cleaned.xml"])
	cw.writerow(["FILES ", " cleaned_2/*"])
        cw.writerow(["TABLE ", " revisions"])
        cw.writerow(["COLUMN ", " ID ","  INT ", " AUTO_INCREMENT UNIQUE ", " DOC_ID"])
        cw.writerow(["COLUMN ", " ip "," VARCHAR(64) ", " ", " .//ip"])
        cw.writerow(["COLUMN ", " username "," VARCHAR(64) ", " ", " .//username"])
        cw.writerow(["COLUMN ", " time_stamp "," VARCHAR(64) ", " ", " .//timestamp"])
        cw.writerow(["COLUMN ", " pageID ", " VARCHAR(128) ", " ", " .//page_id"])

	cw.writerow(["TABLE "," journals",".//cite_journal"])
	cw.writerow(["COLUMN", " ID ", " INT ",""," DOC_ID"])
	cw.writerow(["COLUMN ", " journalName "," VARCHAR(128) ", " ", " .//name"])
        cw.writerow(["COLUMN ", " journalYear "," VARCHAR(12) ", " ", " .//year"])
	cw.writerow(["COLUMN ", " journalPMID "," VARCHAR(64) ", " ", " .//pmid"])
	cw.writerow(["COLUMN ", " journalDOI "," VARCHAR(64) ", " ", ".//doi"])
	cw.writerow(["COLUMN ", " citePMID "," VARCHAR(64) ", " ", ".//cite_pmid"])
	cw.writerow(["COLUMN ", " citeDOI "," VARCHAR(64) ", " ", ".//cite_doi"])


#print 'Transfering group %s...' % group
#os.system('python transfer_by_group.py %s' % group)
#print 'Cleaning group...'
#os.system('python grep_cleaner.py')
print 'Ingesting the files now...'
os.system('python UniversalIngest.py controlFile3.csv')
print 'Database has been ingested.\nFiltering database...'
os.system('python filter_database.py ' + db + ' ' + output_name)
print 'Database has been filtered.'

