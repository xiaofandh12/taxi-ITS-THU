import json
import time

from common.data_parser import *
import common.lib as lib
import common.config

output_dir = proc_output_dir

s_min_lon = 116.56210
s_max_lon = 116.63076
s_min_lat = 40.03905
s_max_lat = 40.12049

t_min_lon = 116.56210
t_max_lon = 116.63076
t_min_lat = 40.03905
t_max_lat = 40.12049

from_cuid = 1
to_cuid = 20

in_one_file = True
start_limited = False
target_limited = True


if target_limited:
	output_prefix = "geojson_t_"
else:
	output_prefix = "geojson_"

class Geojson:
	
	def parser_start_callback(self):
		if in_one_file:
			self.jdict = dict()
			self.jdict["type"] = "FeatureCollection"
			self.features = list()
			self.coordnum = 0

	def parser_end_callback(self):
		if in_one_file:
			self.jdict["features"] = self.features
			self.write_to_file(output_dir + output_prefix + str(from_cuid) + "_" + str(to_cuid) + ".json")

	def cuid_start_callback(self, cuid):
		if not in_one_file:
			self.jdict = dict()
			self.jdict["type"] = "FeatureCollection"
			self.features = list()
			self.coordnum = 0

		self.geo = dict()
		self.geo["type"] = "LineString"
		self.coords = list()
		self.descs = list()

		self.pre_occupied = -1

	def cuid_end_callback(self, cuid):		
		if not in_one_file:
			self.jdict["features"] = self.features
			self.write_to_file(output_dir + output_prefix + str(cuid) + ".json")

	def file_start_callback(self, infn):
		pass

	def file_end_callback(self, infn):
		pass	

	def line_callback(self, line):
		attrs = lib.parse_line(line)
		
		time_tx = time.strftime("%Y-%m-%dT%H:%M:%SZ", attrs['time'])
		head_tx = str(attrs['head'])
		speed_tx = str(attrs['speed'])
		occupied_tx = str(attrs['occupied'])

		if attrs['occupied'] == 1:
			coord = [attrs['lon'], attrs['lat']]
			self.coords.append(coord)
			self.descs.append({"t":time_tx,"h":head_tx,"s":speed_tx,"o":occupied_tx})
			self.coordnum = self.coordnum + 1

		if self.pre_occupied == -1:
			pass

		elif self.pre_occupied == 0 and attrs['occupied'] == 1:
			pass

		elif self.pre_occupied == 1 and attrs['occupied'] == 0:
			track_needed = False

			if (not start_limited) or lib.is_coord_in_area(self.coords[0], s_min_lon, s_max_lon, s_min_lat, s_max_lat):
				track_needed = True
			if track_needed and ((not target_limited) or lib.is_coord_in_area(self.coords[-1], t_min_lon, t_max_lon, t_min_lat, t_max_lat)):
				track_needed = True
			else:
				track_needed = False
			
			if track_needed:
				self.geo["coordinates"] = self.coords
				self.features.append({"geometry":self.geo, "properties":{"desc":self.descs}})

			self.geo = dict()
			self.geo["type"] = "LineString"
			self.coords = list()
			self.descs = list()

		self.pre_occupied = attrs['occupied']


	def write_to_file(self, filename):
		with open(filename, "w") as f:
			f.write(json.dumps(self.jdict))
	
geojson = Geojson()

read_by_cuid(from_cuid,to_cuid,geojson)

print "num of tracks =",len(geojson.features),"num of coord =",geojson.coordnum

