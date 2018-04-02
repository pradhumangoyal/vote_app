from models.model import db

class Vote(db.Model):

	'''
		Contains info about the Vote count 
	'''

	__tablename__ = "Vote"

	electionId = db.Column ( db.Integer, db.ForeignKey('Elections.electionId'),nullable=False, primary_key=True)
	uId = db.Column ( db.Integer,db.ForeignKey('Candidate.uId'), nullable=False , primary_key=True)
	count = db.Column (db.Integer, nullable=False)


	def __repr__(self):
		return 'Vote: < ' + self.electionId + ':' + self.uId + ':' + self.count + '>'
		
	def __init__(self, uId, electionId, count):
		self.uId = uId
		self.electionId = electionId
		self.count = 0

	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}
