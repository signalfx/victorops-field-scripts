import requests, json

#ADD USER CREDENTIALS HERE
username = "goodman"
password = "heydemo123"
org = "victorops-demo"


url = "https://" + username + ":" + password + "@portal.victorops.com/api/v1/org/" + org + "/reports/postmortems"

payload = {}
headers = {
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'en-US,en;q=0.9',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
  'content-type': 'application/json; charset=UTF-8',
  'accept': '*/*',
  'referer': 'https://portal.victorops.com/reports/victorops-demo/post-incidents',
  'authority': 'portal.victorops.com'
}

response = requests.request("GET", url, headers=headers, data = payload, files = files)
pir = json.loads(response.text)

for r in pir:
    if r['owner'] == username:
        url = "https://" + username + ":" + password + "@portal.victorops.com/api/v1/org/" org + "/reports/postmortems/" + r['token']
        response = requests.request("DELETE", url, headers=headers, data = payload)
        if response.status_code == 200:
            print("deleted report: " + r['title'])
        else:
            print("something broke, didn't delete report: " + r['title'])
