#!/usr/bin/env python3
import rest

def choose_password():
    # setup email/password login
    print("""\nI need to create a login using an email/pass
    \nThis login will be used:
    1. By thermostat.py to access the pyrexia api
    2. To login using the pyrexia-android client""")
    email = input("\nChoose email address:")

    while True:
        password = input("\nChoose a password:")
        password2 = input("Re-enter password:")
        if password != password2:
           print("passwords do not match!")
        elif len(password) < 6:
           print("minimum password length is 6 chars")
        else:
           return email, password
        
print("pyrexia first time setup script\n\n")
result = choose_password()
email = result[0]
password = result[1]
response = rest.user_register(email, password)
print(response)
if not response.ok:
    print("ERROR: failed to register "+email+" with the server")
    if response.status_code == 403:
        print("Make sure a user has not already been registered")
    else:
        print("Make sure the pyrexia node server is up and running")

else:
    print("successfully registered user with pyrexia node api")

