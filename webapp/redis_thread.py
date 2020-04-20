from threading import Thread
from webapp import app, redis_obj

def incr_async_var(app,var):
	with app.app_context():
		try:
			redis_obj.incr(var)
		except:
			print("Counter redis server unreachable!")

def set_async_var(app,var,val):
	with app.app_context():
		try:
			redis_obj.set(var,val)
		except:
			print("Counter redis server unreachable!")





def incr_var(var):
	if redis_obj:
		Thread(target=incr_async_var, args=(app, var)).start()



def set_var(var,val):
	if redis_obj:
		Thread(target=set_async_var, args=(app, var, val)).start()
	
def get_var(var):
	if redis_obj:
		return redis_obj.get(var)
	else:
		return "'Unreachable'"