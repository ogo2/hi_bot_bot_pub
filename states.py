from aiogram.fsm.state import StatesGroup, State

class Breef_state(StatesGroup):
    name_state = State()
    email_state = State()
    phone_state = State()
    message_state = State()
    message_state_user_id = State()
    
    
    
class Communi_state(StatesGroup):
    name_state_communi = State()
    phone_state_communi = State()
    message_state_communi = State()
