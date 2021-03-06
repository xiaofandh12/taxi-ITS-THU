import datetime
import time
import os
import math

def dates_to_tbnames(fromdate, todate):
	tbnames = []
	d = datetime.date(fromdate[0],fromdate[1],fromdate[2])
	to_d = datetime.date(todate[0],todate[1],todate[2])
	while True:
		tbnames.append("tb_" + str(d).replace('-',''))
		d += datetime.date.resolution
		if d > to_d:
			return tuple(tbnames)

def times_to_utcs(fromdate, todate, fromtime, totime):
	utcs = []
	t = datetime.datetime(fromdate[0],fromdate[1],fromdate[2],fromtime[0],fromtime[1],fromtime[2])
	to_t = datetime.datetime(todate[0],todate[1],todate[2],totime[0],totime[1],totime[2])
	d = datetime.date(fromdate[0],fromdate[1],fromdate[2])
	to_d = datetime.date(todate[0],todate[1],todate[2])
	while True:
		utcs.append((time.mktime(t.utctimetuple()), time.mktime(to_t.utctimetuple())))   #mktime always convert local time to utc seconds
		d += datetime.date.resolution
		if d > to_d:
			return tuple(utcs)

def new_output_dir():
	output_dir = raw_input('Query results will be loaded in this new directory: ')
	if os.path.isdir(output_dir):
		print output_dir,"has exist"
		return ""
	os.mkdir(output_dir)	
	os.chdir(output_dir)
	os.mkdir('data')
	os.chdir('data')
	return os.getcwd()

def new_output_dir_as(output_dir):
	if os.path.isdir(output_dir):
		print output_dir,"has exist"
		return ""
	os.mkdir(output_dir)
	os.mkdir(output_dir + 'data/')
	return output_dir + 'data/'
	
def cmp_str_by_int(str_x, str_y):
	(x_name, x_ext) = os.path.splitext(str_x)
	(y_name, y_ext) = os.path.splitext(str_y)
	return int(x_name) - int(y_name)
	
def is_record_in_area(line, min_lo, max_lo, min_la, max_la):
	s = line.split(', ')
	lo = int(s[2])
	la = int(s[3])
	return lo >= min_lo and lo <= max_lo and la >= min_la and la <= max_la

def is_coord_in_area(coord, min_lon, max_lon, min_lat, max_lat):
	lon = coord[0]
	lat = coord[1]
	return lon >= min_lon and lon <= max_lon and lat >= min_lat and lat <= max_lat

def parse_line(line):
	s = line.split(', ')
	attrs = {}
	attrs['cuid'] = s[0]
	attrs['time'] = time.localtime(long(s[1]))
	attrs['lat'] = float(s[2]) / 100000
	attrs['lon'] = float(s[3]) / 100000
	attrs['head'] = int(s[4])
	attrs['speed'] = int(s[5])
	attrs['occupied'] = int(s[6])
	return attrs
	
def lonlats2km(s_lonlat, t_lonlat):
    dlat = 111.0 * abs(s_lonlat[1] - t_lonlat[1])
    dlon = 111.0 * abs(math.cos(math.radians((s_lonlat[1] + t_lonlat[1]) / 2))) * abs(s_lonlat[0] - t_lonlat[0])
    return math.sqrt(dlat**2 + dlon**2)
	
