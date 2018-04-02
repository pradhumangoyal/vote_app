from models.model import db

class Candidate(db.Model):

	'''
		Info about candidates
	'''
	__tablename__ = "Candidate"

	voterId = db.Column(db.Integer, db.ForeignKey('ElectoralRoll.voterId'),nullable=False)
	electionId = db.Column(db.Integer,db.ForeignKey('Elections.electionId'), nullable=False)
	name = db.Column (db.String(100), nullable=False)
	manifesto = db.Column (db.Text, nullable=True)
	uId = db.Column(db.Integer,primary_key=True, autoincrement=True )



	def __repr__(self):
		return 'Candidate: < ' + self.electionId + ':' + self.uId + ':' + self.voterId + ':' + self.name + ':' + self.manifesto + '>'
		
	def __init__(self,uId, electionId, voterId, name, manifesto):
		self.uId = uId
		self.voterId = voterId
		self.name = name
		self.manifesto = manifesto
		self.electionId = electionId

	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}
		
