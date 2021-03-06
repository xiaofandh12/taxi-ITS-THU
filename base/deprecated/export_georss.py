import xml.dom.minidom as minidom
import time

from common.data_parser import *
import common.lib as lib
import common.config

output_dir = proc_output_dir

class Georss:
	
	def cuid_start_callback(self, cuid):
		self.doc = minidom.Document()

		self.rss = self.doc.createElementNS('http://www.w3.org/2003/01/geo/wgs84_pos#','rss')
		self.rss.setAttribute('version', '2.0')
		self.rss.setAttribute('xmlns:geo', 'http://www.w3.org/2003/01/geo/wgs84_pos#')
		self.doc.appendChild(self.rss)

		title_el = self.doc.createElement('title')
		title_tx = self.doc.createTextNode('.....')
		title_el.appendChild(title_tx)
		self.rss.appendChild(title_el)

		desc_el = self.doc.createElement('description')
		desc_tx = self.doc.createTextNode('.....')
		desc_el.appendChild(desc_tx)
		self.rss.appendChild(desc_el)

		self.pre_occupied = -1

	def cuid_end_callback(self, cuid):
		self.write_to_file(output_dir + "georss_" + str(cuid))

	def file_start_callback(self, infn):
		pass

	def file_end_callback(self, infn):
		pass	

	def line_callback(self, line):
		attrs = lib.parse_line(line)

		item_el = self.doc.createElement('item')
		self.rss.appendChild(item_el)
	
		pubdate_el = self.doc.createElement('pubDate')
		pubdate_tx = self.doc.createTextNode(time.strftime("%Y-%m-%dT%H:%M:%SZ", attrs['time']))
		pubdate_el.appendChild(pubdate_tx)
		item_el.appendChild(pubdate_el)

		lat_el = self.doc.createElement('geo:lat')
		lat_tx = self.doc.createTextNode(str(attrs['lat']))
		lat_el.appendChild(lat_tx)
		item_el.appendChild(lat_el)

		long_el = self.doc.createElement('geo:long')
		long_tx = self.doc.createTextNode(str(attrs['lon']))
		long_el.appendChild(long_tx)
		item_el.appendChild(long_el)

		head_el = self.doc.createElement('head')
		head_tx = self.doc.createTextNode(str(attrs['head']))
		head_el.appendChild(head_tx)
		item_el.appendChild(head_el)

		speed_el = self.doc.createElement('speed')
		speed_tx = self.doc.createTextNode(str(attrs['speed']))
		speed_el.appendChild(speed_tx)
		item_el.appendChild(speed_el)

		occupied_el = self.doc.createElement('occupied')
		occupied_tx = self.doc.createTextNode(str(attrs['occupied']))
		occupied_el.appendChild(occupied_tx)
		item_el.appendChild(occupied_el)

		if self.pre_occupied == -1:
			pass
		elif self.pre_occupied == 0 and attrs['occupied'] == 1:
			title_el = self.doc.createElement('title')
			title_tx = self.doc.createTextNode('Origin')
			title_el.appendChild(title_tx)
			item_el.appendChild(title_el)

			desc_el = self.doc.createElement('description')
			desc_tx = self.doc.createTextNode(time.strftime("%Y-%m-%dT%H:%M:%SZ", attrs['time']))
			desc_el.appendChild(desc_tx)
			item_el.appendChild(desc_el)
		elif self.pre_occupied == 1 and attrs['occupied'] == 0:
			title_el = self.doc.createElement('title')
			title_tx = self.doc.createTextNode('Target')
			title_el.appendChild(title_tx)
			item_el.appendChild(title_el)

			desc_el = self.doc.createElement('description')
			desc_tx = self.doc.createTextNode(time.strftime("%Y-%m-%dT%H:%M:%SZ", attrs['time']))
			desc_el.appendChild(desc_tx)
			item_el.appendChild(desc_el)

		self.pre_occupied = attrs['occupied']


	def write_to_file(self, filename):
		with open(filename, "w") as f:
			f.write(self.doc.toprettyxml())
	
georss = Georss()

read_by_cuid(1,1,georss)



