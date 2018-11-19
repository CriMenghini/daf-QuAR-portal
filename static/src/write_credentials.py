import sys
import os

user = os.environ['user']
psw = os.environ['psw']
endpoint = os.environ['API']

# Get the credentials from a txt file
with open('static/data/auth/credential.txt', 'w') as f:
    write_user = f.write(user + ' ')
    write_psw = f.write(psw + ' ')
    write_API = f.write(endpoint)
