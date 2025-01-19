from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt = KeyboardButton(text='Рассчитать')
bt2 = KeyboardButton(text='Информация')
bt3 = KeyboardButton(text='Купить')
kb.row(bt, bt2)
kb.add(bt3)

ikb = InlineKeyboardMarkup()
ibt = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ibt2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb.row(ibt, ibt2)

ikb2 = InlineKeyboardMarkup(resize_keyboard=True)
ibt3 = InlineKeyboardButton(text='Для ясности ума', callback_data='product_buying')
ibt4 = InlineKeyboardButton(text='Для очищения', callback_data='product_buying')
ibt5 = InlineKeyboardButton(text='Для понимания', callback_data='product_buying')
ibt6 = InlineKeyboardButton(text='Для легкости', callback_data='product_buying')
ikb2.row(ibt3, ibt4)
ikb2.row(ibt5, ibt6)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Название: Продукт {i} | Описание: Описание {i} | Цена: {i*100}')
        with open(f'pictures/{i}pills.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=ikb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес (кг) + 6,25 * рост (см) – 5 * возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    formula = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма каллорий: {formula} ккал в сутки')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
