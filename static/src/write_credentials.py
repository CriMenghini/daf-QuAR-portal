import sys


user = sys.argv[1]
psw = sys.argv[2]
endpoint = sys.argv[3]

# Get the credentials from a txt file
with open('static/data/auth/credential.txt', 'w') as f:
    write_user = f.write(user + ' ')
    write_psw = f.write(psw + ' ')
    write_API = f.write(endpoint)