import requests

# Login to get the token
login_url = "http://127.0.0.1:5002/login"
login_data = {"username": "admin", "password": "password"}
response = requests.post(login_url, json=login_data)

if response.status_code == 200:
    token = response.json().get("access_token")
    print("Token:", token)

    # Use the token to access the protected endpoint
    protected_url = "http://127.0.0.1:5002/protected"
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = requests.get(protected_url, headers=headers)

    print("Protected Response:", protected_response.json())
else:
    print("Login failed:", response.json())
