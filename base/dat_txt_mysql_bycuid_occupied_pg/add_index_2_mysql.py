import MySQLdb
import getpass
import os

import common.lib as lib
import common.config

fromdate = (2009,5,1)   #format:(year, month, day)
todate = (2009,5,30)   

tbnames = lib.dates_to_tbnames(fromdate, todate)

conn = MySQLdb.connect(host=mysql_hostname,user=mysql_username,passwd=getpass.getpass("db password: "),db=mysql_dbname)  
cursor = conn.cursor()

print "mysql connected."

for tbname in tbnames:	
	try:
		sql = r"ALTER TABLE " + tbname + " ADD INDEX iCUID (CUID)"

		print 'querying',tbname,'...',
		cursor.execute(sql)
		print 'completed'

	except Exception as e:
		print e
		pass 

cursor.close()  
conn.close()
