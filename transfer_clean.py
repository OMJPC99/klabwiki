import os
import sys

input_name = sys.argv[1]
output_name = sys.argv[2]
clean_and_ingest_script = sys.argv[3]  # unused except for swift purposes
parallel_clean_script = sys.argv[4]
grep_clean_script = sys.argv[5]

os.system('aws s3 cp s3://klabwiki/splits/' + input_name + ' ./')
os.system('7z e ' + input_name)
os.system('python clean_and_ingest.py wikibase ' + output_name)
