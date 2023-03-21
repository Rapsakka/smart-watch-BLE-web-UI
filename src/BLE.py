import sys
from bluepy import btle
import sqlite3
import time

def create_table():
	con = sqlite3.connect('Hiking.db')
	cursor = con.cursor()
	
	tableCall = cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Hiking' ''')
	
	if tableCall.fetchone()[0] == 0:
		print("Table not found creating...")
		table = "CREATE TABLE Hiking ( start INTEGER PRIMARY KEY, end INTEGER, steps INTEGER, distance INTEGER, calories REAL, temperature REAL);"	
		cursor.execute(table)
	else:	#else do nothing 
		print("Table has been already created")
	cursor.close()
	
def insert_data(iData):	
	con = sqlite3.connect('Hiking.db')
	cursor = con.cursor()
	
	sta = str( iData[1] ) 
	end = str ( iData[2] )
	stp = str ( iData[3] )
	dist = str ( iData[4] )
	cal = str ( iData[5] )
	temp = str( iData[6] )
	
	query= "SELECT EXISTS(SELECT 1 FROM Hiking WHERE start={}) LIMIT 1".format(sta)
	#query = "SELECT COUNT(*) FROM Hiking WHERE start = {};".format(sta)
	
	check = cursor.execute(query)
	result = check.fetchone()[0]
	if  result == 0: 
		txt = "INSERT INTO Hiking (start,end,steps,distance,calories,temperature) VALUES({},{},{},{},{},{});".format(sta,end,stp,dist,cal,temp)
		cursor.execute(txt) 
		print("new entry to DB added")
	if result == 1 : 
		txt ="UPDATE Hiking SET end = {}, steps = {}, distance = {}, calories = {}, temperature = {} WHERE start == {};".format(end,stp,dist,cal,temp,sta)
		cursor.execute(txt) 
		print("updated previous value")
	con.commit()
	con.close()
	
def readBLE():
	address = "94:b5:55:C8:EA:B6"

	servUUID ="bc2fa7bd-60cd-46f6-bf7f-3ea374234003" 
	charUUID ="73c351d2-ee74-4f5e-b5d3-03a56553fed4"
	ret = "ERROR"
	try:
		p = btle.Peripheral(address)
		svc = p.getServiceByUUID(servUUID ) 
		dat = svc.getCharacteristics( charUUID )[0]
		ret = str( dat.read() )
		if ret is not None:
			ret = ret[2:-1]
	except:
		"""print("BLE connection error")"""
	return ret


def routine():
	print("starting BLE listening")
	dat = " "
	while True:
		time.sleep(5)
		dt = readBLE() 
		if dt != dat and dt is not None and len(dt) > 1:
			if dt != "ERROR":
				nData = list( dt.split(",") )
				insert_data(nData)
		if dt is not None:
			dat = dt
		
		
		

"""
print("starting BLE listening")

def routine2():
		dt = readBLE() 
		if dt is not None and len(dt) > 1:
			print( dt )
			if dt != "ERROR":
				nData = list( dt.split(",") )
				insert_data(nData)
			else:
				print("BLE error 2")

"""
create_table()
routine()
"""
while True:
	time.sleep(10)
	routine2()
"""
	
	
	
	
