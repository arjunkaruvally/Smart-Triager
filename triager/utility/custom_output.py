from flask_socketio import emit
import gevent
import traceback

def cprint(self, val, signal="", mode=1, socketio=None, thread=False):
		if mode==1:
			print val
		elif mode==2:
			if thread:
				socketio.emit(signal, val, broadcast=True)
			else:
				emit(signal, val, broadcast=True)
			gevent.sleep(0)
			print signal," : ",val
		elif mode==3:
			if val['index']%val['step'] == 0 or val['index']==val['max']:
				if thread:
					socketio.emit(signal, val, broadcast=True)
				else:
					emit(signal, val, broadcast=True)
				gevent.sleep(0)
			# print signal," : ",val

class CustomOutput:
	def __init__(self, thread=False, socketio=None):
		self.thread=thread
		self.socketio=socketio


	def cprint(self, val, signal="", mode=1, show_error=False):
		if mode==1:
			print val
		elif mode==2:
			if self.thread:
				self.socketio.emit(signal, val, broadcast=True)
			else:
				try:
					emit(signal, val, broadcast=True)
				except Exception:
					print ''.join(traceback.format_exc())
			gevent.sleep(0)
			print signal," : ",val
		elif mode==3:
			if val['index']%val['step'] == 0 or val['index']==val['max']:
				if self.thread:
					self.socketio.emit(signal, val, broadcast=True)
				else:
					try:
						emit(signal, val, broadcast=True)
					except Exception:
						if show_error:
							print ''.join(traceback.format_exc())
				gevent.sleep(0)
			# print signal," : ",val