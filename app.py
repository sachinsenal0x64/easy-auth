from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import os
import requests


app = Flask(__name__)

load_dotenv(find_dotenv())

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
redirect_uri = os.getenv("REDIRECT_URI")
scope = ["User.Read", "Files.ReadWrite","offline_access"]


@app.route('/')
def home():
    # Construct the authorization URL
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scope)
    }
    auth_url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

    # Redirect the user to the authorization URL
    return f"<h2>🧲 Please go to this URL and Authenticate :</h2> \n <h4> <a href='{auth_url}'>{auth_url}</a> </h4>"




@app.route('/app')
def apps():
    auth_code = request.args.get('code')
    if auth_code:
        # Exchange the authorization code for an access token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": auth_code,
            "grant_type": "authorization_code",
            "scope": " ".join(scope)
        }
        response = requests.post(token_url, data=payload)
        print(response.json())
        if response.ok:
            access_token = response.json()['access_token']
            refresh_token = response.json()['refresh_token']
            
            

            # Do something with the access token
            return f" <h2> ✔ Auth Successfully Completed </h2> <br>  <h3> 🎫 Refresh token: <br></br>  {refresh_token} <br></br>  🔑 Access token: <br></br> {access_token} </h3>"
        
        else:
            return f"Error getting Refresh token: {response.text}"
    else:
        return "Authorization code missing. Please try again."



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(80),debug=True)
