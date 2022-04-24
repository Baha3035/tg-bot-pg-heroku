from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from loader import dp
from filters import IsAdmin, IsUser

catalog = '🛍️ Каталог'
#balance = '💰 Баланс'
cart = '🛒 Корзина'
delivery_status = '🚚 Статус заказа'

settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
deactivate_orders = '❤️‍🩹 Деактивировать заказ'
orders_active = '🙅‍♂️ Заказы которые еще не взяли курьеры'
questions = '❓ Вопросы'

@dp.message_handler(IsAdmin(), commands='admintokensecret43274932rur8ryhf37ry734r23y329r3289ru')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions, orders)
    markup.add(orders_active)
    markup.add(deactivate_orders)

    await message.answer('Меню', reply_markup=markup)

@dp.message_handler(IsUser(), commands='menu')
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(cart)
    markup.add(delivery_status)
    print("MFFF")
    await message.answer('Выберите товар для покупки', reply_markup=markup)
