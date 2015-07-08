import sys
import re
import os
split_script = sys.argv[1]
i = sys.argv[2]
count = sys.argv[3]
rep = i.replace('.7z','')
os.system('aws s3 cp s3://klabwiki/7z_files/%s ./' % i)
print 'File received... Now unzipping the file...'
os.system('7z e %s' % i)
print 'File unzipped... Now splitting it...'
os.system('python splitter.py %s %d %s'%(rep,1000000000,count))
print 'Files have been split.'
os.system('rm %s' % i)	
