import MySQLdb
import getpass
import os

import common.lib as lib
import common.config

'''
	max_cuid = 8602
'''

fromdate = (2009,5,1)   #format:(year, month, day)
todate = (2009,5,30)   

fromtime = (0,0,0)  #24hour, format:(hour, minute, second)
totime = (23,59,59)  

tbnames = lib.dates_to_tbnames(fromdate, todate)
utcs = lib.times_to_utcs(fromdate, todate, fromtime, totime)

conn = MySQLdb.connect(host=mysql_hostname,user=mysql_username,passwd=getpass.getpass("db password: "),db=mysql_dbname)  
cursor = conn.cursor()

print "mysql connected."


max_cuid = 0

for tbname, utc in zip(tbnames, utcs):	
	try:
		sql = r"SELECT MAX(CUID) FROM " + tbname
		#sql = r"SELECT COUNT(*) FROM " + tbname + r" WHERE UTC >= " + str(utc[0]) + r" AND " + r"UTC <= " + str(utc[1])
		#sql = r"SELECT * FROM " + tbname + r" WHERE CUID = 1"

		print 'querying',tbname,'...',
		cursor.execute(sql)
		results = cursor.fetchall()
		print 'completed'

		for items in results:
			print items[0]
			if int(items[0]) > max_cuid:
				max_cuid = items[0]
		pass
	except Exception as e:
		print e
		pass 

cursor.close()  
conn.close()

print max_cuid
