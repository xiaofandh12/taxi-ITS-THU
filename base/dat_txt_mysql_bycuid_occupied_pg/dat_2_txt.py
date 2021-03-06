import time
import struct
import os
import re

import common.config

all_f = os.listdir(dat_data_dir)
for f in all_f:
	if not os.path.isfile(dat_data_dir + f):
		continue
	(f_name, f_ext) = os.path.splitext(f)
	if (not f_ext == '.dat') or (not re.compile(dat_reg).match(f_name)):
		print "skip file:",f
		continue
	
	print 'processing',f,'...',
	bin_f = open(dat_data_dir + f, 'rb')
	text_f = open(txt_data_dir + f_name + '.txt', 'w')

	record_num = 0
	from_cuid = 0
	to_cuid = 0
	from_utc = 0
	to_utc = 0

	error_count = 0

	while True:
		buf = bin_f.read(28)
		if len(buf) < 28:
			if len(buf) == 0:
				print 'complete.'
				if error_count > 0:
					print ' errors:',error_count
				print 'record num:',record_num
				print 'time:from',time.ctime(from_utc),'to',time.ctime(to_utc)
				print 'cuid:from',from_cuid,'to',to_cuid
			else:
				print 'error: buf read less than 28 bytes'
			break
		(CUID,UTC,LAT,LONG,HEAD,SPEED,OCCUPANT) = struct.unpack("iiiiiii",buf)
		if (CUID <= 0 or 
			UTC <= 0 or 
			LAT < -9000000 or LAT > 9000000 or 
			LONG < -18000000 or LONG > 18000000 or 
			HEAD < 0 or HEAD > 360 or 
			SPEED < 0 or 
			OCCUPANT < 0):
			#print 'error: CUID=',CUID,'UTC=',UTC,'LAT=',LAT,'LONG=',LONG,'HEAD=',HEAD,'SPEED=',SPEED,'OCCUPANT=',OCCUPANT
			error_count += 1
			continue
	
		text_f.write(str(CUID)+','+str(UTC)+','+str(LAT)+','+str(LONG)+','+str(HEAD)+','+str(SPEED)+','+str(OCCUPANT)+'\n')
	
		record_num = record_num + 1
		if CUID < from_cuid or from_cuid == 0:
			from_cuid = CUID
		if CUID > to_cuid:
			to_cuid = CUID
		if UTC < from_utc or from_utc == 0:
			from_utc = UTC
		if UTC > to_utc:
			to_utc = UTC
	
	bin_f.close()
	text_f.close()	

