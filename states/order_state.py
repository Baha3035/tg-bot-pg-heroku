from aiogram.dispatcher.filters.state import StatesGroup, State

class OrderAdminState(StatesGroup):
    id_for_update = State()