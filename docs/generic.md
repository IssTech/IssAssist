# Generic Information
Doesn't matter what plugin you are using this is the main steps to create any information and connect that with your device or user.

We are using Django Rest Framework Simple JWT Token base. You can [read more here](https://github.com/jazzband/djangorestframework-simplejwt)

### Overview - New Device
For a new Device you need to do following steps.
* Create a User
* Obtain a Token and a Refresh Token.
* Refresh your token
* Register your Device

### Overview - Existing Device
For a existing device you can then refresh your token with following steps.
* Refresh your Token

## Create a User Account (POST)
To register your device you need to register a user account that will generate a token for future use and assign the data to your specific device.
You need to include following information in your registration.
- Username
- Password
- Owners Email Address. (Not recommended to use fake email, but for test is that ok)

End-Point: `/api/auth/registration/`

### cURL
curl --location --request POST '<issAssist URL>' \
--header 'Content-Type: application/json' \
--form 'username="<device>"' \
--form 'password1="<Password>"' \
--form 'password2="<Password>"' \
--form 'email="<hostname.owners.email@company.com>"'

### Python
import requests
import json

url = "<issAssist URL>"

payload={'username': '<Device Name>',
'password1': '<Password>',
'password2': '<Password>',
'email': '<hostname.owners.email@company.com>'}

headers = {'Content-Type': 'application/json'}

response = requests.request("POST", url, headers=headers, json=payload)
print(response.text)

## Obtain token (POST)
You will get a first token pair that you can reuse for future Token Refresh.
To get your token you need to fill out your Username and Password.

End-Point: `/api/auth/token/`

### cURL
curl --location --request POST '<issAssist URL>' \
--header 'content-type: application/json' \
--form 'username="<device>"' \
--form 'password="<Password>"'

### Python
import requests
import json

url = "<issAssist URL>"

payload={'username': '<device name>', 'password': '<Password>'}

headers = {'content-type': 'application/json'}
response = requests.request("POST", url, headers=headers, json=payload)
print(response.text)

#### Expected output
You should get status code `201` and get a token to use direct and a refresh token that you need to store to be able to refresh your token.

## Refresh Token (POST)
After 60 min of inactivation you need to refresh your token, and when you obtain your first token you did also get a refresh token.
Use that to refresh for a new token.

End-Point: `/api/auth/token/refresh/`

### cURL
curl --location --request POST '<issAssist URL>' \
--header 'content-type: application/json' \
--form 'refresh="<Refresh Token>"'

### Python
import requests
import json

url = "<issAssist URL>"

payload={'refresh': '<refresh token>'}

headers = {'content-type': 'application/json'}

response = requests.request("POST", url, headers=headers, json=payload)
print(response.text)

#### Expected output
You should get status code `201` for a successfully refresh, and a new token that is valid for 60 min.

## Verify Token (POST)
You can verify your token and see if it valid by sending your latest token.

End-Point: `/api/auth/token/verify/`

### cURL
curl --location --request POST '<issAssist URL>' \
--header 'content-type: application/json' \
--form 'token="<Token>"'

### Python
import requests
import json

url = "<issAssist URL>"

payload={'token': <Token>'}
headers = {'content-type': 'application/json'}

response = requests.request("POST", url, headers=headers, json=payload)
print(response.text)

#### Expected output
You should get status code `200` with a empty string.

## Register your Device (POST)
To register your device for IssAssist

End-Point: `/api/v1/core/`

### cURL
curl --location --request POST '<issAssist URL>' \
--header 'content-type: application/json' \
--header 'Authorization: Bearer <Token>' \
--form 'hostname="<Hostname>"' \
--form 'fqdn="<Full Qualify Domain Name>"' \
--form 'ipv4_address="<IP Address>"'

### Python
import requests
import json

url = "<issAssist URL>"

headers = {
  'content-type': 'application/json',
  'Authorization': 'Bearer <Token>'}

payload={
  'hostname': '<Device Name>',
  'fqdn': '<Full Qualify Domain Name>',
  'ipv4_address': '<IP Address>'}

response = requests.request("POST", url, headers=headers, json=payload)
print(response.text)

#### Expected output
You should get status code `201` with a empty string.

## Get Device Information (GET)

End-Point: `/api/v1/core/`

### cURL
curl --location --request GET '<issAssist URL>' \
--header 'content-type: application/json' \
--header 'Authorization: Bearer <Token>' \

### Python
import requests
import json

headers = {
  'content-type': 'application/json',
  'Authorization': 'Bearer <Token>'}

payload = {}

response = requests.request("GET", url, headers=headers, json=payload)
print(response.text)

#### Expected output
You should get status code `200` for successful request, but you should also get the information about your register device.
