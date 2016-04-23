'''
Python methods for Tanda API.  You will need to install Requests: HTTP for Humans
pip install requests
http://docs.python-requests.org/en/master/
'''
import requests
import json

# Creates new token based on Tanda username, password and scope
# You can view your tokens here https://my.tanda.co/api/oauth/access_tokens
# View available scopes https://my.tanda.co/api/v2/documentation#header-scopes
def authenticate(username, password, scope = 'me'):
  url = 'https://my.tanda.co/api/oauth/token'
  body = {'username': username, 'password': password, 'scope': scope, 'grant_type': 'password'}
  headers = {'Cache-Control': 'no-cache'}
  data  = requests.post(url, params=body, headers=headers)
  token = str(json.loads(data.content).get('access_token'))
  return token

def get(extension, token):
  base_url = 'https://my.tanda.co/api/v2/'
  auth = 'Bearer ' + token
  headers = {'Cache-Control': 'no-cache', 'Authorization': auth}
  data = requests.get(base_url + extension, headers=headers)
  return data

def post(extension, params, token):
  base_url = 'https://my.tanda.co/api/v2/'
  auth = 'Bearer ' + token
  headers = {'Content-Type': 'application/json', 'Authorization': auth}
  requests.post(base_url + extension, params=params, headers=headers)

def put(extension, params, token):
  base_url = 'https://my.tanda.co/api/v2/'
  auth = 'Bearer ' + token
  headers = {'Content-Type': 'application/json', 'Authorization': auth}
  requests.put(base_url + extension, params=params, headers=headers)

def delete(extension, token):
  base_url = 'https://my.tanda.co/api/v2/'
  auth = 'Bearer ' + token
  headers = {'Content-Type': 'application/json', 'Authorization': auth}
  requests.delete(base_url + extension, headers=headers)


#Get a token which you will use to authenticate yourself
#Seperate scopes with spaces or leave blank for default scope
def get_users(username = 'kendricktan0814@gmail.com', password = 'tandahack2016'):
    token = authenticate(username, password, "user me")

    try:
        # Use token to get information about your userlist
        # And chucks it into json file
        users = json.loads(get("users", token).content)
        return users
    except:
        return None 

    #for user in users:
    #    print(user['photo'])
    #    print(user['name'])

    
    #Get a token which you will use to authenticate yourself
#Seperate scopes with spaces or leave blank for default scope
def get_users_json(username = 'kendricktan0814@gmail.com', password = 'tandahack2016'):
    token = authenticate(username, password, "user me")

    try:
        # Use token to get information about your userlist
        # And chucks it into json file
        users = get("users", token).content
        return users
    except:
        return None 

    #for user in users:
    #    print(user['photo'])
    #    print(user['name'])