#!/usr/bin/env python
"""get_pd_user_contact_methods"""

# Use the PagerDuty API to get User Contact Methods and put it in a csv  
# 1. Use list (csv) of user_id to
# 2. Get contact_methods associated with those user_id
# 3. Format as need in csv

import requests
import csv
import json

__VERSION__ = '1.0'
__BASEURL__ = 'https://api.pagerduty.com/users/{user_id}/contact_methods'

apiAuth = {
  "Accept": "application/vnd.pagerduty+json;version=2",
  "Authorization": "Token token= [PD API TOKEN]"            # Replace the PD API Token with the one provided by the customer/prospect
}


def get_user_phone_number(pduser_id):
    req = requests.get(__BASEURL__.format(user_id = pduser_id), headers = apiAuth)
    body = json.loads(req.text)

    for method in body['contact_methods']:
        if method['type'] == 'phone_contact_method':
            number = method['address']
            country_code = method['country_code'] 
            phone_number = str(country_code) + "-" + number
            return phone_number


def main():
    # Name the incoming CSV
    infile = csv.reader(open('[infile.csv]'))

    # Title the outgoing file to be created
    outfile = csv.writer(open('[outfile.csv]', 'w'))
    count = 0

    for row in infile:
        if count == 0:
            count += 1 
            continue

        name = row[0]
        email = row[1]
        teams = row[12]
        user_id = row[25]

        if user_id:
            phone_number = get_user_phone_number(user_id)
            if(phone_number != None):
                phone_split = phone_number.split('-')
                country_code = phone_split[0]
                number = phone_split[1]
                newrow = [
                    name,
                    email,
                    teams,
                    user_id,
                    country_code,
                    number
                ]
                print(newrow)
                outfile.writerow(newrow)

            else:
                country_code = '89'
                number = '5555555555'
                newrow = [
                    name,
                    email,
                    teams,
                    user_id,
                    country_code,
                    number
                ]
                print(newrow)
                outfile.writerow(newrow)

if __name__ == '__main__':
	main()