
from aiogram.types import Message
from loader import dp, db
from handlers.user.menu import orders, orders_active, deactivate_orders
from filters import IsAdmin
from states.order_state import OrderAdminState

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders')
    
    if len(orders) == 0: await message.answer('У вас нет заказов.')
    else: await order_answer(message, orders)







@dp.message_handler(IsAdmin(), text=orders_active)
async def process_orders(message: Message):
    orders = db.fetchall('SELECT * FROM orders WHERE is_active=1')
    
    if len(orders) == 0: await message.answer('У вас нет заказов.')
    else: await order_answer(message, orders)



@dp.message_handler(IsAdmin(), text=deactivate_orders)
async def process_orders(message: Message):
    await OrderAdminState.id_for_update.set()
    #id = message.text
    #db.query('DELETE FROM cart WHERE cid=?', (cid,))
    #db.query('UPDATE orders SET is_active=0 WHERE ID=', (id,))
    #orders = db.fetchall('SELECT * FROM orders WHERE is_active=1')


@dp.message_handler(state=OrderAdminState.id_for_update)
async def process_question(message: Message):
    id = message.text
    print(message.text + "")
    db.query('UPDATE orders SET is_active=0 WHERE id=%s', (id,))
    # async with state.proxy() as data:
    #     data['question'] = message.text
    await message.answer('Деактивировано')
    await OrderAdminState.next()
    # await message.answer('Убедитесь, что все верно.', reply_markup=submit_markup())
    # await SosState.next()










async def order_answer(message, orders):

    res = ''
    #product_name = db.fetchone('SELECT title FROM products WHERE idx=?', (order[3][:len(order[3])-2],))[0]
    for order in orders:
        print(order[0])
        #print(("'"+(order[6][:len(order[6])-2])+"'"))
        all_product_ids_counts = db.fetchall('SELECT product_id, product_count FROM orders_and_products WHERE order_id=%s', (order[0],))
        dict_of_name_count = {}
        for x, y in all_product_ids_counts:
            product_name = db.fetchone('SELECT title FROM products WHERE idx=%s', (x,))[0]
            product_count = y
            dict_of_name_count[product_name]=product_count
        #product_names = db.fetchall('SELECT title FROM products WHERE idx=(SELECT )', (("'"+(order[6][:len(order[6])-2])+"'"),))[0]
        #count = order[6][-2:]
        id = order[0]
        usr_name = order[2]
        usr_address = order[3]
        usr_street = order[4]
        usr_phone = order[5]
        res += f'Заказ <b>ID: {id}\nИмя: {usr_name}</b>\nРайон: {usr_address}\nУлица и дом: {usr_street}\nНомер телефона: {usr_phone}\nПродукты: {dict_of_name_count}\n\n'

    await message.answer(res)