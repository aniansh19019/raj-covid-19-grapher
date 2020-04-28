from webapp import db
from datetime import datetime

class Headers(db.Model):
	ip = db.Column(db.String(64), primary_key=False)
	country = db.Column(db.String(16), index=True)
	user_agent = db.Column(db.String(256), index=True)
	fancy_user_agent=db.Column(db.String(128), index=True)
	timestamp = db.Column(db.DateTime, index=True, primary_key=True, default=datetime.utcnow)

	def __repr__(self):
		return self.timestamp.strftime("%m/%d/%Y ; %H:%M:%S")+" || IP: "+self.ip+" | Country: "+self.country+" | User Agent: "+self.fancy_user_agent 