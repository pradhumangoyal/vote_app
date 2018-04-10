import xlrd
import requests
import time

name = 'response.xlsx'
wb = xlrd.open_workbook(name)

sheet = wb.sheet_by_index(0)

# cse = ["cse", "CSE", "Cse", "Computer Science", "Computer Science and Engineering", "Computer science and engineering", "C.S.E.","C.s.e","Computer science","Computer science engineering","Computer science and engineering"]
# ece = ["ece", "ECE", "Electrical", "electrical", "Ece", "Electrical Engineering", "Electrical Engg.", "Electrical engineering", "Electronics and communication","ELECTRICAL ENGINEERING","ELECTRICAL"]
# mechanical = ["Mechanical", "mechanical", "MECHANICAL", "Mechanical Engineering", "Mechanchical", "Mech.","Mechancical", "MECHANICAL". ]
# metta = ["Materials and metallurgy","Material science and metallurgy","Materials & Metallurgy","Materials and Metallurgy","Metallurgy","Materials and metallurgical engineering","Materials & Metallurgical Engineering " , "Materials and Metallurgical Engg"]
# civil = ["Civil","CIVIL", "civil", "Civil Engineering","Civil engineering","CIVIL ENGG","Civil Engineering","Mechanical engineering"]
# ee = ["EE", "ELECTRICAL"]
# aero =["Aerospace","Aero"]
# production = ["Production and Industrial Engineering","production and industrial engg","Production","PRODUCTION AND INDUSTRIAL ENGG.","Production","Production and industrial engineering","Production and industrial engineering", "Materials and Metallurgical Engg", "Production and Industrial"]

  
for rownumber in range(1, sheet.nrows):
  print(rownumber)
  row = sheet.row(rownumber)
  email = row[1].value
  name = row[2].value
  voterid = int(row[3].value)
  temp_branch = (row[4].value)
  contact = int ((int(row[5].value)) % 1e10 )
  temp_year = row[6].value
  year = -1

  if temp_year == "Second Year":
  	year = 2
  elif temp_year == "First Year":
  	year = 1
  elif temp_year == "Fourth Year":
  	year = 4
  else:
  	year = 3

  branchno = str(voterid)
  branch=""
  x = int(branchno[4:5])
  if branchno[2:3] is "1":

    if x is 1:
    	branch = "Aerospace Engineering"
    elif x is 2:
    	branch = "Civil Engineering"
    elif x is 3:
    	branch = "Computer Science and Engineering"
    elif x is 4:
    	branch = "Electrical Engineering"
    elif x is 5:
    	branch = "Electronics and Communication Engineering"
    elif x is 7:
    	branch = "Mechanical Engineering"
    elif x is 8:
    	branch = "Material Science and Metallurgy Engineering"
    elif x is 9:
    	branch = "Production and Industrial Engineering"
  else:
    	branch = temp_branch

  r = requests.post('http://0.0.0.0:8080/create/voter', json={
  		"voterId": voterid,
  		"email": email,
  		"contact": str(contact),
  		"branch": branch,
  		"year": year,
  		"name": name}, headers={"authKey": "pdh"})
  
  print(r)

  time.sleep(0.03)







  