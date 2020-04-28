#!/usr/bin/python

import os
import sys
import time
import datetime
import json
import requests
import time

def getIncidents(orgHead):
    t = time.clock()

    req = requests.get('https://api.victorops.com/api-public/v1/incidents', headers = orgHead)

    #RATE LIMITS
    while req.status_code == 403:
        #wait until minute has passed
        print 'waiting ', str(t + 60 - time.clock()), 'seconds. . .'
        time.sleep(t + 60 - time.clock())
        #reset timer to current time
        t = time.clock()

        #retry
        req = requests.get('https://api.victorops.com/api-public/v1/incidents', headers=orgHead)

    if req.status_code == 200:
        return json.loads(req.text)


def main():

    orgHead = {
        'Content-Type': 'application/json',
        'X-VO-Api-Id': '[API ID]',			#enter your VictorOps API ID here
        'X-VO-Api-Key': '[API KEY]',		#enter your victorOps API Key here
        'Accept': 'application/json'
    }

    incidents = getIncidents(orgHead)
    for i in incidents['incidents']:
        print(json.dumps(i))   

if __name__ == '__main__':
            main()