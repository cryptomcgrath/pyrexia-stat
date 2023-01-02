#!/usr/bin/env python3
import secrets

def generate_token():
    # generate token_key for jwt
    print("generating TOKEN_KEY...")
    key = secrets.token_urlsafe(64)
    print("TOKEN_KEY="+key)
    return key 

key = generate_token()

# write the key to .env file
with open(".env", "w") as f:
    f.write("TOKEN_KEY="+key)

print("The TOKEY_KEY has been written to the .env file")
print("You should restart the pyrexia node server in order to use the new TOKEN_KEY")


