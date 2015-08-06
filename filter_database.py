import MySQLdb
import sys

# sys.argv[1] = <database_name>
# sys.argv[2] = <output_file_name>

db = MySQLdb.connect(host='localhost',
                     user='root',
                     passwd='root',
                     db=sys.argv[1])

cursor = db.cursor()
cursor.execute('SELECT revisions.*, journals.* FROM revisions, journals WHERE journals.journalName IS NOT NULL AND journals.ID=revisions.ID')
#cursor.execute('SELECT revisions.*, journals.* FROM revisions, journals INNER JOIN journals AS j ON j.ID=revisions.ID WHERE journals.journalName IS NOT NULL')
#cursor.execute('SELECT *, GROUP_CONCAT(journals.journalName SEPARATOR ", ") FROM revisions JOIN journals AS jo ON jo.ID = revisions.ID WHERE jo.journalName IS NOT NULL')
#cursor.execute('SELECT * FROM revisions INNER JOIN journals AS j ON j.ID = revisions.ID WHERE j.journalName IS NOT NULL')
rows = cursor.fetchall()
writer = open(sys.argv[2], 'w')
for row in rows:
    line = '|'.join(map(str,row))
    writer.write(line + '\n')
writer.close()
