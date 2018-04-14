import requests
# res = requests.post('http://0.0.0.0:8080/create/election', json={"electionName":"Sample Name 1", "description" : "Hello sample 1"
#                                                                  ,"startTime":"2038-01-19 03:14:07", "endTime":"2038-01-19 03:14:07", "hostId" :16103039}, headers={"authKey": "pdh"})

# print(res.json())

#Create list of voters

# res = requests.post('http://0.0.0.0:8080/create/listvoters/27049', json=[

# 		{"voterId":16103022 },{"voterId": 16103039}

# 	],headers={"authKey": "pdh"})

# print(res.json())
# # 
# res = requests.post('http://0.0.0.0:8080/auth', json={"otp":1271 , "electionId" : 27049, "voterId" :16103022 }, headers={"authKey": "pdh"} )
# print(res.json())

#Candidate register
# res = requests.post('http://0.0.0.0:8080/register/candidate', json={"name":"Ritesh" ,"manifesto":"Hello I am gay", "electionId" : 27049, "voterId" :16103039 }, headers={"authKey": "pdh"} )
# print(res.json())

#Cast Vote
# res = requests.post('http://0.0.0.0:8080/castvote', json={"uId":2 , "electionId" : 27049 }, headers={"authKey": "pdh"} )
# print(res.json())

#Get Results
# res = requests.post('http://0.0.0.0:8080/getresults/', json={"electionId" : 27049 }, headers={"authKey": "pdh"} )
# print(res.json())

#GET List elections
# res = requests.post('http://0.0.0.0:8080/list/elections', headers={"authKey": "pdh"} )
# print(res.json())

res = requests.post('http://172.31.74.11:8000/voters')

print(res.json())

for singleRes in res.json():
	print("<tr>"+'\n'+"<td><input type="+'"'+"checkbox"+'"'+ " name=" +'"' + "voter[]" + '"' +" value=" + '"' + "voter" +'"' +"></td>")
	print("<td>" +singleRes["name"]+"</td>")
	print("<td>" +str(singleRes["voterId"])+"</td>")
	print("<td>" +singleRes["email"]+"</td>")
	print("<td>" +str(singleRes["contact"])+"</td>")
	print("</tr><br>")





