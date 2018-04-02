from models.model import db

class ElectoralRoll(db.Model):

	'''
		Contains Master Details
	'''

	__tablename__ = 'ElectoralRoll'

	voterId = db.Column(db.Integer, nullable=False, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	branch = db.Column(db.String(100), nullable=False)
	year = db.Column(db.Integer, nullable=False)
	email = db.Column(db.String(256), nullable=False, unique=True)
	contact = db.Column(db.String(10), nullable=False, unique=True)


	def __repr__(self):
		return 'ElectoralRoll: < ' + self.voterId + ':' + self.name + ':' + self.branch + ':' + self.year + ':' + self.email + ':' + self.contact + '>'
		
	def __init__(self, voterId, name, branch, year, email, contact):
		self.voterId = voterId
		self.name = name
		self.branch = branch
		self.year = year
		self.email = email
		self.contact = contact

	def as_dict(self):
		return { c.name : getattr(self, c.name) for c in self.__tablename__.columns}
		
