from aiogram.fsm.state import State, StatesGroup

class Regestration(StatesGroup):
    name = State()
    age = State()
    confirm = State()