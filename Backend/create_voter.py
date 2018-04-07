import requests
# res = requests.post('http://0.0.0.0:8080/create/election', json={"electionName":"Sample Name 1", "description" : "Hello sample 1"
#                                                                  ,"startTime":"2038-01-19 03:14:07", "endTime":"2038-01-19 03:14:07", "hostId" :16103023}, headers={"authKey": "pdh"})
#
# print(res.json())

res = requests.post('http://0.0.0.0:8080/create/listvoters/49033', json=[

		{"voterId":16103023 },{"voterId": 16103026}

	],headers={"authKey": "pdh"})

print(res.json())
