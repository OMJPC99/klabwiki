import MySQLdb
import sys
import ip_lookup

# sys.argv[1] = <database_name>
# sys.argv[2] = <output_file_name>

db = MySQLdb.connect(host='localhost',
                     user='root',
                     passwd='root',
                     db=sys.argv[1])

cursor = db.cursor()
cursor.execute('SELECT * FROM revisions WHERE journalName IS NOT NULL')
rows = cursor.fetchall()
writer = open(sys.argv[2], 'w')
for row in rows:
    line = '|'.join(map(str,row))
    writer.write(line + '\n')
writer.close()
