#!/usr/bin/python
#python3 - updated 4.5.19

import requests
import sys
import json
import time

def getUsers(orgHead):
	t = time.perf_counter()

	req = requests.get('https://api.victorops.com/api-public/v1/user', headers = orgHead)

	#RATE LIMITS
	while req.status_code == 403:
		#wait until minute has passed
		print(('waiting ', str(t + 60 - time.perf_counter()), 'seconds. . .'))
		time.sleep(t + 60 - time.perf_counter())
		#reset timer to current time
		t = time.perf_counter()

		#retry
		req = requests.get('https://api.victorops.com/api-public/v1/user', headers=orgHead)

	if req.status_code == 200:
		#return list of usernames
		usernames = []
		get = json.loads(req.text)['users'][0]
		for k in get:
			usernames.append(k['username'])
		return usernames
		
	#NON-RATE LIMIT FAILURE
	else:
		print('Failed to get usernames . . .')

def deleteAllUsers(orgHead, users, repU):
	for u in users:
		if u == repU:
			continue
		else:
			deleteUser(orgHead, u, repU)

def deleteUser(orgHead, delU, repU):
	t = time.perf_counter()
	body = {
		'replacement':repU
	}

	req = requests.delete('https://api.victorops.com/api-public/v1/user/' + delU, headers=orgHead, data = json.dumps(body))

	#RATE LIMITS
	while req.status_code == 403:
		#wait until minute has passed
		print(('waiting ', str(t + 60 - time.perf_counter()), 'seconds. . .'))
		time.sleep(t + 60 - time.perf_counter())
		#reset timer to current time
		t = time.perf_counter()

		#retry
		req = requests.delete('https://api.victorops.com/api-public/v1/user/' + delU, headers=orgHead, data = json.dumps(body))

	if req.status_code == 200:
		print(('\t 200 - ' + delU + ' was deleted'))
		
	#NON-RATE LIMIT FAILURE
	else:
		print(('Failed to get usernames . . .\n\t\t' + str(json.loads(req.text))))

def getTeams(orgHead):
	t = time.perf_counter()

	req = requests.get('https://api.victorops.com/api-public/v1/team', headers = orgHead)

	#RATE LIMITS
	while req.status_code == 403:
		#wait until minute has passed
		print(('waiting ', str(t + 60 - time.perf_counter()), 'seconds. . .'))
		time.sleep(t + 60 - time.perf_counter())
		#reset timer to current time
		t = time.perf_counter()

		#retry
		req = requests.get('https://api.victorops.com/api-public/v1/team', headers=orgHead)

	if req.status_code == 200:
		#return list of usernames
		teams = []
		get = json.loads(req.text)
		for k in get:
			teams.append([k['slug'], k['name']])
		return teams
		
	#NON-RATE LIMIT FAILURE
	else:
		print('Failed to get usernames . . .')

def deleteTeam(orgHead, team):
	t = time.perf_counter()

	req = requests.delete('https://api.victorops.com/api-public/v1/team/' + team[0], headers=orgHead)

	#RATE LIMITS
	while req.status_code == 403:
		#wait until minute has passed
		print(('waiting ', str(t + 60 - time.perf_counter()), 'seconds. . .'))
		time.sleep(t + 60 - time.perf_counter())
		#reset timer to current time
		t = time.perf_counter()

		#retry
		req = requests.delete('https://api.victorops.com/api-public/v1/team/' + team[0], headers=orgHead)

	if req.status_code == 200:
		print(('\t 200 - ' + team[1] + ' was deleted'))
		
	#NON-RATE LIMIT FAILURE
	else:
		print(('Failed to delete ' + team[1] + ' . . .\n\t\t' + str(json.loads(req.text))))	

def deleteAllTeams(orgHead, teams):
	for t in teams:
		deleteTeam(orgHead, t)

def printList(l, num=False):
	for i, val in enumerate(l):
		print((str(i) + '. ' + str(val)))

def main():
	userList = []
	userIn = int(eval(input('Enter \'0\' to use vops-jdsouza, enter anything else to set other VO account.\n')))
	
	# Set Default VictorOps Account (i.e. Test Account)
	apiAuth = {
			'Content-Type': 'application/json',
			'X-VO-Api-Id': '[API ID]', 
			'X-VO-Api-Key': '[API KEY]',
			'Accept': 'application/json'
		}
	if userIn == 0:
		apiAuth = {
			'Content-Type': 'application/json',
			'X-VO-Api-Id': '[API ID]', 
			'X-VO-Api-Key': '[API KEY]',
			'Accept': 'application/json'
		}
	else:
		apiAuth = {
			'Content-Type': 'application/json',
			'X-VO-Api-Id': str(userIn),
			'X-VO-Api-Key': '',
			'Accept': 'application/json'
		}
		#userIn = input('Enter the api key:\n')
		#apiAuth['X-VO-Api-Key'] = str(userIn)

	while True:
		userIn = int(eval(input('\nEnter a number for,\n\t1. Get and Print Users\n\t2. Delete Users\n\t3. Get and Print Teams\n\t4. Delete Teams\n\t5. Nuke\n\t6. SUPERNUKE\n\t0. Exit\n>')))
		#GET USERS
		if userIn == 1:
			userList = getUsers(apiAuth)
			printList(userList)
		#DELETE ALL USERS
		elif userIn == 2:
			printList(userList)
			userIn = eval(input('\nSelect one user from above to keep:'))
			deleteAllUsers(apiAuth, userList, userList[userIn])
		#GET TEAMS
		elif userIn	== 3:
			teamList = getTeams(apiAuth)
			printList(teamList)
		#DELETE TEAMS
		elif userIn == 4:
			deleteAllTeams(apiAuth, teamList)
		elif userIn ==5:
			printList(userList)
			userIn = int(eval(input('\nSelect one user from above to keep:')))
			deleteAllUsers(apiAuth, userList, userList[userIn])
			deleteAllTeams(apiAuth, teamList)
		elif userIn == 6:
			userList = getUsers(apiAuth)
			teamList = getTeams(apiAuth)
			printList(userList)
			userIn = int(eval(input('\nSelect one user from above to keep:')))
			deleteAllTeams(apiAuth, teamList)
			deleteAllUsers(apiAuth, userList, userList[userIn])
		elif userIn == 0:
			sys.exit()
		else:
			print('invalid input')

if __name__ == '__main__':
	main()
