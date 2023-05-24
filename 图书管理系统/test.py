import requests


resp = requests.get('http://localhost:5000/activities')
print(resp.status_code)
print(resp.json())