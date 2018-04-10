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
		return 'Candidate: < ' + str(self.electionId) + ':' + str(self.uId) + ':' + str(self.voterId) + ':' + self.name + ':' + self.manifesto + '>'
		
	def __init__(self, electionId, voterId, name, manifesto):
		self.voterId = voterId
		self.name = name
		self.manifesto = manifesto
		self.electionId = electionId

	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}

	def get_uId(self):
		return self.uId

	def get_voterId(self):
		return self.voterId

	def get_name(self):
		return self.name

	def get_manifesto(self):
		return self.manifesto
		
