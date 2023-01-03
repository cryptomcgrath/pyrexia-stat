#!/usr/bin/env python3
import rest

def choose_password():
    # setup email/password login
    print("""\nI need to create a login using an email/pass
    \nThis login will be used:
    1. By thermostat.py to access the pyrexia api
    2. Your login using the pyrexia-android client""")
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

def setup_user():
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
        return False

    else:
        print("successfully registered user with pyrexia node api")
        return True

def write_base_url(url):
    with open(".env", "w") as f:
        f.write("BASE_URL="+url)

def setup_url():
    while True:
        print("\n\n** pyrexia-stat first time setup **\n")
        print("NOTE: Before you continue, make sure the pyrexia-api-node server is running!")
        print("Enter the url for the pyrexia-api-node server")
        print("  In most cases use the default since both")
        print("  pyrexia-api-node and pyrexia-stat would run on the same host")
        url = input("(http://localhost:8000) ?: ")
        if url == "":
            url = "http://localhost:8000"
        response = rest.ping(url)
        if response.ok:
            write_base_url(url)
            print("SUCESS: pinged "+url+" ok!")
            return
        else:
            print(response)
            print("ERROR: unable to connect to "+url)

setup_url()
setup_user()

