#upload modules
import sqlite3

#connecting
connect = sqlite3.connect('DataBase.db')
cursor = connect.cursor()

#create table
cursor.execute('''CREATE TABLE IF NOT EXISTS cars(
	id 	INTEGER PRIMARY KEY,
	brand TEXT,
	model TEXT,
	year INTEGER,
	description TEXT,
	status TEXT)''')

#functions

#create car
def create_car():
	#data request
	print('Введите марку машины:')
	brand = input('>>')
	print('Введите модель машины:')
	model = input('>>')
	print('Введите год производства машины:')
	year = int(input('>>'))
	print('Введите описание работ:')
	description = input('>>')
	print('Введите статус работы (1 - готово, 0 - не готово):')
	status = 'not ready' if input('>>') == '0' else 'ready'

	#write data to DB
	cursor.execute(f'''INSERT INTO cars(brand, model, year, description, status) VALUES('{brand}', '{model}', {year}, '{description}', '{status}')''')
	connect.commit()

#update car
def update_car():
	#id request
	print('Введите номер машины:')
	command1 = input('>>')

	#request change
	print('Введите то, что хотите изменить:')
	print('1: Марку машины')
	print('2: Модель машины')
	print('3: Год производства машины')
	print('4: Описание работ')
	print('5: Статус работы')
	command2 = input('>>')

	#number to text
	if command2 == '1':
		command2 = 'brand'
	elif command2 == '2':
		command2 = 'model'
	elif command2 == '3':
		command2 = 'year'
	elif command2 == '4':
		command2 = 'description'
	elif command2 == '5':
		command2 = 'status'
	else:
		print('Команда не найдена')

	#request data
	if command2 == 'status':
		print('Введите данные (0 - не готово, 1 - готово)')
	else:
		print('Введите данные:')
	command3 = input('>>')

	#update data to DB
	cursor.execute(f'''UPDATE cars SET {command2} = {command3} WHERE id = {command1}''')
	connect.commit()

def list_car(ready='not ready'):
	#select data from DB
	cursor.execute(f'''SELECT * FROM cars WHERE status = '{ready}' ''')
	data = cursor.fetchall()

	#print
	j = 0
	for i in data:
		print(f'Номер: {data[j][0]}')
		print(f'Марка: {data[j][1]}')
		print(f'Модель: {data[j][2]}')
		print(f'Год производства: {data[j][3]}')
		print(f'Описание работы: {data[j][4]}')
		j += 1
		print('')

#run
while True:
	print('Введите номер команды:')
	print('1: Добавить новый автомобиль на обслуживание')
	print('2: Обновить информацию об автомобиле')
	print('3: Просмотреть список авто на обслуживании')
	print('4: Просмотреть список обслуженых авто')
	print('5: Выйти')
	comand = input('>')
	if comand == '1':
		create_car()
	elif comand == '2':
		update_car()
	elif comand == '3':
		list_car(ready='not ready')
	elif comand == '4':
		list_car(ready='ready')
	elif comand == '5':
		connect.close()
		quit()
	else:
		print('Неверная команда!')