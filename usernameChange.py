#!/usr/bin/python

#usernameChange
#
#this script is designed to take in a username and replace them with a new username with 
#the same teams, personal paging policy, permissions and contact methods
#
#More information on the public API can be found at:
#
#https://portal.victorops.com/public/api-docs.html
#
#Note, there is no way to include mobile devices
#
#usage:
# ./usernameChange.py <apiId> <apiKey> <current_username> <new_username> <boolean_is_admin>
#
#for example:
# ./usernameChange.py 32caec21 2527dc8405e99eb0840995ea51c0276f dumbolduser newsmartuser True
#
#this line tests with org "cordis-testing-arena", as well the username(s) listed:
#
#./usernameChange.py 5f026e9a 190fb368cdd27f5a7bf25d32a4a1436e chall newusernameperson True

import datetime
import requests
import sys
import json
import time


class org:
	"""This class contains the organization information and operates as the public api in this script"""
	
	#all org objects must have an apiId and apiKey
	def __init__(self, apiId, apiKey):
		self.apiId = apiId
		self.apiKey = apiKey
		self.genericHeader = {
							'Content-Type': 'application/json',
							'X-VO-Api-Id': apiId,
							'X-VO-Api-Key': apiKey,
							'Accept': 'application/json'
		}
		self.baseURL = 'https://api.victorops.com/api-public'

	#print org info
	def printOrg(self):
		print '\n--------------------------------------------------\n   ORG INFO:\n\n   API-ID:\t' + self.apiId +  '\n' + '   API-Key:\t' + self.apiKey + '\n\n--------------------------------------------------\n\n'
		pass

	def rmUser(self, newUsername, oldUsername):
		url = self.baseURL + '/v1/user/' + oldUsername

		body = {
			"replacement":newUsername
		}
		
		req = requests.delete(url, headers = self.genericHeader, data = json.dumps(body))

		if req.status_code != 200: #ERROR
			print "\n********\n","ERROR(",req.status_code,"): ", "\n\t",req.text,"\n********\n"
		else: #SUCCESS
			print "SUCCESS (", req.status_code, "\n"

		pass

	def postUser(self, first, last, username, email, admin):
		url = self.baseURL + '/v1/user'

		body = {
			"firstName": first,
			"lastName": last,
			"username": username,
			"email": "chall+ieurw3b@victorops.com",
			"admin": admin,
			"expirationHours": 24
		}

		req = requests.request('POST', url, headers = self.genericHeader, data = json.dumps(body))

		if req.status_code != 200: #ERROR
			print "\n********\n","ERROR(",req.status_code,"): ", "\n\t",req.text,"\n********\n"
		else: #SUCCESS
			print "SUCCESS (", req.status_code, "\n"

		pass

	def postPhones(self, username, phones):
		ids = []
		url = self.baseURL +'/v1/user/' + username + '/contact-methods/phones'

		for x in xrange(0, len(phones)):
			body = {
	  			"label": phones[x][0],
	  			"phone": phones[x][1],
	  			"rank": 0
			}
			print body

			req = requests.request('POST', url, headers = self.genericHeader, data = json.dumps(body))

			if req.status_code != 200: #ERROR
				print "\n********\n","ERROR(",req.status_code,"): ", "\n\t",req.text,"\n********\n"
			else: #SUCCESS
				print "SUCCESS (", req.status_code, "\n"
				#log contact id
				ids.append(json.loads(req.text)['id'])
		print ids
		return ids


	def postEmails(self, username, emails):
		url = self.baseURL +'/v1/user/' + username + '/contact-methods/emails'

		#check if only one email. If so, exit as this should already be included with the user creation
		#this is also why the index of emails starts at 1 instead of 0
		for x in xrange(1, len(emails)):
			body = {
	  			"label": emails[x][0],
	  			"email": emails[x][1],
	  			"rank": 0
			}

			req = requests.request('POST', url, headers = self.genericHeader, data = json.dumps(body))

			if req.status_code != 200: #ERROR
				print "\n********\n","ERROR(",req.status_code,"): ", "\n\t",req.text,"\n********\n"
			else: #SUCCESS
				print "SUCCESS (", req.status_code, "\n"

		pass

	def getUserInfo(self, username):
		print 'Getting User Information'

		url = self.baseURL+'/v1/user/' + username
		print url

		req = requests.get(url, headers = self.genericHeader)

		#print json.loads(req.text)

		return json.loads(req.text)

	def getContactInfo(self, username):
		print 'Getting user contact information'

		url = self.baseURL + '/v1/user/' + username + '/contact-methods'

		req = requests.get(url, headers=self.genericHeader)

		contactInfo = self.formatContactMethods(json.loads(req.text))

		#print json.loads(req.text)

		return contactInfo

	def formatContactMethods(self, contactInfo):
		phones = []
		emails = []
		#devices = [] can't post to user, not worth having right now

		for x in xrange(0,len(contactInfo['phones']['contactMethods'])):
			phones.append([contactInfo['phones']['contactMethods'][x]['label'],contactInfo['phones']['contactMethods'][x]['value']])

		for x in xrange(0,len(contactInfo['emails']['contactMethods'])):
			emails.append([contactInfo['emails']['contactMethods'][x]['label'],contactInfo['emails']['contactMethods'][x]['value']])

		# for x in xrange(0,len(contactInfo['devices']['contactMethods'])):
		# 	print contactInfo['devices']['contactMethods'][x]['label']
		# 	print contactInfo['devices']['contactMethods'][x]['value']
		
		devices = {"phones": phones, "emails": emails}
		return devices

	# def getEmail(self, username):
	# 	url = self.baseURL + '/v1/'

	# 	pass

	# def getContactID(self, username, method, labels):
	# 	url = self.baseURL + '/v1/user/' + username + '/contact-methods/' + method
	# 	id = []
	# 	for x in xrange(0,len(labels)):
	# 		req = requests.get(url, headers = self.genericHeader)
	# 		tmp = json.loads(req.text)['contactMethods']
	# 		for y in xrange(0, len(tmp)):
	# 			if labels[x][0] == tmp[y]['label']:
	# 				print tmp[y]['id']
	# 	pass

	def allTeamsHelper(self):
		print 'Getting list of all teams . . .\n'

		teamsArray = []

		url = self.baseURL + '/v1/team'

		req = requests.get(url, headers = self.genericHeader)

		temp = json.loads(req.text)

		for element in json.loads(req.text):
			if element['memberCount'] != 0:
				teamsArray.append(element['slug'])
				#print teamsArray[-1], " \n"

		return teamsArray


	def getTeamInfo(self):
		print 'Getting team members for all teams . . . \n'

		teamsArray = self.allTeamsHelper()
		url = self.baseURL+'/v1/team/'

		for x in xrange(0,len(teamsArray)):
			req = requests.get(url + teamsArray[x] + '/members', headers = self.genericHeader)
			#print json.loads(req.text)


	def getPolicy(self):
		pass



class user:
	#All user information is initialized to blank values
	pagingPolicy = []  #will be built as an array of JSON steps
	teams = []
	isAdmin = False
	phones = []
	emails = []
	first = ''
	last = ''

	#Initialization must have both the new and old usernames
	def __init__(self, username):
		self.username = username
		isAdmin = True

	#print all user information	
	def printUser(self):
		print '--------------------------------------------------\n\n   USER INFO\n\n   username:\t' + self.username + '\n\n--------------------------------------------------\n'
		pass

	def setTeams(self, teamArray):
		pass

	def setEmail(self, email):
		self.emails = email
		print 'user email set to ' , self.emails, '\n'

	def setPhones(self, phones):
		self.phones = phones
		print 'user phones set to ', self.phones, '\n'

	def setName(self, first, last):
		self.first = first
		self.last = last
		print 'user\'s name is ' + self.first, self.last + '\n'


	def setPolicy(self):
		pass


def main():
	#build objects and print them out
	organization = org(sys.argv[1], sys.argv[2])
	newUser = user(sys.argv[4])
	oldUser = user(sys.argv[3])

	#print initialized objects
	organization.printOrg()
	newUser.printUser()
	oldUser.printUser()

	#user information
	userInfo = organization.getUserInfo(oldUser.username)
	print userInfo

	#set userInfo
	#myUser.setEmail(userInfo['email'])
	newUser.setName(userInfo['firstName'], userInfo['lastName'])

	#get user contact information
	oldContactInfo = organization.getContactInfo(sys.argv[3])

	#set user contact information
	newUser.setEmail(oldContactInfo['emails'])
	newUser.setPhones(oldContactInfo['phones'])


	#get and print paging policy
	#organization.getContactID(newUser.username, 'emails', newUser.emails)


	#Change condition to acually post stuff, keep at false for testing
	if True:

		#create new user
		organization.postUser(newUser.first, newUser.last, newUser.username, newUser.emails[0][1], newUser.isAdmin)

		#post user contact information
		organization.postEmails(newUser.username, newUser.emails)
		organization.postPhones(newUser.username, newUser.phones)

		#Now get the id's

		#remove old user
		#organization.rmUser(oldUser.newName, oldUser.oldName)

		#organization.getTeamInfo()


	
	

if __name__ == "__main__":
	main()