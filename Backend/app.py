import string
from flask import Flask, request, jsonify, send_from_directory, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import random	
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail,  Message
from email.message import EmailMessage
from mailjet_rest import Client
import os

api_key =  "08654429a1ccf308410d2f91df61713e"
api_secret = "6f82ebe2371ab441fbb694f8bca67708"
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

#mailjet.sender.create(data={'email': 'onlinepollingsys@gmail.com'})

# set the project root directory as the static folder, you can set others.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://onlinepolling:password@localhost/onlinepollingdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'onlinepollingsys@gmail.com'
# app.config['MAIL_PASSWORD'] = 'onlinepollingsystem'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['Debug'] = True

db = SQLAlchemy(app)

mail = Mail(app)
mail.init_app(app)

from models.model import pass_param

pass_param(db)

from models.voter import Voter
from models.electoralroll import ElectoralRoll
from models.candidate import Candidate
from models.elections import Elections
from models.vote import Vote

#********FUNCTIONS***********#
def gen_otp():
	return random.randint(999,9999)	

def gen_electionId():
	done = False

	while not done:
		electionId = random.getrandbits(16)
		alreadyId = db.session.query(Elections.electionId).filter_by(electionId=electionId).first()

		if alreadyId == None:
			break

	return electionId 

def check_valid_hostId(hostId):

	listId = db.session.query(ElectoralRoll.voterId)

	ids = []
	for row in listId:
		ids.append(row[0])

	print (ids)

	if hostId not in ids:
		return False
	return True

def send_email(electionId, voterId, otp):
    fromaddr = "onilnepollingsys@gmail.com"
    toaddrs = db.session.query(ElectoralRoll.email).filter_by(voterId = voterId).first()
    username = 'onlinepollingsys@gmail.com'
    password = "onlinepollingsystem"
    message = "OTP for election with id = " + str(electionId) +" is = " + str(otp)
    subject = 'Onlinepollingsystem : OTP'

    toaddrs = toaddrs[0]

    result = mailjet.contact.create(data={'email': toaddrs})

    email = {
    'Messages': [
	    {
			"From": {
				"Email": fromaddr,
				"Name": "Onlinepollingsystem"
			},
			"To": [
				{
					"Email": toaddrs,
					"Name": "OTP: "
				}
			],
			"Subject": subject,
			"TextPart": message,
			"HTMLPart": "OTP for election with id = " + str(electionId) +" is = " + str(otp)
		}
	]
}

    res = mailjet.send.create(email)
    
    print(res.json())

    # server = smtplib.SMTP_SSL('smtp.gmail.com',587)
    # server.login(username,password)
    # server.sendmail(
    # 	fromaddr,toaddrs,message
    # 	)
    # server.quit()
    # print('Sending mail')
    # msg = Message(subject, sender = fromaddr, recipients = [toaddrs])
    # msg.body = message
    # print('Progress started')
    # mail.send(msg)
    # msg = EmailMessage()
    # msg.set_content(message)
    # msg['Subject'] = subject
    # msg['From'] = fromaddr
    # msg['To'] = toaddrs
    # print('Generating SMTP')
    # s = smtplib.SMTP('smtp.gmail.com:587')
    # print('SMTP generated')
    # s.send_message(msg)
    # s.quit()


#*****************************************************#

@app.route('/')
def main_page():
	return render_template("/frontpage.html")
	
#*********************Voter Related API*****************************#

#Get all the voters from the electoral roll
@app.route('/voters', methods=['GET'])
def getVoters():


	# try:
	# 	if request.headers['authKey'] != "pdh":
	# 		return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	# except Exception as e:
	# 	return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	voters = ElectoralRoll.query.all()
	votersInfo = []

	if voters == None:
		votersInfo["ACK"] = "Failed"
		return jsonify(votersInfo)

	for voter in voters:
		voterInfo = {}
		voterInfo["ACK"] = "Success"
		voterInfo["voterId"] = voter.voterId
		voterInfo["name"] = voter.name
		voterInfo["branch"] = voter.branch
		voterInfo["year"] = voter.year
		voterInfo["email"] = voter.email
		voterInfo["contact"] = voter.contact

		votersInfo.append(voterInfo)

	return jsonify(votersInfo)

#Add A voter to electoral roll
@app.route('/create/voter', methods=['POST'])
def create_voter():
    
	# try:
	# 	if request.headers['authKey'] != "pdh":
	# 		return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	# except Exception as e:
	# 	return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	singleVoter = request.get_json()

	if singleVoter == None:
		return jsonify({'ACK': 'FAILED'})
	
	try:	
		voterId = singleVoter["voterId"]
		name = singleVoter["name"]
		branch = singleVoter["branch"]
		year = singleVoter["year"]
		email = singleVoter["email"]
		contact = singleVoter["contact"]
	except KeyError as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	electoralRoll = ElectoralRoll( voterId=voterId,
		name=name,
		branch=branch,
		year=year,
		email=email,
		contact=contact)

	curr_session = db.session
	success = False

	try:
		curr_session.add(electoralRoll)
		curr_session.commit()
		success = True
	except Exception as err:
		print(err)
		curr_session.roll_back()
		curr_session.flush()

	if success:
		return jsonify({'ACK': 'Success'})
	return jsonify({'ACK': 'FAILED'})

#**********Authenticate a Voter*******#

@app.route('/auth', methods=['GET','POST'])
def check_auth():
	if request.method == 'POST':
		otp = int(request.form["otp"].strip())
		electionId = int(request.form["electionId"].strip())
		voterId = int(request.form["voterId"].strip())

		result = db.session.query(Voter.otp).filter_by(electionId=electionId,voterId=voterId).first()

		result = result[0]

		print("result otp ==> " + str(result))

		if result != otp:
			return render_template("/frontpage.html")
		return render_template("/cast_vote.html", electionId=electionId,otp=otp,voterId=voterId)

	return render_template("/voter_login.html")

#***********Create a Elegible voter List and send Emails with otp for a particular electionId************#

@app.route('/create/listvoters/<electionId>', methods=['POST'])
def create_eligible_list(electionId):
	# try:
	# 	if request.headers['authKey'] != "pdh":
	# 		return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	# except Exception as e:
	# 	return jsonify({'ACK' : 'Not auth', 'Message' : 'Missing ' + e.args[0]})

	data = request.get_json()

	if data == None:
		return jsonify({'ACK': 'FAILED'})

	success = False
	curr_session = db.session

	sendList = []

	print("data == > CREATE LIST")
	print(data)

	try:
		for voter in data:
			listMember = {}
			print("voter data == > CREATE LIST")
			print(voter)
			print("voter print end")
			voterId = voter["voterId"]
			print("VoterId Recieved ==> " + str(voterId))	
			otp = gen_otp()

			electionId = int(electionId)
            
			voter = Voter(electionId = electionId, id = voterId, otp= otp)
			
			print("Printing == > ")
			print("==> making Object")

			listMember["voterId"] = voterId
			listMember["electionId"] = electionId
			listMember["otp"] = otp 

			curr_session.add(voter)

			print("==> Current session added")
			sendList.append(listMember)

	except Exception as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	try:
		curr_session.commit()
		success = True

		for eligibleVoter in sendList:
			send_email(voterId=eligibleVoter["voterId"], electionId=eligibleVoter["electionId"], otp=eligibleVoter["otp"])

	except Exception as err:
		print(err)
		curr_session.roll_back()
		curr_session.flush()

	if success:
		return jsonify({'ACK': 'Success'})
	return jsonify({'ACK': 'FAILED'})

#***********Create Elections************#
@app.route('/create/election', methods=['GET','POST'])
def create_election():

	if request.method == 'POST':
		try:
			electionName = request.form["electionName"].strip()
			description = request.form["description"].strip()
			startTime = request.form["startTime"].strip().replace('T', ' ')
			endTime = request.form["endTime"].strip().replace('T',' ')
			hostId = int(request.form["hostId"].strip())



			if not check_valid_hostId(hostId):
				raise KeyError('Invalid hostId')

		except KeyError as e:
			return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

		electionId = gen_electionId()
		print("electionId ==> " + str(electionId) + "hostId ==> " + str(hostId) )
		election = Elections(hostId =hostId,electionId = electionId, electionName=electionName,startTime=startTime,endTime=endTime,description=description)

		curr_session = db.session
		success = False

		try:
			curr_session.add(election)
			curr_session.commit()
			success = True
		except Exception as err:
			print(err)
			curr_session.roll_back()
			curr_session.flush()

		if success:
			return jsonify({'ACK': 'Success'})
		return jsonify({'ACK': 'FAILED'})

	return render_template("/host_election.html")

#********Cast vote and get results***********#
@app.route('/castvote', methods=['GET','POST'])
def cast_vote():

	if request.method == 'POST':

		curr_session = db.session
		success = False

		try:
			uId = int(request.form['uId'].strip())
			electionId = int(request.form['electionId'].strip())
			vote = Vote.query.filter_by(uId=uId,electionId=electionId)
			x = vote[0].count
			vote[0].count = x + 1
			result = db.engine.execute("delete from Voter where electionId="+str(electionId)+",name="+str(courseId))	
			curr_session.commit()
			success = True
		except Exception as err:
			print(err)

		if success:
			return jsonify({'ACK': 'Success'})
		return jsonify({'ACK': 'FAILED'})

#********Register as a candidate*******#
@app.route('/register/candidate',methods=['GET','POST'])
def reg_candidate():

	if request.method == 'POST':		
		try:
			voterId = int(request.form["voterId"].strip())
			electionId = int(request.form["electionId"].strip())
			name = request.form["name"].strip()
			manifesto = request.form["manifesto"].strip()
			if not check_valid_hostId(voterId):
				raise KeyError('Invalid hostId')

		except KeyError as e:
			return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

		candidate = Candidate(voterId=voterId,electionId=electionId,name=name,manifesto=manifesto)

		curr_session = db.session
		success = False

		try:
			curr_session.add(candidate)
			curr_session.commit()
			print(candidate)
			uId = candidate.uId
			print(uId)
			result = db.engine.execute("INSERT INTO Vote (uId,electionId,count) VALUES (" + str(uId) + "," + str(electionId) + ", 0)") 
			success = True
		except Exception as err:
			print(err)
			

		if success:
			return jsonify({'ACK': 'Success'})
		return jsonify({'ACK': 'FAILED'})

	return render_template("/candidate_reg.html")

#***********Get the results********#
@app.route('/getresults/', methods=['GET', 'POST'])
def fetch_results():

	# try:
	# 	if request.headers['authKey'] != "pdh":
	# 		return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	# except Exception as e:
	# 	return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	data = request.get_json()
	if data == None:
		return jsonify({'ACK': 'FAILED'})

	try:
		electionId = data["electionId"]
	except KeyError as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	
	try:
		results = db.engine.execute("SELECT * FROM Vote where electionId="+str(electionId)).fetchall()
		print("results == > " )
		print(results)
		ret = []

		for result in results:
			add = {}
			count = result.count
			uId = result.uId
			add["count"] = count
			add["uId"] = uId
			add["ACK"] = "Success"
			print("Reached Before query")
			candidate = db.engine.execute("SELECT * FROM Candidate where electionId="+str(electionId)).fetchone()
			print("Candidate == >")
			print(candidate)
			print("Reached After query")
			add["voterId"] = candidate[2]
			print("Reached Before query")
			add["manifesto"] = candidate[4]
			add["name"] = candidate[3]
			ret.append(add)
			print("Here")

		return jsonify(ret)
	except Exception as e:
		return jsonify({'ACK': 'FAILED'})

#**********Get list of elections***********#
@app.route('/list/elections', methods=['GET', 'POST'])
def get_listAll():
	# try:
	# 	if request.headers['authKey'] != "pdh":
	# 		return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	# except Exception as e:
	# 	return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	try:
		#lists = db.session.query(Elections).order_by(Elections.electionId)
		print("Reached here")
		lists = db.engine.execute("SELECT * FROM Elections order by electionId").fetchall()
		print("lists ==> ")
		print(lists)

		ret=[]
		for election in lists:
			print("Start")
			add = {}
			print("Election == >")
			print(election[0])
			add["electionId"] = election[0]
			add["name"] = election[2]
			add["ACK"] = "Success"
			print("here")
			ret.append(add)
			print("Done")
		print(ret)

		return jsonify(ret)
		print("Here")
	except Exception as e:
		return jsonify({'ACK': 'FAILED'})



if __name__ == '__main__':
	db.create_all()
	app.run(debug=False, host="172.31.74.11", port=8000, threaded=True)