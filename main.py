#импорт модулей
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
from logging import basicConfig, INFO
import sqlite3

try:
	bot = Bot(token=TOKEN)
	storage = MemoryStorage()
	dp = Dispatcher(bot, storage=storage)
	connect = sqlite3.connect('todo.db')
	cursor = connect.cursor()

	cursor.execute('''CREATE TABLE IF NOT EXISTS todo(
		id INTEGER PRIMARY KEY,
		nickname TEXT VARCHAR(255),
		to_do TEXT
		)''')
	basicConfig(level=INFO)

	class CreateState(StatesGroup):
		todo = State()

	class DeleteState(StatesGroup):
		id_ = State()

	@dp.message_handler(commands="start")
	async def start(message:types.Message):
		await message.answer('Добро пожаловать в TODO bot!')
		await message.answer('Введите /help для просмотра списка команд')

	@dp.message_handler(commands="help")
	async def help(message:types.Message):
		await message.answer('/create - создать строку списка дел')
		await message.answer('/list - просмотреть список дел')
		await message.answer('/delete - удалить строку из списка дел')


	@dp.message_handler(commands="create")
	async def create_todo(message: types.Message):
		await message.answer('Введите строку которую хотите создать')
		await CreateState.todo.set()

	@dp.message_handler(state=CreateState.todo)
	async def create_end(message:types.message, state:FSMContext):
		await state.update_data(todo=message.text)
		data = await storage.get_data(user=message.from_user.id)
		await state.finish()
		cursor.execute(f'''INSERT INTO todo(nickname, to_do) VALUES('{message.from_user.username}', '{data['todo']}')''')
		connect.commit()
		cursor.execute(f'''SELECT id FROM todo WHERE nickname='{message.from_user.username}' AND to_do='{data['todo']}' ''')
		await message.answer(f'Запись создана! ID: {cursor.fetchall()[0][0]}')


	@dp.message_handler(commands="list")
	async def list_(message:types.Message):
		cursor.execute(f'''SELECT * FROM todo WHERE nickname='{message.from_user.username}' ''')
		data = cursor.fetchall()

		i = 0
		for j in data:
			await message.answer(f'{data[i][0]}: {data[i][2]}')
			i += 1


	@dp.message_handler(commands="delete")
	async def delete_todo(message: types.Message):
		await message.answer('Введите ID строки которую хотите удалить')
		await DeleteState.id_.set()

	@dp.message_handler(state=DeleteState.id_)
	async def delete_end(message:types.message, state:FSMContext):
		await state.update_data(id_=message.text)
		data = await storage.get_data(user=message.from_user.id)
		await state.finish()
		cursor.execute(f'''SELECT * FROM todo WHERE id={data['id_']}''')
		if cursor.fetchall() == []:
			await message.answer('Запись не найдена')
		else:
			cursor.execute(f'''DELETE FROM todo WHERE id={data['id_']}''')
			connect.commit()

			await message.answer('Запись удалена!')

	@dp.message_handler()
	async def notdefind(message:types.Message):
		await message.answer('Команда не найдена')


	executor.start_polling(dp)
except Exception:
	connect.close()