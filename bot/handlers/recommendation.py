import logging
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import SmartphoneRecommendation
from bot.keyboards.inline import InlineKeyboardBuilder, InlineKeyboardButton
from utils.validators import is_valid_budget

logger = logging.getLogger(__name__)
router = Router(name="recommendation")


@router.message(Command("recommend"))
async def start_recommendation(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started recommendation process.")

    await state.set_state(SmartphoneRecommendation.waiting_for_budget)
    await message.answer(
        "<b>Подбор смартфона:</b>\n\n"
        "Введите бюджет в долларах:"
    )


@router.message(SmartphoneRecommendation.waiting_for_budget)
async def process_budget(message: Message, state: FSMContext):
    user_input = message.text
    is_valid, budget = is_valid_budget(user_input)
    if not is_valid:
        await message.answer(
            "<b>Некорректный бюджет.</b>\n\n"
            "Введите сумму от 30 до 4000 долларов:"
        )
        return

    await state.update_data(budget=budget)
    logger.info(f"User {message.from_user.id} set budget: {budget}$.")
    await state.set_state(SmartphoneRecommendation.waiting_for_brand)
    keyboard = get_brands_keyboard()
    await message.answer(
        "Есть ли предпочтения по бренду?",
        reply_markup=keyboard
    )


def get_brands_keyboard():
    builder = InlineKeyboardBuilder()
    brands = [
        ("Samsung", "brand:samsung"),
        ("iPhone", "brand:iphone"),
        ("Google Pixel", "brand:google"),
        ("Xiaomi", "brand:xiaomi"),
        ("Huawei", "brand:huawei"),
        ("Любой", "brand:any")
    ]
    for brand_name, brand_data in brands:
        builder.button(
            text=brand_name,
            callback_data=brand_data
        )

    return builder.adjust(2).as_markup()


@router.callback_query(
    SmartphoneRecommendation.waiting_for_brand,
    F.data.startswith("brand:")
)
async def process_brand(callback: CallbackQuery, state: FSMContext):
    brand = callback.data.split(":")[1]
    await state.update_data(brand=brand)
    logger.info(f"User {callback.from_user.id} selected brand: {brand}.")
    await state.set_state(SmartphoneRecommendation.waiting_for_features)
    keyboard = get_features_keyboard()

    data = await state.get_data()
    budget = data["budget"]
    brand_name = get_brand_display_name(brand)

    await callback.message.edit_text(
        f"Подобрать смартфон под бюджет: {budget}$ для {brand_name}",
        "Что для вас наиболее важно в смартфоне?",
        reply_markup=keyboard
    )
    await callback.answer()


def get_brand_display_name(brand):
    brands = {
        "samsung": "Samsung",
        "iphone": "iPhone",
        "google": "Google Pixel",
        "xiaomi": "Xiaomi",
        "huawei": "Huawei",
        "any": "любого бренда"
    }
    return brands.get(brand, brand)


def get_features_keyboard():
    builder = InlineKeyboardBuilder()
    features = [
        ("Камера", "feature:camera"),
        ("Батарея", "feature:battery"),
        ("Экран", "feature:screen"),
        ("Производительность", "feature:performance"),
        ("Память", "feature:storage")
    ]
    for feature_name, feature_data in features:
        builder.button(
            text=feature_name,
            callback_data=feature_data
        )
    builder.button(
        text="Готово, подобрать",
        callback_data="features:done"
    )

    return builder.adjust(2, 2, 1, 1).as_markup()


@router.callback_query(
    SmartphoneRecommendation.waiting_for_features,
    F.data.startswith("feature:")
)
async def procces_feature_toggle(
        callback: CallbackQuery,
        state: FSMContext
):
    feature = callback.data.split(":")[1]
    data = await state.get_data()
    features = data.get("features", [])
    if feature in features:
        features.remove(feature)
    else:
        features.append(feature)

    await state.update_data(features=features)
    logger.info(f"User {callback.from_user.id} selected features: {features}.")

    keyboard = get_features_keyboard_with_marks()

    try:
        await callback.message.edit_reply_markup(
            reply_markup=keyboard
        )
    except Exception:
        pass

    await callback.answer(
        f"{'Добавлено' if feature in features else 'Удалено'}"
    )


def get_features_keyboard_with_marks(selected_features):
    builder = InlineKeyboardBuilder()

    features = [
        ("Камера", "feature:camera"),
        ("Батарея", "feature:battery"),
        ("Экран", "feature:screen"),
        ("Производительность", "feature:performance"),
        ("Память", "feature:storage")
    ]

    for feature_code, feature_name in features:
        text = f"{'Готово' if feature_code in selected_features else ''}{feature_name}"

        builder.button(
            text=text,
            callback_data=feature_code
        )

    builder.button(
        text="Готово, подобрать",
        callback_data="features:done"
    )

    return builder.adjust(2, 2, 1, 1).as_markup()


@router.callback_query(
    SmartphoneRecommendation.waiting_for_features,
    F.data == "features:done"
)
async def finish_recommendation(
    callback: CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()
    budget = data["budget"]
    brand = data["brand"]
    features = data.get("features", [])
    logger.info(
        f"User {callback.from_user.id} completed recommendation. ",
        f"Budget: {budget}, Brand: {brand}, Features: {features}"
        )

    brand_name = get_brand_display_name(brand)
    features_text = get_features_display(features)

    result_text = (
        "Смартфон подобран, подходящий для вас:\n",
        f"Бюджет: {budget}$\n",
        f"Бренд: {brand_name}\n",
        f"Характеристики: {features_text}"
    )
    await callback.message.edit_text(result_text)
    await state.clear()
    await callback.answer("Подбор смартфона завершен")


def get_features_display(features):
    if not features:
        return "<i>Нет</i>"

    feature_names = {
        "camera": "Камера",
        "battery": "Батарея",
        "screen": "Экран",
        "performance": "Производительность",
        "storage": "Память"
    }

    display_names = [feature_names.get(f, f) for f in features]
    return ", ".join(display_names)


@router.message(
    Command("cancel"),
    StateFilter(SmartphoneRecommendation)
)
async def cancel_recommendation(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} cancelled recommendation.")
    await state.clear()

    await message.answer(
        "Подбор смартфона отменен.\n\n",
        "Чтобы начать заново, используйте команду /recommend."
    )
