from time import sleep

class Timer:
	def __init__(self, time):
		self.time = time
		self.old_time = time

	def get_time(self):
		return self.time

	def start(self):
		if self.time < 0:
			print('Невреное значение!')
		else:
			time1 = self.time
			for i in range(self.time):
				sleep(1)
				time1 -= 1
			print('Время истекло!')
			self.time = time1

	def reset(self):
		self.time = self.old_time
