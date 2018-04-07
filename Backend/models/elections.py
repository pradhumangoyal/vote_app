from models.model import db

class Elections(db.Model):

	'''
		Contains Details of all elections
	'''

	__tablename__ = "Elections"

	electionId = db.Column( db.Integer, nullable=False, primary_key=True, autoincrement=True)
	electionName = db.Column (db.String(1000),nullable=False )
	description = db.Column (db.Text, nullable=True)
	startTime = db.Column (db.DateTime, nullable=False)
	endTime = db.Column (db.DateTime, nullable=False)
	hostId = db.Column ( db.Integer, nullable=False)

	def __repr__(self):
		return 'Electons: < ' + self.hostId + ':' + self.electionId + ':' + self.electionName + ':' + self.description + ':' + self.startTime + ':' + self.endTime + '>'
		
	def __init__(self, hostId, electionId, electionName, description, startTime, endTime):
		self.electionId = electionId
		self.electionName = electionName
		self.description = description
		self.startTime = startTime
		self.endTime = endTime
		self.hostId = hostId

	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}
		
