from aiogram.fsm.state import State, StatesGroup

class SendLogin(StatesGroup):
    bot = State()
    email = State()
    password = State()
    ssh_link = State()
    ssh_login = State()
    ssh_pass = State()
    confirm = State()
