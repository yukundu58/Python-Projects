import math
import csv
import webbrowser
from datetime import datetime

class Library:
	def __init__(self, data):
		self.name = data['NAME ']
		self.hours = self.hours_helper(data['HOURS OF OPERATION'].replace('M-TH', 'M, TU, W, TH'))
		self.address = data['ADDRESS']
		self.city = data['CITY']
		self.state = data['STATE']
		self.zip = data['ZIP']
		self.phone = data['PHONE']
		self.url = data['WEBSITE']
		self.location = Coordinate.fromdegrees(data['LOCATION'][1:-1].split(', ')[0], data['LOCATION'][1:-1].split(', ')[1])

	def open_website(self):
		webbrowser.open_new_tab(self.url)

	def __repr__(self):
		return f'Library({self.name})'

	def hours_helper(self, hours_operation):
		time_list = [0,-1]*7
		day_dict = {'M':0, 'TU':1, 'W':2, 'TH':3, 'F':4, 'SA':5, 'SU':6}
		for item in hours_operation.split(';'):
			if 'Closed' in item: 
				continue
			for i in day_dict.keys():
				if i in item.split(':')[0]:
					open_time = item.split(': ')[1].split('-')[0]
					close_time = item.split(': ')[1].split('-')[1]
					if 'PM' in open_time and '12' not in open_time:
						time_list[2 * int(day_dict[i])] = int(open_time[:-2]) + 12
					else :
						time_list[2 * int(day_dict[i])] = int(open_time[:-2])
					if 'PM' in close_time and '12' not in close_time:
						time_list[2 * int(day_dict[i]) + 1] = int(close_time[:-2]) + 12
					else :
						time_list[2 * int(day_dict[i]) + 1] = int(close_time[:-2])
		return time_list

	def is_open(self, time):
		day = time.weekday()
		time_day = time.hour + time.minute / 60
		return self.hours[day * 2] <= time_day <= self.hours[day * 2 + 1] 

	def distance(self, coord):
		return self.location.distance(coord)

	def full_address(self):
		return f'{self.address}\n{self.city}, {self.state} {self.zip}'

class Coordinate:
	def __init__(self, latitude, longitude):
		self.latitude = latitude;
		self.longitude = longitude;

	@classmethod
	def fromdegrees(cls, latitude, longitude):
			return Coordinate(float(latitude) * math.pi / 180, float(longitude) * math.pi / 180)

	def distance(self, coord):
		part1 = (math.sin((coord.latitude - self.latitude) / 2)) ** 2
		part2 = math.cos(self.latitude) * math.cos(coord.latitude) * (math.sin((coord.longitude - self.longitude) / 2)) ** 2
		return 2 * 3961 * math.asin(math.sqrt(part2 + part1))

	def as_degrees(self):
		return self.latitude * 180 / math.pi, self.longitude * 180 / math.pi

	def show_map(self):
		degree_para = self.as_degrees();
		webbrowser.open_new_tab(f'http://maps.google.com/maps?q={degree_para[0]},{degree_para[1]}')

	def __repr__(self):
		return f'Coordinate({self.as_degrees()[0]} {self.as_degrees()[1]})'


class City:
	def __init__(self, filename):
		self.libraries = []
		with open(filename, 'r', newline='') as f:
			reader = csv.DictReader(f)
			for row in reader:
				self.libraries.append(Library(row))

	def nearest_library(self, coord):
		closest = self.libraries[0]
		for library in self.libraries:
			if library.distance(coord) < closest.distance(coord):
				closest = library
		return closest

"""
chicago = City('libraries.csv')
print(chicago.libraries[:5])
print([x for x in chicago.libraries if x.name.startswith('N')])
the_bean = Coordinate.fromdegrees(41.8821512, -87.6246838)
print(chicago.nearest_library(the_bean))
the_bean.show_map()
time = datetime(2017, 10, 9, 20, 30)
for x in chicago.libraries:
	print(x.hours)
print([x for x in chicago.libraries if x.is_open(time)])
austin = chicago.libraries[3]
print(austin.full_address())
print('5615 W. Race Avenue\nCHICAGO, IL 60644')
print(austin.full_address() == '5615 W. Race Avenue\nCHICAGO, IL 60644')
print(austin.location)
"""