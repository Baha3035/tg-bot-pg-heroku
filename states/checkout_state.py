from aiogram.dispatcher.filters.state import StatesGroup, State

class CheckoutState(StatesGroup):
    check_cart = State()
    name = State()
    address = State() # address
    street = State() # new added
    phone = State() # new new new added
    confirm = State()