from models.model import db

class Voter(db.Model):

	'''
		Contains details of a voter
	'''

	__tablename__ = 'Voter'

	voterId = db.Column(db.Integer,db.ForeignKey('ElectoralRoll.voterId'), nullable=False, primary_key=True )
	electionId = db.Column(db.Integer,db.ForeignKey('Elections.electionId'), nullable=False)
	otp = db.Column(db.Integer, nullable=True)

	def __repr__(self):
		return 'Voter: < ' + self.voterId + ':' + self.electionId + ':' + self.otp + '>'

	def __init__(self, id, electionId,otp):
		self.voterId = id
		self.electionId = electionId
		self.otp = otp


	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}
		
