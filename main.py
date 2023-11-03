from aiogram import Dispatcher, Bot, executor, types
from config import TOKEN
from logging import basicConfig, INFO

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
basicConfig(level=INFO)

buttons = [
	types.KeyboardButton('О нас'),
	types.KeyboardButton('Объекты'),
	types.KeyboardButton('Контакты')
]
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

@dp.message_handler(commands='start')
async def comand(message: types.Message):
	await message.answer(f'Здравствуйте, {message.from_user.full_name}!', reply_markup=keyboard)

@dp.message_handler(text="О нас")
async def comand(message: types.Message):
	await message.answer('Американская торговая палата в Кыргызской Республике (Палата) – ведущая международная бизнес-ассоциация, которая стремится к созданию благоприятной и конкурентоспособной деловой среды в Кыргызской Республике.\
	 Палата объединяет более 80 крупных, средних и малых предприятия из разных отраслей экономики. Палата продвигает и защищает законные интересы местных и международных инвесторов, сделавших вклад в экономику Кыргызстана.')

@dp.message_handler(text="Объекты")
async def comand(message: types.Message):
	await message.answer('Здесь будет информация об обьектах')

@dp.message_handler(text="Контакты")
async def comand(message: types.Message):
	await message.answer_contact('+996 (312) 97 98 45', 'AmCham', 'Kyrgyzstan')
executor.start_polling(dp)