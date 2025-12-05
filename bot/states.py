from aiogram.fsm.state import StatesGroup, State


class SmartphoneRecommendation(StatesGroup):
    waiting_for_budget = State()
    waiting_for_brand = State()
    waiting_for_features = State()
    showing_results = State()


class SmartphoneComparison(StatesGroup):
    waiting_for_first_model = State()
    waiting_for_second_model = State()
