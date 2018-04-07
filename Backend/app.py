import string
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import random	
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail,  Message



# set the project root directory as the static folder, you can set others.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://onlinepolling:password@localhost/onlinepollingdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'onlinepollingsys@gmail.com'
app.config['MAIL_PASSWORD'] = 'onlinepollingsystem'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

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
    fromaddr = 'onlinepollingsys@gmail.com'
    toaddrs = db.session.query(ElectoralRoll.email).filter_by(voterId = voterId).first()
    username = 'onlinepollingsys@gmail.com'
    password = 'onlinepollingsystem'
    message = "OTP for election with id = " + str(electionId) +" is = " + str(otp)
    subject = 'Onlinepollingsystem : OTP'

    # server = smtplib.SMTP_SSL('smtp.gmail.com',587)
    # server.login(username,password)
    # server.sendmail(
    # 	fromaddr,toaddrs,message
    # 	)
    # server.quit()
    print('Sending mail')
    msg = Message(subject, sender = fromaddr, recipients = [toaddrs])
    msg.body = message
    print('Progress started')
    mail.send(msg)

#*****************************************************#

@app.route('/')
def show_all():
	example = {}
	example["OnlinePolling"] = "Welcome To Online Polling Database"

	return jsonify(example)

#*********************Voter Related API*****************************#

#Get all the voters from the electoral roll
@app.route('/voters', methods=['GET'])
def getVoters():


	try:
		if request.headers['authKey'] != "pdh":
			return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	except Exception as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

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
    
	try:
		if request.headers['authKey'] != "pdh":
			return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	except Exception as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

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

@app.route('/auth', methods=['POST'])
def check_auth(otp):
	try:
		if request.headers['authKey'] != "pdh":
			return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	except Exception as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	data = request.get_json()

	if data == None:
		return jsonify({'ACK': 'FAILED'})

	otp = data["otp"]
	electionId = data["electionid"]
	voterId = data["voterId"]

	sql = text('select otp from Voter where electionId = :electionId AND voterId = :voterId', {'electionId': electionId, 'voterId': voterId})
	result = db.engine.execute(sql)

	print("result otp ==> " + str(result))

	if result is not otp:
		return jsonify({ 'Authenticate' : 'Failed'})
	return jsonify({'Authenticate' : 'Pass'})

#***********Create a Elegible voter List and send Emails with otp for a particular electionId************#

@app.route('/create/listvoters/<electionId>', methods=['POST'])
def create_eligible_list(electionId):
	try:
		if request.headers['authKey'] != "pdh":
			return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	except Exception as e:
		return jsonify({'ACK' : 'Not auth', 'Message' : 'Missing ' + e.args[0]})

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
	try:
		if request.headers['authKey'] != "pdh":
			return jsonify({"ACK" : "AUTH NOT FOUND", "requestHeader": request.headers['authKey']})
	except Exception as e:
		return jsonify({'ACK' : 'FAILED', 'Message' : 'Missing ' + e.args[0]})

	data = request.get_json()

	if data == None:
		return jsonify({'ACK': 'FAILED'})


	try:
		electionName = data["electionName"]
		description = data["description"]
		startTime = data["startTime"]
		endTime = data["endTime"]
		hostId = data["hostId"]



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




if __name__ == '__main__':
	db.create_all()
	app.run(debug=True, host="0.0.0.0", port=8080, threaded=True)

