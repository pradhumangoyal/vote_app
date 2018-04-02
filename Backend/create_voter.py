import requests
res = requests.post('http://0.0.0.0:8080/create/voter', json={"id":"3", "electionId" : "3"})

print(res.json())

