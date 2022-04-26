import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.districts import district_markup, district_cb
from keyboards.inline.products_from_cart import product_markup, product_cb
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import *
from aiogram.types.chat import ChatActions
from states import CheckoutState
from loader import dp, db, bot
from filters import IsUser
from .menu import cart


@dp.message_handler(IsUser(), text=cart)
async def process_cart(message: Message, state: FSMContext):
    print('Doesnt respond?')
    cart_data = db.fetchall(
        'SELECT * FROM cart WHERE cid=%s', (message.chat.id,))
    print(cart_data)
    if len(cart_data) == 0:

        await message.answer('Ваша корзина пуста.')

    else:
        print("Got to bee working man")
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        async with state.proxy() as data:
            data['products'] = {}

        order_cost = 0

        for idx, _, count_in_cart in cart_data:

            product = db.fetchone('SELECT * FROM products WHERE idx=%s', (idx,))

            if product == None:

                db.query('DELETE FROM cart WHERE idx=%s', (idx,))

            else:
                _, title, body, image, price, _ = product
                order_cost += price

                async with state.proxy() as data:
                    data['products'][idx] = [title, price, count_in_cart]

                markup = product_markup(idx, count_in_cart)
                text = f'<b>{title}</b>\n\n{body}\n\nЦена: {price} сомов.'

                await message.answer_photo(photo=image,
                                           caption=text,
                                           reply_markup=markup)

        if order_cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('📦 Оформить заказ')

            await message.answer('Перейти к оформлению?',
                                 reply_markup=markup)


@dp.callback_query_handler(IsUser(), product_cb.filter(action='count'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='increase'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='decrease'))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):

    idx = callback_data['id']
    action = callback_data['action']
    if 'count' == action:

        async with state.proxy() as data:

            if 'products' not in data.keys():

                await process_cart(query.message, state)

            else:

                await query.answer('Количество - ' + str(data['products'][int(idx)][2]))

    else:

        async with state.proxy() as data:

            if 'products' not in data.keys():

                await process_cart(query.message, state)

            else:
                #print(data['products'])
                #print("This is itttt",data['products'][int(idx)])
                data['products'][int(idx)][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][int(idx)][2]

                if count_in_cart == 0:

                    db.query('''DELETE FROM cart
                    WHERE cid = %s AND idx = %s''', (query.message.chat.id, int(idx)))

                    await query.message.delete()
                else:

                    db.query('''UPDATE cart 
                    SET quantity = %s 
                    WHERE cid = %s AND idx = %s''', (count_in_cart, query.message.chat.id, int(idx)))

                    await query.message.edit_reply_markup(product_markup(idx, count_in_cart))





@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='6-микрорайон'), state=CheckoutState.address)
@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='7-микрорайон'), state=CheckoutState.address)
@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='8-микрорайон'), state=CheckoutState.address)
@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='10-микрорайон'), state=CheckoutState.address)
@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='11-микрорайон'), state=CheckoutState.address)
@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='12-микрорайон'), state=CheckoutState.address)
@dp.callback_query_handler(IsUser(), district_cb.filter(distr_name='Асанбай'), state=CheckoutState.address)
async def process_address(query: CallbackQuery, callback_data: dict, state: FSMContext):
    #print("Vostok 5")
    distr_name = callback_data['distr_name']
    async with state.proxy() as data:
        data['address'] = distr_name

    #await confirm(query.message)
    await CheckoutState.next()
    await query.message.answer('''Укажите свою улицу, дом и квартиру.''',
                                 reply_markup=back_markup())







@dp.message_handler(IsUser(), text='📦 Оформить заказ')
async def process_checkout(message: Message, state: FSMContext):

    await CheckoutState.check_cart.set()
    await checkout(message, state)


async def checkout(message, state):
    answer = ''
    total_price = 0

    async with state.proxy() as data:

        for title, price, count_in_cart in data['products'].values():

            tp = count_in_cart * price
            answer += f'<b>{title}</b> * {count_in_cart}шт. = {tp}сом\n'
            total_price += tp

    await message.answer(f'{answer}\nОбщая сумма заказа: {total_price} сом.',
                         reply_markup=check_markup())


@dp.message_handler(IsUser(), lambda message: message.text not in [all_right_message, back_message], state=CheckoutState.check_cart)
async def process_check_cart_invalid(message: Message):
    await message.reply('Такого варианта не было.')


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.check_cart)
async def process_check_cart_back(message: Message, state: FSMContext):
    await state.finish()
    await process_cart(message, state)


@dp.message_handler(IsUser(), text=all_right_message, state=CheckoutState.check_cart)
async def process_check_cart_all_right(message: Message, state: FSMContext):
    await CheckoutState.next()
    await message.answer('Укажите свое имя.',
                         reply_markup=back_markup())



@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.name)
async def process_name_back(message: Message, state: FSMContext):
    await CheckoutState.check_cart.set()
    await checkout(message, state)


@dp.message_handler(IsUser(), state=CheckoutState.name)
async def process_name(message: Message, state: FSMContext):

    async with state.proxy() as data:

        data['name'] = message.text


        if 'address' in data.keys():

            await confirm(message)
            await CheckoutState.confirm.set()

        else:

            await CheckoutState.next()
            await message.answer('''Укажите район в котором вы живете.''',
                                 reply_markup=district_markup())


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.address)
async def process_address_back(message: Message, state: FSMContext):

    async with state.proxy() as data:

        await message.answer('Изменить имя с <b>' + data['name'] + '</b>?',
                             reply_markup=back_markup())

    await CheckoutState.name.set()



# @dp.message_handler(IsUser(), state=CheckoutState.address)
# async def process_address(message: Message, state: FSMContext):

#     async with state.proxy() as data:
#         data['address'] = message.text

#     #await confirm(message)
#     await CheckoutState.next()
#     await message.answer('''Укажите свою улицу.''',
#                                  reply_markup=back_markup())


async def confirm(message):

    await message.answer('Убедитесь, что все правильно оформлено и подтвердите заказ.',
                         reply_markup=confirm_markup())


# @dp.message_handler(IsUser(), lambda message: message.text not in [confirm_message, back_message], state=CheckoutState.confirm)
# async def process_confirm_invalid(message: Message):
#     await message.reply('Такого варианта не было.')


# @dp.message_handler(IsUser(), text=back_message, state=CheckoutState.confirm)
# async def process_confirm(message: Message, state: FSMContext):

#     await CheckoutState.address.set()

#     async with state.proxy() as data:
#         await message.answer('Изменить адрес с <b>' + data['address'] + '</b>?',
#                              reply_markup=back_markup())








@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.street)
async def process_confirm(message: Message, state: FSMContext):

    await CheckoutState.address.set()

    async with state.proxy() as data:
        await message.answer('Изменить район с <b>' + data['address'] + '</b>?',
                             reply_markup=district_markup())






@dp.message_handler(IsUser(), state=CheckoutState.street)
async def process_address(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['street'] = message.text

    #await confirm(message)
    await CheckoutState.next()
    await message.answer('Укажите свой номер телефона.',
                         reply_markup=back_markup())






@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.phone)
async def process_confirm(message: Message, state: FSMContext):

    await CheckoutState.street.set()

    async with state.proxy() as data:
        await message.answer('Изменить улицу с <b>' + data['street'] + '</b>?',
                             reply_markup=district_markup())






@dp.message_handler(IsUser(), state=CheckoutState.phone)
async def process_address(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['phone'] = message.text

    await confirm(message)
    await CheckoutState.next()


@dp.message_handler(IsUser(), lambda message: message.text not in [confirm_message, back_message], state=CheckoutState.confirm)
async def process_confirm_invalid(message: Message):
    await message.reply('Такого варианта не было.')


@dp.message_handler(IsUser(), text=back_message, state=CheckoutState.confirm)
async def process_confirm(message: Message, state: FSMContext):

    await CheckoutState.street.set()

    async with state.proxy() as data:
        await message.answer('Изменить телефонный номер с <b>' + data['phone'] + '</b>?',
                             reply_markup=back_markup())






@dp.message_handler(IsUser(), text=confirm_message, state=CheckoutState.confirm)
async def process_confirm(message: Message, state: FSMContext):

    enough_money = True  # enough money on the balance sheet
    markup = ReplyKeyboardRemove()

    if enough_money:

        logging.info('Deal was made.')

        async with state.proxy() as data:

            cid = message.chat.id
            # products = [idx + '=' + str(quantity)
            #             for idx, quantity in db.fetchall('''SELECT idx, quantity FROM cart
            # WHERE cid=%s''', (cid,))]  # idx=quantity



            # db.query('INSERT INTO orders (cid, usr_name, usr_address, usr_street, usr_phone,is_active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
            #          (cid, data['name'], data['address'], data['street'], data['phone'], 1))
            # id_of_the_order = db.fetchone()[0]

            db.cur.execute('INSERT INTO orders (cid, usr_name, usr_address, usr_street, usr_phone,is_active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
                     (cid, data['name'], data['address'], data['street'], data['phone'], 1))
            id_of_the_order = db.cur.fetchone()[0]
            db.conn.commit()
            #db.conn.close()

            for idx, quantity in db.fetchall('''SELECT idx, quantity FROM cart WHERE cid=%s''', (cid,)):
                db.query('INSERT INTO orders_and_products (order_id, product_id, product_count) VALUES (%s, %s, %s)',
                         (id_of_the_order, int(idx), quantity))


            db.query('DELETE FROM cart WHERE cid=%s', (cid,))

            await message.answer('Ок! Ваш заказ уже в пути 🚀\nИмя: <b>' + data['name'] + '</b>\nРайон: <b>' + data['address'] + '</b>\nУлица: <b>' + data['street'] + '</b>\nТелефонный номер: <b>' + data['phone'] + '</b>\nЧтобы вернуться в меню воспользуйтесь командой /start <b>' + '</b>',
                                 reply_markup=markup)
            print('Не сработало')
    else:

        await message.answer('У вас недостаточно денег на счете. Пополните баланс!',
                             reply_markup=markup)

    await state.finish()
