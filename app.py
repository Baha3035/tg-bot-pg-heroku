import os
import handlers
from handlers import user
from handlers import admin
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging


filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = 'Покупатель'
admin_message = 'Поставщик'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    #markup.row(user_message, admin_message)
    await user.menu.user_menu(message)
#     await message.answer('''Привет! 👋

# 🤖 Я бот-магазин по пpодаже натуральных товаров .
    
# 🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся товары возпользуйтесь командой /menu.

# ❓ Возникли вопросы? Не проблема! Команда /sos поможет связаться с админами, которые постараются как можно быстрее откликнуться.

# ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):

    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)
    # await user.menu.user_menu(message)  # Менюшка на пользователе
    await message.answer('Включен пользовательский режим.', reply_markup=ReplyKeyboardRemove())
    await user.menu.user_menu(message)  # Менюшка на пользователе

@dp.message_handler(commands=['bhutavy'])
async def admin_mode(message: types.Message):

    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Включен админский режим.', reply_markup=ReplyKeyboardRemove())
    await user.menu.admin_menu(message)

async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
