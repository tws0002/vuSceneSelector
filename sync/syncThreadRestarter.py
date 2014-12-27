"""
Calls syncThrad as SubThread,
and Restarts him whenever nessesarry
"""




import os
import time
import syncThread
import threading

class SubThread(threading.Thread):
	'''SubThread to run the syncThread'''
	def __init__(self):
		super(SubThread, self).__init__()
		self.running = True

	def run(self):
		while self.running:
			syncThread.watch()
			time.sleep(0.1)


if __name__ == '__main__':
	fileName = syncThread.__file__
	startTime = None
	thread = None

	while True:
		lastModify = os.path.getmtime(fileName)

		if startTime != lastModify:
			print "Restart all the Things!!!"

			if thread:
				thread.running = False

			reload(syncThread)
			thread = SubThread()
			thread.start()
			startTime = lastModify
		else:
			time.sleep(0.1)

	#thread = SubThread()
	#thread.start()