# IssSys Framework
IssSys is just a project name and there is a open-source plugin called IssSys that can do small generic upgrades.
There is other tools that are much smarter and more cleaver then IssSys, but if you want to use open source and freeware, please feel free to use it.

## Idea behind IssSys
Main idea behind IssSys is to help and guide you to make the right decision and follow your internal process whatever situation. Make sure you never forget or taking the wrong decision.

## With other tools
You can use IssSys framework to get IssAssist to work together with your preference of of tools.
By writing a small connector between your tool and IssSys Framework you can push in the necessary data and also the other way around you can execute automated upgrades of your system when all criteria has been fulfilled.

## Using IssSys
IssSys is a small open source software that use the native package tools like `YUM`, `DNF`, `APT` or `Windows Update Manager`. Collect all static and send that to IssAssist and make sure IssAssist can guide you when a upgrade is needed or not.

### Download IssSys
If you want to use or test IssSys, you can find it here [IssSys Link](https://github.com/IssTech/IssSys).

## Develop your own connector
To be able to create your own connector this is the steps you need to follow.

#### First time Registration
* Create a User
* Obtain a Token and a Refresh Token.
* Refresh your token
* Register your Device

#### Before you Send Information
Before you send information to IssSys Framework you need to refresh your token.
* Refresh your Token

## Send Update Information
To be able to send data to IssSys Framework in IssAssist you need to get hold of following information.
- Token
- Total Number of available system updates
- How many are Security System Updates
- How many of the updates are priority 1
- How many of the updates are priority 2
- How many of the updates are priority 3
- How many of the updates are priority 4
- How many of the updates are priority 5
- Assign the updates to your Host ID that you get from End-Point `/api/v1/core/`

End-Point: `/api/v1/isssys/`

### cURL
curl --location --request POST '<issAssist URL>' \
--header 'Authorization: Bearer <Token>' \
--form 'isssys_version="<Version>"' \
--form 'total_updates="<Total Number of Updates>"' \
--form 'security_updates="<Total Number of Security Updates>"' \
--form 'priority1_updates="<Total priority 1 Updates>"' \
--form 'priority2_updates="<Total priority 2 Updates>"' \
--form 'priority3_updates="<Total priority 3 Updates>"' \
--form 'priority4_updates="<Total priority 4 Updates>"' \
--form 'priority5_updates="<Total priority 5 Updates>"' \
--form 'hostname="<Hostname ID>"'

### Python
import requests
import json

url = "<issAssist URL>"

payload={'isssys_version': '<version>',
'total_updates': '<Total Number of Updates>',
'security_updates': '<Total Number of Security Updates>',
'priority1_updates': '<Total priority 1 Updates>',
'priority2_updates': '<Total priority 2 Updates>',
'priority3_updates': '<Total priority 3 Updates>',
'priority4_updates': '<Total priority 4 Updates>',
'priority5_updates': '<Total priority 5 Updates>',
'hostname': '<Hostname ID>'}

headers = {'Authorization': 'Bearer <token>'}

response = requests.request("POST", url, headers=headers, json=payload)
print(response.text)

#### Expected output
You should get status code `201` with a empty string.

## Get Device Information (GET)

End-Point: `/api/v1/isssys/`

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
You should get status code `200` for successful request, but you should also get the information how the status was last time you send a POST Request.
