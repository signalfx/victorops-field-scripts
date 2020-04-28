#!/usr/bin/python
import requests, json, time

#DEFINE PAGING POLICY

policy = {
    "steps": [
        {
		    "index": 0,
		    "timeout": 5,
		    "rules": [
		        {
		            "index": 0,
		            "type": "phone"
		        },
		        {
		        	"index": 1,
		        	"type": "email" # defaults to push if not activated
		        },
		        {
		        	"index": 2,
		        	"type": "push"
		        },
		        {
		        	"index": 3,
		        	"type": "sms"
		        }
		    ]
		},
		{
			"index": 1,
		    "timeout": 10,
		    "rules": [
		        {
		            "index": 0,
		            "type": "sms"
		        },
		        {
		        	"index": 1,
		        	"type": "phone"
		        }
		    ]
		},
		{
			"index": 2,
		    "timeout": 15,
		    "rules": [
		        {
		            "index": 0,
		            "type": "push"
		        },
		        {
		        	"index": 1,
		        	"type": "email" # defaults to push if not activated
		        }
		    ]
		}
    ]
}

#static urls
userPpUrl = "https://api.victorops.com/api-public/v1/profile/"

#Update API Credentials
headersPub = {
	    'Content-type': "application/json",
	    'X-VO-Api-Id': '[API ID]',
	    'X-VO-Api-Key': '[API KEY]',
	    'cache-control': "no-cache",
	    }

def getUsers():
	#no rate limit check as this call is only made once
	res = requests.request("GET", 'https://api.victorops.com/api-public/v1/user', headers=headersPub)
	res.json()
	return json.loads(res.text)['users'][0]

def clearPp(user):
	#set timer for rate limit
	t = time.process_time()

	# print user['pagingPolicy']

	#create copy of new dict to return at the end
	newPolicy = dict(user['pagingPolicy'])

	#for each step in policy
	for step in reversed(user['pagingPolicy']['steps']):
		s = step['index']
		for rule in reversed(step['rules']):
			#get step and 
			r = rule['index']

			#can't delete rule zero and step zero of policy, leave it there
			if r + s == 0:
				break

			#define url
			url = userPpUrl + user['username'] + "/policies/" + str(s) + "/" +str(r)

			#make DELETE request
			response = requests.request("DELETE", url, headers=headersPub)

			#handle rate limits
			while response.status_code == 403:
				#wait until minute has passed
				wait = t + 5 - time.process_time()
				print('waiting ', str(wait), 'seconds. . .')
				time.sleep(wait)
				#reset timer to current time
				t = time.process_time()

				#retry
				response = requests.request("GET", url, headers=headersPub)

			#if success, update return policy
			if response.status_code == 200:
				#update policy
				del newPolicy['steps'][s]['rules'][r]
		
			#NON-RATE LIMIT FAILURE
			else:
				print(user['username'] + ' - Failed to delete rule ' + r + 'of step ' + s + '. - ' + str(response.status_code))
				print(str(response.text) + '\n----------\n')
		#update return policy
		del newPolicy['steps'][s]
	#return copy of new policy to update user
	return newPolicy

def setUserPp(user, policy):

	for step in policy['steps']:
		#first step needs a PUT
		if step['index'] == 0:
			putPpStep(user, policy['steps'][0])

		#if more than one step, post them as new steps.
		else:
			postPpStep(user, step)


def putPpStep(user, step):

	#start timer
	t=time.process_time()
	
	url = userPpUrl + user['username'] + "/policies/0"

	#build payload
	payload = buildUserStep(user, step)

	response = requests.request("PUT", url, data=json.dumps(step), headers=headersPub)

	#RATE LIMITS
	while response.status_code == 403:
		#wait until minute has passed
		wait = t + 5 - time.process_time()
		print('waiting ', str(wait), 'seconds. . .')
		time.sleep(wait)
		#reset timer to current time
		t = time.process_time()

		#retry
		response = requests.request("PUT", url, data=json.dumps(payload), headers=headersPub)

	if response.status_code == 200:
		#return list of usernames
		user['pagingPolicy']['steps'] += step
		print(user['username'] + ' - 200 - first policy step set.')
		return response.status_code

	else:
		print(step)
		print(url)
		print(response.text)
		print(response.status_code)
		return False

def postPpStep(user, step):
	#stat timer
	t=time.process_time()

	payload = buildUserStep(user, step)

	url = userPpUrl + user['username'] + "/policies"

	response = requests.request("POST", url, data=json.dumps(step), headers=headersPub)

	#RATE LIMITS
	while response.status_code == 403:
		#wait until minute has passed
		wait = t + 5 - time.process_time()
		print('waiting ', str(wait), 'seconds. . .')
		time.sleep(wait)
		#reset timer to current time
		t = time.process_time()

		#retry
		response = requests.request("POST", url, data=json.dumps(step), headers=headersPub)

	if response.status_code == 200:
		#return list of usernames
		print(user['username'] + ' - 200 - policy step [' + str(step['index']) + '] set.') 
		user['pagingPolicy']['steps'] += step
		
	#NON-RATE LIMIT FAILURE
	else:
		print(user['username'] + ' - Failed to post paging policy - ' + str(response.status_code) + '\n----------\n')
		print(response.text)
		print(step)

def buildUserStep(user, step):
	#This function crafts the user-specific paging policy step to include the first 
   #	{
   #          "index": 0,
   #          "timeout": 15,
   #          "rules": [
   #              {
   #                  "index": 0,
   #                  "type": "push"
   #              }
   #          ]
   #      }
	payload = dict(step)
	del payload['index']
	for rule in payload['rules']:
		#check to verify that user actually has a phone number as their contact methods.
		if (rule['type'] == 'sms' or rule['type'] == 'phone') and (len(user['contactMethods']['phones']['contactMethods']) > 0):
			#there is a phone number in the user profile, but is it verified?
			for number in user['contactMethods']['phones']['contactMethods']:
				if number['verified'] == 'verified':
					rule['contact'] = {
						'type': 'Phone',
						'id': user['contactMethods']['phones']['contactMethods'][0]['id']
					}
					break
				else:
					print(user['username'] + ' - ' + number['value'] + ' is not verified, defaulting to email.')
					rule['type'] = "email"
					rule['contact'] = {
						'type': 'email',
						'id': user['contactMethods']['emails']['contactMethods'][0]['id']
					}
		#if type is email or there are no phone numbers present default to email
		elif rule['type'] == 'email' or ((rule['type'] == 'sms'or rule['type'] == 'phone') and (len(user['contactMethods']['phones']['contactMethods']) == 0)):
			#if email is not verified, default to push
			if len(user['contactMethods']['phones']['contactMethods']) == 0:
				print(user['username'] + ' - no phone number is present, defaulting to email.') 
			for email in user['contactMethods']['emails']['contactMethods']:
				if email['verified'] == 'verified':
					rule['contact'] = {
						'type': 'email',
						'id': user['contactMethods']['emails']['contactMethods'][0]['id']
					}
				#if the email is not verified, default to push
				else:
					print(user['username'] + ' - ' + email['value'] + ' is not verified, defaulting to push.')
					rule['type'] = 'push'
		#this would be for a push, shouldn't need to add a contact id, since it goes to all devices
		else:
			print('should be a push')
			pass
	return payload

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

	#attach contact methods and existing policy to all users
	for user in users:
		user['contactMethods'] = getContactMethods(user)
		user['pagingPolicy'] = getUserPolicy(user)
		#print '\t' + user['username'] + ' contact and paging information retrieved.'

	#print users

	#clear existing paging policies
	for user in users:
		user['pagingPolicy'] = clearPp(user)
		#print '\t' + user['username'] + ' paging policy cleared.'

	#set template policy for all users
	for user in users:
		setUserPp(user, policy)
		#print '\t' + user['username'] + ' paging policy set.'
  
if __name__== "__main__":
	main()
