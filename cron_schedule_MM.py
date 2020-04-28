#!/usr/bin/python

import json, requests, pprint, time, datetime, sys

#GLOBALS

#SET API CREDENTIALS
auth = {
	'apiId': 'API ID',
	'apiKey': 'API KEY'
}

#Start Maintenance Mode
def startMaintenanceMode(auth, routingKeys, purpose):
	url = "https://api.victorops.com/api-public/v1/maintenancemode/start"

	payload = {
  		"type": "RoutingKeys",
  		"names": routingKeys,
  		"purpose": purpose
	}

	headers = {
	    'Accept': "application/json",
	    'X-VO-Api-Id': auth['apiId'],
	    'X-VO-Api-Key': auth['apiKey'],
	    'Content-Type': "application/json",
	    }

	response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

	if response.status_code == 200:
		return json.loads(response.text)
	else:
		return False


#End Maintenance Mode
def endMaintenanceMode(auth, id):
	print(id)
	url = "https://api.victorops.com/api-public/v1/maintenancemode/"+id+"/end"

	headers = {
	    'Accept': "application/json",
	    'X-VO-Api-Id': auth['apiId'],
	    'X-VO-Api-Key': auth['apiKey'],
	    }

	response = requests.request("PUT", url, headers=headers)

	if response.status_code == 200:
		return json.loads(response.text)
	else:
		return False


#Get Maintenance Mode Status
def getMaintenanceMode(auth):
	url = "https://api.victorops.com/api-public/v1/maintenancemode"

	headers = {	
	    'Accept': "application/json",
	    'X-VO-Api-Id': auth['apiId'],
	    'X-VO-Api-Key': auth['apiKey'],
	    }

	response = requests.request("GET", url, headers=headers)

	if response.status_code == 200:
		return json.loads(response.text)
	else:
		return False

#Helper function to retrieve a list of all maintenance mode id's whose targets match the specified array of routing keys.
def getMmIds(auth, routingKeys):
	current = getMaintenanceMode(auth)
	ids = []

	#determine if any active sessions using listed routing keys
	for mm in current['activeInstances']:
		if set(mm['targets'][0]['names']) == set(routingKeys):
			print(mm['instanceId'])
			ids.append(mm['instanceId'])
	return ids


#Main
mmIds = []

while True:
	userIn = eval(input('\nEnter a number for,\n\t1. Start Maintenance Mode\n\t2. Stop Maintenance Mode\n\t3. Get Maintenance Mode Status\n\t4. Exit\n>'))
	#START MM
	if userIn == 1:
		userIn = input('\nEnter a list of comma separated routing keys (i.e. routingkey1,routingkey2,routingkey3):\n')
		rks  = userIn.split(',')
		userIn = input('\nEnter a maintenance mode purpose:\n')
		purpose = userIn
		req = startMaintenanceMode(auth, rks, purpose)
		if req:
			mmIds += req
		else:
			print(("Failed to startMaintenanceMode for routing keys"+str(rks)+", and purpose "+purpose))

	#STOP MM
	elif userIn == 2:
		userIn = eval(input('\nEnd Maintenance Mode by:\n\t1. Routing Key List\n\t2. Maintenance Mode Session Id\n'))
		#END BY ROUTING KEY
		if userIn == 1:
			userIn = input('\nEnter a list of comma separated routing keys (i.e. routingkey1,routingkey2,routingkey3):\n')
			rks = userIn.split(',')
			#Find MM ID
			ids = getMmIds(auth, rks)
			print(ids)
			if ids > 0:
				for mm in ids:
					endMaintenanceMode(auth, mm)
			else:
				print(('No Maintenance Mode sessions could be found for the routing key list '+rks+'.'))
		#END BY ID
		elif userIn == 2:
			userIn = input('\nEnter the Maintenance Mode session ID:\n')
			req = endMaintenanceMode(auth, userIn)
		#NON VALID ENTRY
		else:
			print("\nEnter a valid number.\n")

	#GET MM Status
	elif userIn	== 3:
		print((getMaintenanceMode(auth)))

	#EXIT
	elif userIn == 4:
		sys.exit()
	else:
		print('\ninvalid input\n')













