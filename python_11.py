#импорт модулей
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
from logging import basicConfig, INFO
import sqlite3

try:
	#базовые переменные
	bot = Bot(token=TOKEN)
	storage = MemoryStorage()
	dp = Dispatcher(bot, storage=storage)
	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()

	#создание таблицы
	cursor.execute('''CREATE TABLE IF NOT EXISTS users(
		id INTEGER PRIMARY KEY,
		first_name TEXT VARCHAR(255),
		last_name TEXT VARCHAR(255),
		login TEXT VARCHAR(255),
		password TEXT,
		age INTEGER,
		balance INTEGER,
		telegram_id TEXT
		)''')
	#лог
	basicConfig(level=INFO)

	#классы ФСМ
	class SignState(StatesGroup): #вход
		login = State()
		password = State()

	class RegState(StatesGroup): #регистарция
		login = State()
		password = State()
		age = State()

	class TransState(StatesGroup): #перевод
		user_id = State()
		summ = State()
		password = State()



	@dp.message_handler(commands="start")
	async def start(message:types.Message):
		await message.answer('Добро пожаловать в aiogram bank system!')
		await message.answer('Для просмотра команд введите /help')

	@dp.message_handler(commands="help")
	async def help(message:types.Message):
		await message.answer('/sign - вход\n/register - регистрация\n/info - информация о пользователе\n/balance - баланс\n/transfer - перевести')


	@dp.message_handler(commands="sign")
	async def sign_login(message:types.Message):
		await message.answer('Введите логин:')
		await SignState.login.set()

	@dp.message_handler(state=SignState.login)
	async def sign_password(message:types.Message, state:FSMContext):
		await state.update_data(login=message.text)
		await message.answer('Введите пароль:')
		await SignState.password.set()

	@dp.message_handler(state=SignState.password)
	async def sign_end(message:types.Message, state:FSMContext):
		await state.update_data(password=message.text)
		data = await storage.get_data(user=message.from_user.id)
		await state.finish() #остановка ФСМ
		#проверка на наличие этого пользователя в базе
		cursor.execute(f'''SELECT * FROM users WHERE login="{data['login']}" AND password="{data['password']}"''')
		data2 = cursor.fetchall()
		if data2 == []:
			await message.answer('Неверные данные для входа!')
			print('BANK: Неудачный вход (Неверные данные)')
		else:
			await message.answer('Успешный вход!')
			print('BANK: Успешный вход')
			#запоминание айди для дальнейших операций
			global id_
			id_ = data2[0][0]
			

	@dp.message_handler(commands="register")
	async def reg_login(message:types.Message):
		await message.answer('Придумайте логин:')
		await RegState.login.set()

	@dp.message_handler(state=RegState.login)
	async def reg_password(message:types.Message, state:FSMContext):
		await state.update_data(login=message.text)
		await message.answer("Придумайте пароль:")
		await RegState.password.set()

	@dp.message_handler(state=RegState.password)
	async def reg_age(message: types.Message, state:FSMContext):
		await state.update_data(password=message.text)
		await message.answer('Введите ваш возраст:')
		await RegState.age.set()

	@dp.message_handler(state=RegState.age)
	async def reg_end(message: types.Message, state:FSMContext):
		await state.update_data(age=message.text)
		data = await storage.get_data(user=message.from_user.id)
		await state.finish()

		#заполнение профиля
		first_name = message.from_user.first_name
		last_name = message.from_user.last_name
		age = data['age']
		login = data['login']
		password = data['password']
		balance = 0
		telegram_id = message.from_user.id

		#проверки перед записью в БД
		if password == '1234' or password == '1111': #проверка на наличие легкого пароля
			await message.answer('Придумайте надеждный пароль!')
			print('BANK: Неудачная регистрация (легкий пароль)')
		else:
			if int(age) < 14: #проверка на возраст
				await message.answer('Регистрация в банке возможна только с 14 лет!')
				print('BANK: Неудачная регистрация (меньше 14 лет)')
			else: #запись в БД и вход
				cursor.execute(f'''SELECT * FROM users WHERE login='{login}' ''')

				if cursor.fetchall() == []:
					cursor.execute(f'''INSERT INTO users(first_name, last_name, age, login, \
						password, balance, telegram_id) VALUES('{first_name}', '{last_name}', {age}, '{login}',\
						'{password}', {balance}, '{telegram_id}')''')
					connect.commit()

					#запоминание айди для дальнейших операций
					global id_
					id_ = login

					print('BANK: Успешная регистрация')
					await message.answer('Успешная регистрация!')
					await state.finish()
				else:
					print('BANK: Неудачная регистрация (логин существует)')
					await message.answer('Аккаунт с таким логином уже существует!')


	@dp.message_handler(commands="info")
	async def info(message:types.Message):
		try:
			print('BANK: Просмотр информации о пользователе')
			#поиск инофрмации о пользователе через айди
			cursor.execute(f'''SELECT * FROM users WHERE id={id_}''')
			data = cursor.fetchall()[0]
			await message.answer(f'ID: {id_}\nTG ID: {data[7]}\nИмя: {data[1]}\nФамилия: {data[2]}\nЛогин: {data[3]}\nВозраст: {data[5]}')
		except NameError:
			await message.answer('Войдите в аккаунт!')
			print('BANK: Неудачный просмотр информации о пользователе (нет аккаунта)')

	@dp.message_handler(commands="balance")
	async def balance(message:types.Message):
		try:
			print('BANK: Просмотр баланса')
			cursor.execute(f'''SELECT balance FROM users WHERE id={id_}''')
			await message.answer(f'Ваш текущий баланс: {cursor.fetchall()[0][0]} сом')
		except NameError:
			await message.answer('Войдите в аккаунт!')
			print('BANK: Неудачный просмотр баланса (нет аккаунта)')

	@dp.message_handler(commands="transfer")
	async def transfer_user(message:types.Message):
		try:
			a = id_ #проверка на наличиие аккаунта
			await message.answer('Введите ID получателя:')
			await TransState.user_id.set()
		except NameError:
			await message.answer('Войдите в аккаунт!')
			print('BANK: Неудачный перевод (нет аккаунта)')

	@dp.message_handler(state=TransState.user_id)
	async def transfer_summ(message: types.Message, state:FSMContext):
		await state.update_data(user_id=message.text)
		await message.answer('Введите сумму перевода:')
		await TransState.summ.set()

	@dp.message_handler(state=TransState.summ)
	async def transfer_password(message:types.Message,state:FSMContext):
		await state.update_data(summ=message.text)
		await message.answer('Введите пароль:')
		await TransState.password.set()

	@dp.message_handler(state=TransState.password)
	async def transfer_end(message:types.Message, state:FSMContext):
		await state.update_data(password=message.text) #обновление данных о пароле
		data = await storage.get_data(user=message.from_user.id) #получение информации о том что ввел пользователь
		await state.finish() #остановка ФСМ
		
		#заполнение информациии об операции
		user = data['user_id']
		summ = data['summ']
		password = data['password']

		#проверка на совпадение паролей
		cursor.execute(f'''SELECT password FROM users WHERE id={id_}''')
		data2 = cursor.fetchall()

		if data2[0][0] == password:
			cursor.execute(f'''SELECT telegram_id FROM users WHERE id={user}''')
			user_id = cursor.fetchall()
			if user_id == []: #проверка на наличие получателя
				await message.answer('Пользователь, которому вы хотите перевести деньги не найден!')
				print('BANK: Неудачный перевод (получатель не найден)')
			else: #проверка на наличие средств
				user_id = str(user_id)[str(user_id).find("'")+1:str(user_id).rfind("'")] #получение айди телеграма получателя для отправки уведомления
				cursor.execute(f'''SELECT balance FROM users WHERE id={id_}''') #получение информации о балансе отправителя
				balance = cursor.fetchall()[0][0]
				cursor.execute(f'''SELECT balance FROM users WHERE id={user}''') #получение информации о балансе получателя
				balance2 = cursor.fetchall()[0][0]
				if int(balance) < int(summ):
					await message.answer('Недостаточно средств!')
					print('BANK: Неудачный перевод (недостаточно средств)')
				else: #перевод денег
					#изменение информации в бд
					cursor.execute(f'''UPDATE users SET balance={int(balance) - int(summ)} WHERE id={id_}''')
					cursor.execute(f'''UPDATE users SET balance={int(balance2) + int(summ)} WHERE id={user}''')
					await bot.send_message(user_id, f'Вам было переведено {summ} сом.') #уведомление получателю
					await message.answer('Успешно!') #ответ отправителю
					print('BANK: Успешный перевод')
					connect.commit()
		else:
			await message.answer('Неверный пароль!')
			print('BANK: Неудачный перевод (неверный пароль)')


	executor.start_polling(dp)

except Exception: #при любой ошибки закрытие БД
	connect.close()
