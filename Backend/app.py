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



@app.route('/')
def show_all():
	example = {}
	example["Hello"] = "hello"

	return jsonify(example)

@app.route('/voters', methods=['GET'])
def getVoters():

	voters = Voter.query.all()
	votersInfo = []

	if voters == None:
		votersInfo["ACK"] = "Failed"
		return jsonify(votersInfo)

	for voter in voters:
		voterInfo = {}
		voterInfo["ACK"] = "Success"
		voterInfo["voterId"] = voter.voterId
		voterInfo["electionId"] = voter.electionId

		votersInfo.append(voterInfo)

	return jsonify(votersInfo)


@app.route('/create/voter', methods=['POST'])
def create_voter():
	data = request.get_json()
	print("request: ")
	print(request)
	try:
		print("Reached")
		voterId = data['id']
		eId = data['electionId']

		voter = Voter(voterId, eId)
		db.session.add(voter)
		db.session.commit()

		return jsonify({'ACK': 'SUCCESS'})
	except:
		return jsonify({'ACK': 'FAILED'})


if __name__ == '__main__':
	db.create_all()
	app.run(debug=False, host="0.0.0.0", port=8080, threaded=True)

