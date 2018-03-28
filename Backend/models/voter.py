from models.model import db

class Voter(db.Model):

	'''
		Contains details of a voter
	'''

	__tablename__ = 'Voter'

	voterId = db.Column(db.Integer, nullable=False, primary_key=True)
	electionId = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return 'Voter: < ' + self.voterId + ':' + self.electionId + '>'

	def __init__(self, id, electionId):
		self.voterId = id
		self.electionId = electionId


	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}
		
