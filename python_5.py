class Animal:
	def __init__(self, name, age):
		self.name = name
		self.age = age

class Dog(Animal):
	def __init__(self, name, age, breed):
		super().__init__(name, age)
		self.breed = breed
	def bark(self):
		print('Гав-гав!')

class Cat(Animal):
	def __init__(self, name, age, color):
		super().__init__(name, age)
		self.color = color
	def meow(self):
		print('Мяу!')
