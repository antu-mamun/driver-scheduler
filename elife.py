import geopy.distance
from datetime import datetime, timedelta
avail_driver = []
import numpy
# Estimate Time Equation: 2*(int((distance*3)/(60)))
# Price Score Equation: price_per_hour*10
# Distance Score Equation: distance*3.146
# Final Score Equation: Distance_Score/Price_Score

driver_list = {1:["driver_1", 10, 40.758896,-73.985130, "2023-03-17 08:50:00.000123 to 2023-03-17 10:30:00.000123_,_2023-03-17 11:30:00.000123 to 2023-03-17 23:30:00.000123"],
			2:["driver_2", 11, 40.758896,-73.985130, "2023-03-17 10:30:00.000123 to 2023-03-17 18:30:00.000123_,_2023-03-17 22:30:00.000123 to 2023-03-17 23:30:00.000123"],
			3:["driver_3", 12, 40.758896,-73.985130, "2023-03-17 15:30:00.000123 to 2023-03-17 20:30:00.000123"],
			4:["driver_4", 13, 40.758896,-73.985130, "[]"],
			5:["driver_5", 14, 40.758896,-73.985130, "[]"]}
# ["Driver ID", "Price Per Hour", "Current Possition Latitude", "Current Possition Longitude", "Boked Time"],
ride_list = {1:["2023-03-17 09:00:00.000123", 40.308896,-73.185130, 42.308896,-78.985130, 52, "Empty"],
			2:["2023-03-17 11:30:00.000123", 40.808896,-73.185130, 41.308896,-72.185130, 10, "Empty"],
			3:["2023-03-17 11:00:00.000123", 39.708896,-73.900030, 43.308896,-78.185130, 52, "Empty"],
			4:["2023-03-17 09:30:00.000123", 40.308896,-73.585130, 48.308896,-77.185130, 92, "Empty"],
			5:["2023-03-17 11:30:00.000123", 40.908896,-74.185130, 40.908896,-77.185130, 24, "Empty"],
			6:["2023-03-17 16:00:00.000123", 39.108896,-74.985130, 40.308896,-78.985130, 36, "Empty"],
			7:["2023-03-17 22:00:00.000123", 44.308896,-93.185130, 40.758896,-73.985130, 162, "Empty"],
			8:["2023-03-17 09:30:00.000123", 44.508896,-83.185130, 40.758896,-73.985130, 86, "Empty"],
			9:["2023-03-17 09:20:00.000123", 43.808896,-73.185130, 40.308896,-73.185130, 38, "Empty"],
			10:["2023-03-17 10:30:00.000123", 34.10191,-63.112130, 40.308896,-73.185130, 112, "Empty"]}
# ["Pickup Time", "Pickup Location Latitude", "Pickup Location Longitude", "Drop off Location Latitude", "Drop off Location Longitude", "Estimate_Time", "Empty"],

def time_in_range(start, end, x):
	if ((start <= x) and (end>=x)):
		return True
	else:
		return False

def getDistance(pick_lat_x,pick_lat_y,drop_lat_x,drop_lat_y):
	coords_1 = (pick_lat_x,pick_lat_y)
	coords_2 = (drop_lat_x,drop_lat_y)
	distance = geopy.distance.geodesic(coords_1,coords_2).km
	return distance;
def printAllDriver():
	print ("{:<3} {:<20} {:<20} {:<20} {:<20} {:<20}".format('k', 'driver', 'price','cur_loc_latx','cur_loc_laty','booked_slot'))
	for k, v in driver_list.items():
	    driver, price, cur_loc_latx, cur_loc_laty, booked_slot = v
	    print ("{:<3} {:<20} {:<20} {:<20} {:<20} {:<20}".format(k, driver, price, cur_loc_latx, cur_loc_laty, booked_slot))
	print("\n")
def prinAllRide():
	print ("{:<3} {:<30} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format('k', 'pickup_time', 'pick_lat_x', 'pick_lat_y', 'drop_lat_x', 'drop_lat_y', 'es_time','assigned_driver'))
	for k, v in ride_list.items():
	    pickup_time, pick_lat_x, pick_lat_y, drop_lat_x, drop_lat_y, es_time, assigned_driver  = v
	    print ("{:<3} {:<30} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(k, pickup_time, pick_lat_x, pick_lat_y, drop_lat_x, drop_lat_y, es_time,assigned_driver))
	# print("\n")
def checkDriverAvailable(driver_info,start_time,es_time):
	dt=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
	newDT = (dt + timedelta(minutes=es_time))
	if(driver_info[4]=="[]"):
		return True
	else:
		booked_time = driver_info[4].split("_,_")
		inRange = False
		for i in range(len(booked_time)):
			booked_time_split = booked_time[i].split(" to ")
			start = datetime.strptime(booked_time_split[0], '%Y-%m-%d %H:%M:%S.%f')
			end = datetime.strptime(booked_time_split[1], '%Y-%m-%d %H:%M:%S.%f')
			t_chk = time_in_range(start, end, newDT)
			if(t_chk):
				inRange=False
				break
			else:
				inRange=True
		return inRange
def findMaxScore(driver_score_only):
	max = driver_score_only[0]
	arr = numpy.array(driver_score_only)
	# print("Max Score: ", numpy.amax(driver_score_only))
	max_index = numpy.where(arr == numpy.amax(arr))
	return max_index[0][0]
def findDriverByScore(avail_driver,pick_lat_x,pick_lat_y):
	driver_score = []
	driver_id = []
	for i in range(len(avail_driver)):
		price_score = driver_list[avail_driver[i]][1]*10
		distance_score = getDistance(pick_lat_x,pick_lat_y,driver_list[avail_driver[i]][2],driver_list[avail_driver[i]][3])*3.146
		final_score = distance_score/price_score
		# driver_score.append(avail_driver[i]+"__"+final_score)
		driver_id.append(avail_driver[i])
		driver_score.append(final_score)
		# print("for Driver ", avail_driver[i]," Price Score: ",price_score,"Distance Score: ",distance_score," and Final Score: ",final_score)
	getDriverId = findMaxScore(driver_score)
	# print("Selected Driver ID: ",driver_id[getDriverId])
	return driver_id[getDriverId]
def getHighestScoreDriver(ride_k,start_time,pick_lat_x,pick_lat_y,es_time):
	for k, v in driver_list.items():
	    # print("Driver Info: ",driver_list[k],"Start Time: ", start_time,"Estimate Time: ",int(es_time))
	    driver, price, cur_loc_latx, cur_loc_laty, booked_slot = v
	    chk=checkDriverAvailable(driver_list[k],start_time,int(es_time))
	    if(chk):
	    	# print("-->Availabe\n") 
	    	avail_driver.append(k)
	    # else:
	    # 	print("-->Not Availabe\n")
	# print(avail_driver," for ",start_time,pick_lat_x,pick_lat_y,es_time)
	setThisDriver = findDriverByScore(avail_driver,pick_lat_x,pick_lat_y)
	# print("Assigning DriverID for RideID",ride_k,": ",setThisDriver)
	# ride_list[ride_k][6] = driver_list[setThisDriver][0]
	if(ride_list[ride_k][6]=="Empty"):
		ride_list[ride_k][6] = driver_list[setThisDriver][0]
		if(driver_list[setThisDriver][4]=="[]"):
			dt=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
			newDT = (dt + timedelta(minutes=es_time))
			driver_list[setThisDriver][2]=ride_list[ride_k][3]
			driver_list[setThisDriver][3]=ride_list[ride_k][4]
			rval = str(dt)+" to "+ str(newDT)
			driver_list[setThisDriver][4]=str(rval)
		else:
			dt=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
			newDT = (dt + timedelta(minutes=es_time))
			driver_list[setThisDriver][2]=ride_list[ride_k][3]
			driver_list[setThisDriver][3]=ride_list[ride_k][4]
			rval = driver_list[setThisDriver][4]+"_,_"+str(dt)+" to "+ str(newDT)
			driver_list[setThisDriver][4]=str(rval)
	else:
		ride_list[ride_k][6]="Was not Empty"
	avail_driver.clear()
def scheduleDriver(ride_list,driver_list):
	for k, v in ride_list.items():
	    pickup_time, pick_lat_x, pick_lat_y, drop_lat_x, drop_lat_y, es_time, assigned_driver  = v
	    # print("\n\n\n")
	    # print("Ride Info: ",ride_list[k][0],ride_list[k][1], ride_list[k][2],ride_list[k][5])
	    getHighestScoreDriver(k, ride_list[k][0],ride_list[k][1], ride_list[k][2],ride_list[k][5])


print("Driver Info Before Scheduling:")
printAllDriver()
print("Ride Info Before Scheduling:")
prinAllRide()
print("\n")
scheduleDriver(ride_list,driver_list)
print("\n\n||||||||||||||||||||||||||||||      Scheduling      |||||||||||||||||||||||||||||||||||\n")
print("Ride Info After Scheduling:	")
prinAllRide()
print("\n||||||||||||||||||||||||||||||      Scheduling      |||||||||||||||||||||||||||||||||||\n\n")
# printAllDriver()


