import string
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json




# set the project root directory as the static folder, you can set others.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://onlinepolling:password@localhost/onlinepollingdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models.model import pass_param

pass_param(db)

from models.voter import Voter
from models.electoralroll import ElectoralRoll
from models.candidate import Candidate
from models.elections import Elections
from models.vote import Vote



@app.route('/')
def show_all():
	example = {}
	example["OnlinePolling"] = "Welcome To Online Polling Database"

	return jsonify(example)

#*********************Voter Related API*****************************#

#Get all the voters from the electoral roll
@app.route('/voters', methods=['GET'])
def getVoters():

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

@app.route('/auth/<int: otp>', methods=['POST'])
def check_auth():
	


if __name__ == '__main__':
	db.create_all()
	app.run(debug=False, host="172.31.71.98", port=8080, threaded=True)

