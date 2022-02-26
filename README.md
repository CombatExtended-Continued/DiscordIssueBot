# Discord Github Issue Bot

## About
This repository hosts the server-side code for the Discord -> GitHub issue creation bot.

## Requirements
Basic requirements are python 3.10 or later, the github-cli, python-twisted, and libsodium (with python bindings)

## Setup
### Server-Side
Get an SSL certificate from Let's Encrypt
run `python3.10 -m dib` which will listen on port 8080.  
Use a reverse proxy to wrap that in an SSL connection, or configure `dib/__main__.py` to listen on SSL itself.
### GitHub-Side
Create a bot account on github and configure a personal access token for it.  Give it permission to create issues on the target repository
Use the `gh` command on the server hosting the `Server-Side` to login as the bot.
### Discord-Side
Create a new discord app via the discord developers site
Copy the public key from the new app and put it in `$HOME/pubkey`
Note the discord app UID

Update the application id in `makecommand.py` to point to the new application
Run `makecommand.py` provide the client id and client secret when prompted.
Point the endpoint URL from the discord application portal to the domain hosting the `Server-Side`

### Discord Server-side

Add the new discord application to the server
Add a role to manage access to the application commands
Use the `/issue * ` commands to point it at a github repository and set the authorized role.
