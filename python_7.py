import sqlite3

connect = sqlite3.connect('DataBase.db')
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Books(
	id INTEGER PRIMARY KEY,
	title TEXT,
	author TEXT,
	year INTEGER)''')

#1
class Book:
	def __init__(self, title, author, year):
		self.title = title
		self.author = author
		self.year = year
	def display_info(self):
		print(f'Книга: {title}')
		print(f'Автор: {author}')
		print(f'Год: {year}')

#2
class Book:
	def info_book(self):
		cursor.execute('''SELECT * FROM Books''')
		info = cursor.fetchall()
		for i in info:
			print(f'Номер: {i[0]}')
			print(f'Книга: {i[1]}')
			print(f'Автор: {i[2]}')
			print(f'Год: {i[2]}')
			print('')
	def create_book(self):
		print('Введите название книги:')
		command1 = input('>>')
		print('Введите автора книги:')
		command2 = input('>>')
		print('Введите год издания:')
		command3 = int(input('>>'))
		cursor.execute(f'''INSERT INTO Books(title, author, year) VALUES('{command1}', '{command2}', {command3}) ''')
		connect.commit()
	def update_book(self):
		print('Введите номер того, чего хотите поменять:')
		print('1: Название книги')
		print('2: Автора книги')
		print('3: Год изданния книги')
		command1 = input('>>')
		print('Введите данные:')
		command2 = input('>>')
		print('Введите номер книги')
		command3 = int(input('>>'))
		if command1 == '1':
			cursor.execute(f'''UPDATE Books SET title = '{command2}' WHERE id = {command3}''')
		elif command1 == '2':
			cursor.execute(f'''UPDATE Books SET author = '{command2}' WHERE id = {command3}''')
		elif command1 == '3':
			cursor.execute(f'''UPDATE Books SET year = {command2} WHERE id = {command3}''')
		else:
			print('Неверная команда!')
		connect.commit()
	def delete_book(self):
		print('Введите номер книги')
		command1 = int(input('>>'))
		cursor.execute(f'''DELETE FROM Books WHERE id = {command1}''')
	def main(self):
		while True:
			print('Введите номер команды:')
			print('1: Посмотреть информацию о книгах')
			print('2: Создать книгу')
			print('3: Обновить информацию о книге')
			print('4: Удалить книгу')
			print('5: Выход')
			command = input('>')
			if command == '1':
				self.info_book()
			elif command == '2':
				self.create_book()
			elif command == '3':
				self.update_book()
			elif command == '4':
				self.delete_book()
			elif command == '5':
				connect.close()
				break
			else:
				print('Неверная команда!')
# book = Book()
# book.main()