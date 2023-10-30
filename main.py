from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN
from random import randint

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

num = str(randint(1, 3))
IMAGE_1 = "https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg"
IMAGE_2 = "https://media.makeameme.org/created/sorry-you-lose.jpg"

print('Бот запущен!')

@dp.message_handler(commands="start")
async def start(message: types.Message):
	await message.answer('Я загадал число от 1 до 3, угадайте его!')

@dp.message_handler(text="1")
async def ans_1(message: types.Message):
	if num == '1':
		await message.answer_photo(IMAGE_1)
	else:
		await message.answer_photo(IMAGE_2)

@dp.message_handler(text="2")
async def ans_2(message: types.Message):
	if num == '2':
		await message.answer_photo(IMAGE_1)
	else:
		await message.answer_photo(IMAGE_2)

@dp.message_handler(text="3")
async def ans_3(message: types.Message):
	if num == '3':
		await message.answer_photo(IMAGE_1)
	else:
		await message.answer_photo(IMAGE_2)


executor.start_polling(dp)