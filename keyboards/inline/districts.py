from dis import dis
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

district_cb = CallbackData('district', 'distr_name')

def district_markup():

    global district_cb

    markup = InlineKeyboardMarkup()
    distr_btn1 = InlineKeyboardButton('6-микрорайон', callback_data=district_cb.new(distr_name='6-микрорайон'))
    distr_btn2 = InlineKeyboardButton('7-микрорайон', callback_data=district_cb.new(distr_name='7-микрорайон'))
    distr_btn3 = InlineKeyboardButton('8-микрорайон', callback_data=district_cb.new(distr_name='8-микрорайон'))
    distr_btn4 = InlineKeyboardButton('10-микрорайон', callback_data=district_cb.new(distr_name='10-микрорайон'))
    distr_btn5 = InlineKeyboardButton('11-микрорайон', callback_data=district_cb.new(distr_name='11-микрорайон'))
    distr_btn6 = InlineKeyboardButton('12-микрорайон', callback_data=district_cb.new(distr_name='12-микрорайон'))
    distr_btn7 = InlineKeyboardButton('Асанбай', callback_data=district_cb.new(distr_name='Асанбай')) 
    markup.add(distr_btn1)
    markup.add(distr_btn2)
    markup.add(distr_btn3)
    markup.add(distr_btn4)
    markup.add(distr_btn5)
    markup.add(distr_btn6)
    markup.add(distr_btn7)

    return markup