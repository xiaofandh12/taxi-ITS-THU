import os

import common.lib as lib
import common.config

execfile("config.py")

max_cuid = 8602
#max_cuid = 3

for cuid in range(1, max_cuid + 1):
	input_dir = proc_input_dir + 'CUID_' + str(cuid) + '/data/'
	if not os.path.isdir(input_dir):
		continue

	output_dir = lib.new_output_dir_as(proc_output_dir + 'CUID_' + str(cuid) + '/')
	f_count = 1
	l_count = 0
	f = open(output_dir + str(f_count) + '.txt', 'w')
	#print 'new file:',f.name

	print 'CUID =',str(cuid),'...',

	all_infn = sorted(os.listdir(input_dir),cmp=lib.cmp_str_by_int)

	pre_occupied = -1
	pre_line = ""

	for infn in all_infn:	
		if not os.path.isfile(input_dir + infn):
			continue

		inf = open(input_dir + infn, 'r')
		while True:
			line = inf.readline()
			if len(line) == 0:
				break

			curr_occupied = line.split(', ')[6]
			if pre_line == "":
				f.write(line)
				l_count += 1				
			elif curr_occupied == "1":
				if pre_occupied == "0":
					f.write(pre_line + '\n')
					l_count += 2
				f.write(line)
				l_count += 1
			elif curr_occupied == "0" and pre_occupied == "1":
				f.write('\n'+line)
				l_count += 2
			pre_occupied = curr_occupied
			pre_line = line

			if l_count >= query_output_lines:
				f.close()
				f_count += 1
				f = open(output_dir + str(f_count) + '.txt', 'w')
				#print 'new file:',f.name
				l_count = 0
		pass

	f.close()
	
	print 'completed'

