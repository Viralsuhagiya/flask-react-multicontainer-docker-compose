from flask import Flask, redirect, request
import requests

app = Flask(__name__)
access_token = ''

@app.route("/")
def index():
    print()
    return redirect("/auth")

@app.route("/auth")
def auth():
    # LinkedIn authentication parameters
    client_id = "77bt7nz3gqy28r"
    redirect_uri = "https://e5e7-2409-40c1-1035-7f10-cce5-507f-7872-f1bc.ngrok-free.app/callback"
    scope = "r_liteprofile"  # Requesting basic profile permissions

    # Redirect the user to the LinkedIn authorization URL
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    client_id = "77bt7nz3gqy28r"
    client_secret = "woPt4tsjsLC9dQt5"
    redirect_uri = "https://e5e7-2409-40c1-1035-7f10-cce5-507f-7872-f1bc.ngrok-free.app/callback"

    # Retrieve the authorization code from the request
    auth_code = request.args.get("code")

    # Exchange the authorization code for an access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_params = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }
    response = requests.post(token_url, data=token_params)

    # Process the access token response
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        print('>>>>>>access_token',access_token)
        # Store the access_token securely for future API calls
        return redirect("/leads")
    else:
        return "Access token retrieval failed."

@app.route("/leads")
def leads():
    print('>>>>>access_token here in leads',access_token)
    # LinkedIn API endpoint to retrieve leads
    leads_url = "https://api.linkedin.com/v2/leads"

    # Retrieve leads using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    response = requests.get(leads_url, headers=headers)

    # Process the leads response
    if response.status_code == 200:
        leads_data = response.json()
        # Process and display the leads data as required
        return "Leads retrieved successfully."
    else:
        return "Leads retrieval failed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)