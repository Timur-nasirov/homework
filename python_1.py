class Calculator:
	def __init__(self):
		self.num1 = int(input('Введите 1 число: '))
		self.num2 = int(input('Введите 2 число: '))
	def add(self):
		print(f'Ответ при сложении: {self.num1 + self.num2}')
	def subtract(self):
		print(f'Ответ при выитании: {self.num1 - self.num2}')
	def multiply(self):
		print(f'Ответ при умножении: {self.num1 * self.num2}')
	def divide(self):
		print(f'Ответ при делении: {self.num1 / self.num2}')

def main():
	operation = input('Введите операцию (add/subtract/multiply/divide): ')
	calc = Calculator()
	exec(f'calc.{operation}()')

main()