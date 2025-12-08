from aiogram.fsm.state import StatesGroup, State


class SmartphoneRecommendation(StatesGroup):
    waiting_for_budget = State()
    waiting_for_brand = State()
    waiting_for_features = State()
    showing_results = State()


class SmartphoneComparison(StatesGroup):
    waiting_for_first_model = State()
    waiting_for_second_model = State()


class SmartRecommendation(StatesGroup):
    waiting_for_budget = State()
    waiting_for_brands = State()
    waiting_for_features = State()
    waiting_for_additional = State()
    showing_preview = State()
    showing_results = State()
