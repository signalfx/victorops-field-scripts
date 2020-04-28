#!/usr/bin/env python
"""onboard_victorops_user"""
import sys
import argparse
import requests
import time
try:
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
import csv
import json

__VERSION__ = '1.0'
__BASEURL__ = 'https://stapi.victorops.com'     #Should this be staging or production?

def main():
    parser = VoParser(prog='onboard_victorops_user3.0')
    setup_parser(parser)
    args = parser.parse_args()
    data = handle_args(args)
    
    # Get current team slugs
    teams = get_teams(args.apiId, args.apiKey)
    # Create new teams, return slugs
    data = handle_teams(args.apiId, args.apiKey, data, teams)
    # Post the users to VO
    post_to_victorops(args.apiId, args.apiKey, json.loads(data))

def handle_args(args):
    """ Routes args by format """
    if hasattr(args, 'csv'):
        return handle_csv(args.csv)
    else:
        return args_to_json(args)

def get_teams(apiId, apiKey):
    head = {'Content-type': 'application/json', 'Accept': 'application/json',
            'X-VO-API-ID': apiId, 'X-VO-API-KEY': apiKey}
    req = requests.get(__BASEURL__+'/api-public/v1/team', headers = head)
    teams = req.json()
    # Create a dictionary of team names and slugs
    team_names_and_slugs = {}

    for team in teams:
        team_names_and_slugs[team['name']]=team['slug']
    
    print('TEAMS AND SLUGS:')
    for element in team_names_and_slugs:
        print(element+' : '+team_names_and_slugs[element])
    
    return team_names_and_slugs

def handle_teams(apiid, apikey, data, teams):
    # Check for teams that don't already exist, create them, add them to the teams object
    team_names_and_slugs = get_teams(apiid, apikey)
    #print("Existing Teams: ", team_names_and_slugs, '\n')
    # Pull all team names from user data
    user_teams = [] 
    for u in json.loads(data)['users']:
        for t in u['teams']:
            # deduplicate teams in csv
            if t['team'] not in user_teams:
                user_teams.append(t['team'])
    print('\nUSER TEAMS:\n',user_teams)
    
    #create teams that don't exist yet and swap team names with team slugs for all new/existing teams
    teams = {}
    for t in user_teams:
        #if a team in the data doesn't already exist
        if t not in team_names_and_slugs.keys():
            #create the team
            teams[t] = post_team(apiid, apikey, t)
            #in data, replace team names with slugs
            data = data.replace(t, teams[t]['slug'])
            print('CREATED:\n',t,':',teams[t]['slug'])
        else:
            print('RETREIVED:\n', t, ':', team_names_and_slugs[t])
            data = data.replace(t,team_names_and_slugs[t])
    #return updated data with team slugs for all teams which now exist
    return data

def post_team(apiId, apiKey, name):
    head = {'Content-type': 'application/json', 'Accept': 'application/json',
            'X-VO-API-ID': apiId, 'X-VO-API-KEY': apiKey}
    req = requests.request('POST',__BASEURL__+'/api-public/v1/team', data = json.dumps({"name":name}), headers = head)
    return json.loads(req.text)

def post_to_victorops(apiId, apiKey, data):
    # Attempts to post JSON payload to VictorOps
    head = {'Content-type': 'application/json', 'Accept': 'application/json',
            'X-VO-API-ID': apiId, 'X-VO-API-KEY': apiKey}
    body = ''
    count_users = 0
    # continually pop off users from data into the body field until done
    while data['users']:
        count_users += 1
        body = ''
        body += json.dumps(data['users'].pop()) + ', '
        body = body[:-2]

        # Add User
        req = requests.request('POST',__BASEURL__+'/api-public/v1/user', data=body, headers=head)
        if req.status_code != 200:
            print('ERROR ADDING USER:\n', req.text,'\n')
        else:
            print('USER', json.loads(body)['username'], 'ADDED\n-------------------\n')
                
        # Add Contact Method Phone Number
        json_body = json.loads(body)
        phone_body = json.dumps({'phone': '+' + json_body['countryCode'] + json_body['phone'], 'label': 'Default', 'rank': 0})
        #print(phone_body)
        req = requests.request('POST',__BASEURL__+'/api-public/v1/user/'+json_body['username']+'/contact-methods/phones',data=phone_body, headers = head)
        if req.status_code != 200:
            print('ERROR ADDING PHONE:\n',req.text,'\n')
        else:
            print('PHONENUMBER', json.loads(phone_body)['phone'], 'ADDED\n-------------------\n')
        
        # Add Users to new team
        for t in json_body['teams']:
            #print(t)
            team_body=json.dumps({'username':json_body['username']})
            req = requests.request('POST',__BASEURL__+'/api-public/v1/team/'+t['team']+'/members',data=team_body, headers = head)    
            if req.status_code != 200:
                print('ERROR ADDING TO TEAM:\n',req.text,'\n')
            else:
                print('USER', json_body['username'], 'ADDED TO TEAM', t['team'],'\n-------------------\n')
            time.sleep(1.2)
            #print('POST',__BASEURL__+'/api-public/v1/team/'+t['team']+'/members')
            #print(team_body)
        
        # Sleep to avoid rate limiting on the public apis 
        time.sleep(1.2)

def args_to_json(args):
    teams = []        
    for team in args.teams.split(','):
        teams.append({'team': team})
    json_object =  json.dumps({"users": [{'username': args.username, 'email': args.email,
                                  'firstName': args.firstName, 'lastName': args.lastName,
                                  'phone': args.phone,'teams': teams}]})
    return json_object

def handle_csv(infile):
    with open(infile, 'rt') as csvfile:
        users = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            teams = []
            #print row
            for team in row['teams'].split(','):
                teams.append({'team': team.strip()})
            row['teams'] = teams
            userjson = {'username': row['username'], 'email': row['email'],
                        'firstName': row['firstName'], 'lastName': row['lastName'],
                        'countryCode': row['countryCode'],'phone': row['phone'],'teams': row['teams']}
            users.append(userjson)
        return json.dumps({'users': users})            

def setup_parser(parser):
    subparsers = parser.add_subparsers(help='Import users from:')
    parser.add_argument('-v', '-version', action='version', version=__VERSION__)
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--apiId', required=True, help='e.g. --apiId  abcdef12')
    parent_parser.add_argument('--apiKey', required=True, help='e.g. --apiKey  abcdef12')
    csv_parser = subparsers.add_parser('csv', parents=[parent_parser], help='csv file')
    csv_parser.add_argument('-f', '--file', required=True, dest='csv', help='e.g. -f <foo.csv>')
    return parser

class VoParser(argparse.ArgumentParser):
    """ Adds better error handling to standard argument parser """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

if __name__ == "__main__":
    main()
