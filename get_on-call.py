#!/usr/bin/python
import requests, json, time, pprint

#static urls
org_oncall_Url = "https://api.victorops.com/api-public/v1/oncall/current"

#Update API Credentials
headersPub = {
	    'Content-type': "application/json",
	    'X-VO-Api-Id': "API ID",
	    'X-VO-Api-Key': "API KEY",
	    'cache-control': "no-cache",
	    }

# Dumps all On-Call users for an org
def getOnCall():
	# no rate limit check since this call only needs to be made once
	response = requests.request("GET", org_oncall_Url, headers=headersPub)
	response.json()
	return json.loads(response.text)

# Display the on-call users for a specifc team
# def teamOnCall(team):



def main():
	#get On-Call
	oncall = getOnCall()
	pprint.pprint(oncall)
	print('Team:', oncall['teamsOnCall'][1]['team']['name'])
	print('Escalation Policy:', oncall['teamsOnCall'][1]['oncallNow'][0]['escalationPolicy']['name'])
	print('User:', oncall['teamsOnCall'][1]['oncallNow'][0]['users'][0]['onCalluser']['username'], '\n')
	print('Team:', oncall['teamsOnCall'][2]['team']['name'])
	print('Escalation Policy:', oncall['teamsOnCall'][2]['oncallNow'][0]['escalationPolicy']['name'])
	print('User:', oncall['teamsOnCall'][2]['oncallNow'][0]['users'][0]['onCalluser']['username'], '\n')

if __name__== "__main__":
	main()