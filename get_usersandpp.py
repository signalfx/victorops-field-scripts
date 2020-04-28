#!/usr/bin/python
import requests, json, time, pprint

#static urls
userPpUrl = "https://api.victorops.com/api-public/v1/profile/"

#headers
headersPub = {
	    'Content-type': "application/json",
	    'X-VO-Api-Id': "fb4d9889",
	    'X-VO-Api-Key': "a44738f03267f54c7a409e5bc6792869",
	    'cache-control': "no-cache",
	    }

def getUsers():
	#no rate limit check as this call is only made once
	res = requests.request("GET", 'https://api.victorops.com/api-public/v1/user', headers=headersPub)
	res.json()
	return json.loads(res.text)['users'][0]


def getContactMethods(user):
	t = time.process_time()

	url = "https://api.victorops.com/api-public/v1/user/" + user['username'] + "/contact-methods"

	response = requests.request("GET", url, headers=headersPub)

	#RATE LIMITS
	while response.status_code == 403:
		#wait until minute has passed
		wait = t + 5 - time.process_time()
		print('waiting ', str(wait), 'seconds. . .')
		time.sleep(wait)
		#reset timer to current time
		t = time.process_time()

		#retry
		response = requests.request("GET", url, headers=headersPub)

	if response.status_code == 200:
		#return list of usernames
		return json.loads(response.text)
		
	#NON-RATE LIMIT FAILURE
	else:
		print(user['username'] + ' - Failed to retrieve contactMethods - ' + str(response.status_code) + '\n----------\n')
		print(response.text)

def getUserPolicy(user):
	t = time.process_time()

	url = userPpUrl + user['username'] + '/policies'

	response = requests.request("GET", url, headers=headersPub)

	#RATE LIMITS
	while response.status_code == 403:
		#wait until minute has passed
		wait = t + 5 - time.process_time()
		print('waiting ', str(wait), 'seconds. . .')
		time.sleep(wait)
		#reset timer to current time
		t = time.process_time()

		#retry
		response = requests.request("GET", url, headers=headersPub)

	if response.status_code == 200:
		#return list of usernames
		policy = json.loads(response.text)
		del policy['_selfUrl']
		return policy
		
	#NON-RATE LIMIT FAILURE
	else:
		print(user['username'] + ' - Failed to retrieve pagingPolicy - ' + str(response.status_code))
		print(str(response.text) + '\n----------\n')

def main():
	#get all the users
	users = getUsers()
	#print(users)

	#attach contact methods and existing policy to all users
	for user in users:
	#	user['contactMethods'] = getContactMethods(user)
		user['pagingPolicy'] = getUserPolicy(user)
		print(user['username'])
		pprint.pprint(user['pagingPolicy'])
		#print '\t' + user['username'] + ' contact and paging information retrieved.'
  
if __name__== "__main__":
	main()
