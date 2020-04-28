from webapp import db
from datetime import datetime

class Headers(db.Model):
	ip = db.Column(db.String(16), primary_key=False)
	country = db.Column(db.String(16), index=True)
	user_agent = db.Column(db.String(128), index=True)
	timestamp = db.Column(db.DateTime, index=True, primary_key=True, default=datetime.utcnow)

	def __repr__(self):
		return '<IP: {}>'.format(self.ip)   