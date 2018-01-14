import numpy as np
import pandas as pd
import math
import datetime

LATITUDE_DE = 41.8873906
LONGITUDE_DE = -87.6459561
LATITUDE = LATITUDE_DE * math.pi / 180
LONGITUDE = LONGITUDE_DE * math.pi / 180
DATE = datetime.date(2016, 11, 1)
DISTANCE = 0.5
RADIUS = 3961

def date_compare(inspectionDate):
	"""The function is to compare the inspection date passed in with 
	the DATE 2016/11/1 in proper format

	Args: the inspection date of restaurant
	Return: whether the date is latter or equal to DATE
	"""
	if isinstance(inspectionDate, str):
	    mounth, day, year = inspectionDate.split('/')
	    return datetime.date(int(year), int(mounth), int(day)) >= DATE
	return False

def get_distance(location):
	""" This function is to get the distance between Dr. Romano's apartment
	and each input location

	Args: location: a tuple of latitude and longtitude of degree in String format
	return: the distance from apartment to given position in miles, or the diameter
			of earth if the input location is not a string
	"""
	if isinstance(location, str):
		la = float(location[1:-1].split(',')[0])
		lo = float(location[1:-1].split(',')[1])
		r_la = la * math.pi / 180
		r_lo = lo * math.pi / 180
		part_1 = (math.sin((LATITUDE - r_la) / 2)) ** 2
		part_2 =  math.cos(r_la) * math.cos(LATITUDE) * ((math.sin((LONGITUDE - r_lo) / 2)) ** 2)
		return 2 * RADIUS * math.asin(math.sqrt(part_1 + part_2))
	else:
		return 2 * RADIUS


def search_by_zip(dataframe):
	"""Search the restaurants which have ZIP 60661 and get a fail in the inspection 
	after the DATE 2016/11/1

	Args: dataframe: a dataframe containing all the data
	Return: all the matching rows
	"""
	return dataframe[(dataframe['Facility Type'] == 'Restaurant') & (dataframe['Zip'] == 60661) &
			(dataframe['Results'] == 'Fail') & (dataframe['Inspection Date'].map(date_compare))]

def search_by_location(dataframe):
	"""Search the restaurants which have a distance within 0.5 mile with apartment and get 
	a fail in the inspection after the DATE 2016/11/1

	Args: dataframe: a dataframe containing all the data
	Return: all the matching rows
	"""

	dataframe['Distance'] = [get_distance(i) for i in dataframe['Location']]

	temp_dataframe =  dataframe[(dataframe['Facility Type'] == 'Restaurant') & (dataframe['Results'] == 'Fail') &
                     (dataframe['Inspection Date'].map(date_compare)) & (dataframe['Distance'] <= DISTANCE)]
	return temp_dataframe.sort_values('Distance').drop('Distance', axis=1)

def main():
	dataframe = pd.read_csv('Food_inspections.csv')
	print(search_by_zip(dataframe))    
	print(search_by_location(dataframe))

if __name__ == "__main__":
    main();