import time
import threading
class Timer(threading.Thread):
	def __init__(self, action, time=1):
		self.count = 0
 		self.runTime = time
		self.action = action
		self.__stop = False
 		threading.Thread.__init__(self)
	def run(self):
 		if not self.__stop:
			time.sleep(self.runTime)
			self.count += 1
 			self.action(self.count)
			self.run()
		else:
			exit()
	def timer_start(self):
		if self.__stop:
			self.__stop = False
			self.run()
	def timer_stop(self):
		self.__stop = True
	def started(self):
		return not self.__stop


def __MyFunc(count):
	print "timer thread, count - %d" % count


if __name__ == '__main__':
	t = Timer(action=__MyFunc, time=1)
	t.start()
	t.timer_start()
	print 'main thread'
	print 'main thread'
	print 'main thread'
	time.sleep(5)
	print 'main thread - sleep 5'
	t.timer_stop()
	del t
	time.sleep(6)
	print 'main thread - sleep 6'
	t = Timer(action=__MyFunc, time=2)
	t.start()
	t.timer_start()
	print 'second timer start'
        time.sleep(8)
	print 'second timer stop'
	t.timer_stop()	
	
