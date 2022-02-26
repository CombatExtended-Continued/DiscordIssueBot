import requests
import base64
import json

my_application_id = "918936936377372752"


API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = input("Client ID")
CLIENT_SECRET = input("Client Secret")

def get_token():
  data = {
    'grant_type': 'client_credentials',
    'scope': 'applications.commands.update guilds'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  r.raise_for_status()
  return r.json()




g = get_token()
print(g)
my_credentials_token = g['access_token']

baseurl = "https://discord.com/api/v8"

url = f"{baseurl}/applications/{my_application_id}/commands"
print(url)

commands = dict(
  issue = dict(
    name = "issue",
    type = 1,
    description = "manage creating a GitHub issue",
    options = [
      dict(
        name = "start",
        description = "start creating a new GitHub issue",
        type = 1,
        options = [
          dict(
            name = "issue-name",
            description = "The name of the new issue",
            type = 3,
            required = True)]),
      dict(
        name = "complete",
        description = "mark an issue complete and ready for sending to GitHub",
        type = 1),
      dict(
        name = "submit",
        description = "submit the issue to GitHub",
        type = 1),
      dict(
        name = "add",
        description = "Add text to a pending issue",
        type = 1,
        options = [
          dict(
            name = "text",
            description = "The tet to add to the pending issue",
            type = 3,
            required = True)]),
      dict(
        name = "status",
        description = "Get the status of the pending issue",
        type = 1,
        ),
      dict(
        name = "repository",
        description = "Get or set the GitHub repositry where issues are opened",
        type = 2,
        options = [
          dict(
            name = "set",
            description = "set the repository",
            type = 1,
            options = [
              dict(
                name = "repository-name",
                description = "the name of the repository",
                type = 3,
                required = True)]),
          dict(
            name = "get",
            description = "get the repository",
            type = 1)]),

      dict(
        name = "role",
        description = "Get or set the role which has permission to create GitHub issues",
        type = 2,
        options = [
          dict(
            name = "set",
            description = "set the role",
            type = 1,
            options = [
              dict(
                name = "role-name",
                description = "the @role",
                type = 3,
                required = True)]),
          dict(
            name = "get",
            description = "get the role",
            type = 1)])]),
     
  AddToIssue = dict(
    name="AddToIssue",
    type=3,
    
  )
)  

# or a client credentials token for your app with the applications.commands.update scope
headers = {
    "Authorization": f"Bearer {my_credentials_token}"
}

import sys
import time
if len(sys.argv) == 1 or sys.argv[1] == 'setup':

  #r = requests.put(url, headers=headers, json=json)
  r = requests.get(url, headers=headers)
  if r.ok:
    current_commands = json.loads(r.text)
    current_command_map = {}
    print("Existing Commands")
    print("-"*20)

    for command in current_commands:
      print(f"Name: {command['name']}")
      if command['name'] not in commands:
        print("Removing obsolete command")
        r = requests.delete(f"{url}/{command['id']}", headers=headers)
        if not r.ok:
          print(r.text)
          raise SystemExit(1)
        time.sleep(1)
      else:
        current_command_map[command['name']] = command
    for command, nc in commands.items():
      if command in current_command_map:
        cc = current_command_map[command]
        print(f"Updating {command}")
        id = cc['id']
        r = requests.patch(f"{url}/{id}", headers=headers, json=nc)
        if not r.ok:
          print(r.text)
          raise SystemExit(2)
        time.sleep(5)
      else:
        print(f"Creating new command {command}")
        r = requests.post(url, headers=headers, json=nc)
        if not r.ok:
          print(r.text)
          raise SystemExit(3)
        time.sleep(5)

  else:
    print(r)
    print(r.text)


else:
  method = sys.argv[1]
  suburl = sys.argv[2]
  if method in ['put', 'patch', 'post']:
    body = json.loads(input())
    r = getattr(requests, method)(f"{baseurl}{suburl}", headers=headers, json=body)
  else:
    r = getattr(requests, method)(f"{baseurl}{suburl}", headers=headers)
  print(r.ok)
  if r.ok:
    print(json.dumps(indent=4, obj=json.loads(r.text)))
  else:
    print(r.text)
