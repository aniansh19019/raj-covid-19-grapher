from webapp import db
from webapp.models import Headers
import sys

def view_all():
	hs=Headers.query.all()
	for x in hs:
		print(x)

if __name__ == '__main__':
	view_all()