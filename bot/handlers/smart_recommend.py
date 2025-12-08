import logging
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.states import SmartRecommendation
from bot.keyboards.inline import get_main_menu, get_cancel_keyboard
from utils.validators import is_valid_budget

logger = logging.getLogger(__name__)
router = Router(name="smart_recommend")


@router.callback_query(F.data == "recommend:smart")
async def start_smart_recommendation(
    callback: CallbackQuery,
    state: FSMContext
):
    logger.info(f"User {callback.from_user.id} started smart recommendation.")

    await state.set_state(SmartRecommendation.waiting_for_budget)

    await callback.message.edit_text(
        "<b>Умный подбор смартфона</b>\n\n"
        "Я задам вам несколько вопросов и подберу смартфон для вас!\n\n"
        "Укажите ваш примерный бюджет, в долларах:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(SmartRecommendation.waiting_for_budget)
async def process_budget(message: Message, state: FSMContext):
    is_valid, budget = is_valid_budget(message.text)

    if not is_valid:
        logger.warning(
            f"User {message.from_user.id} "
            f"entered invalid budget: {message.text}"
                       )
        await message.answer(
            "<b>Некорректный бюджет.</b>\n\n"
            "Введите сумму от 30 до 4000 долларов:",
            reply_markup=get_cancel_keyboard()
        )
        return

    await state.update_data(budget=budget)
    logger.info(f"User {message.from_user.id} set budget: {budget}$.")

    await state.set_state(SmartRecommendation.waiting_for_brands)
    keyboard = get_brands_selection_keyboard()
    await message.answer(
        "Есть ли предпочтения по бренду?\n"
        "Выберите один или несколько брендов:",
        reply_markup=keyboard
    )


def get_brands_selection_keyboard(selected_brands=None):
    if selected_brands is None:
        selected_brands = []
    builder = InlineKeyboardBuilder()

    brands = [
        ("Apple", "brand:apple"),
        ("Samsung", "brand:samsung"),
        ("Google", "brand:google"),
        ("Xiaomi", "brand:xiaomi"),
        ("Huawei", "brand:huawei"),
    ]

    for brand_name, brand_data in brands:
        brand_id = brand_data.split(":")[1]
        mark = "✅ " if brand_id in selected_brands else ""
        builder.button(
            text=f"{mark}{brand_name}",
            callback_data=brand_data
        )

    builder.button(text="Пропустить", callback_data="brands:skip")
    builder.button(text="Далее", callback_data="brands:next")
    builder.button(text="Назад", callback_data="brands:back")
    builder.button(text="Отменить", callback_data="action:cancel")

    return builder.adjust(2, 2, 2, 1, 1, 1, 1).as_markup()


@router.callback_query(
    SmartRecommendation.waiting_for_brands,
    F.data.startswith("brand:")
)
async def toggle_brand_selection(
    callback: CallbackQuery,
    state: FSMContext
):
    brand = callback.data.split(":")[1]

    data = await state.get_data()
    selected_brands = data.get("selected_brands", [])

    if brand in selected_brands:
        selected_brands.remove(brand)
        logger.info(f"User {callback.from_user.id} deselected brand: {brand}")
    else:
        selected_brands.append(brand)
        logger.info(f"User {callback.from_user.id} selected brand: {brand}")

    await state.update_data(selected_brands=selected_brands)

    keyboard = get_brands_selection_keyboard(selected_brands)

    try:
        await callback.message.edit_reply_markup(
            reply_markup=keyboard
        )
    except Exception:
        pass

    await callback.answer()


@router.callback_query(
    SmartRecommendation.waiting_for_brands,
    F.data == "brands:skip"
)
async def skip_brands(
    callback: CallbackQuery,
    state: FSMContext
):
    logger.info(f"User {callback.from_user.id} skipped brands selection.")

    await state.update_data(selected_brands=[])

    await state.set_state(SmartRecommendation.waiting_for_features)

    keyboard = get_features_selection_keyboard()
    await callback.message.edit_text(
        "Что для вас наиболее важно в смартфоне?\n"
        "Выберите наиболее важные параметры для вас:",
        reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(
    SmartRecommendation.waiting_for_brands,
    F.data == "brands:next"
)
async def brands_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_brands = data.get("selected_brands", [])
    logger.info(
        f"User {callback.from_user.id} "
        f"selected brands: {selected_brands}"
    )

    await state.set_state(SmartRecommendation.waiting_for_features)

    keyboard = get_features_selection_keyboard()
    await callback.message.edit_text(
        "Что для вас наиболее важно в смартфоне?\n"
        "Выберите наиболее важные параметры для вас:",
        reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(
    SmartRecommendation.waiting_for_brands,
    F.data == "brands:back"
)
async def brands_back(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} backed to budget selection.")

    await state.set_state(SmartRecommendation.waiting_for_budget)

    await callback.message.edit_text(
        "Введите новый бюджет, либо пропустите этот шаг.",
        reply_markup=get_budget_navigation_keyboard()
    )
    await callback.answer()


def get_budget_navigation_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Далее", callback_data="budget:next")
    builder.button(text="Отменить", callback_data="action:cancel")

    return builder.adjust(1).as_markup()


@router.callback_query(
    SmartRecommendation.waiting_for_budget,
    F.data == "budget:next"
)
async def budget_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    budget = data.get("budget")

    if not budget:
        await callback.answer(
            "Вы не ввели бюджет. Пожалуйста, введите бюджет!",
            show_alert=True
        )
        return

    await state.set_state(SmartRecommendation.waiting_for_brands)

    keyboard = get_brands_selection_keyboard()
    await callback.message.edit_text(
        "Есть ли предпочтения по бренду?\n"
        "Выберите один или несколько брендов:",
        reply_markup=keyboard
    )
    await callback.answer()


def get_features_selection_keyboard(selected_features=None):
    if selected_features is None:
        selected_features = []

    builder = InlineKeyboardBuilder()

    features = [
        ("Камера", "feature_select:camera"),
        ("Батарея", "feature_select:battery"),
        ("Экран", "feature_select:screen"),
        ("Производительность", "feature_select:performance"),
        ("Память", "feature_select:storage"),
        ("Игры", "feature_select:gaming")
    ]

    for feature_name, feature_data in features:
        feature_id = feature_data.split(":")[1]
        mark = "✅ " if feature_id in selected_features else ""
        builder.button(
            text=f"{mark}{feature_name}",
            callback_data=feature_data
        )

    builder.button(text="Пропустить", callback_data="features:skip")
    builder.button(text="Далее", callback_data="features:next")
    builder.button(text="Назад", callback_data="features:back")
    builder.button(text="Отменить", callback_data="action:cancel")

    return builder.adjust(2, 2, 2, 1, 1, 1, 1).as_markup()


@router.callback_query(
    SmartRecommendation.waiting_for_features,
    F.data.startswith("feature_select:")
)
async def toggle_feature_selection(callback: CallbackQuery, state: FSMContext):
    feature = callback.data.split(":")[1]

    data = await state.get_data()
    selected_features = data.get("selected_features", [])

    if feature in selected_features:
        selected_features.remove(feature)
    else:
        selected_features.append(feature)

    await state.update_data(selected_features=selected_features)

    keyboard = get_features_selection_keyboard(selected_features)

    try:
        await callback.message.edit_reply_markup(
            reply_markup=keyboard
        )
    except Exception:
        pass

    await callback.answer()


@router.callback_query(
    SmartRecommendation.waiting_for_features,
    F.data == "features:skip"
)
async def skip_features(callback: CallbackQuery, state: FSMContext):
    await state.update_data(selected_features=[])

    await state.set_state(SmartRecommendation.waiting_for_additional)

    await callback.message.edit_text(
        "Есть ли предпочтения по дополнительным характеристикам?\n"
        "<i>Например: хочу компактный смартфон, наличие 3.5mm jack</i>\n"
        "Напишите текстом свои пожелания, либо пропустите этот шаг.",
        reply_markup=get_additional_navigation_keyboard()
    )
    await callback.answer()


@router.callback_query(
    SmartRecommendation.waiting_for_features,
    F.data == "features:next"
)
async def features_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_features = data.get("selected_features", [])
    logger.info(
        f"User {callback.from_user.id} "
        f"selected features: {selected_features}"
    )

    await state.set_state(SmartRecommendation.waiting_for_additional)

    await callback.message.edit_text(
        "Есть ли предпочтения по дополнительным характеристикам?\n"
        "<i>Например: хочу компактный смартфон, наличие 3.5mm jack</i>\n"
        "Напишите текстом свои пожелания, либо пропустите этот шаг.",
        reply_markup=get_additional_navigation_keyboard()
    )
    await callback.answer()


@router.callback_query(
    SmartRecommendation.waiting_for_features,
    F.data == "features:back"
)
async def features_back(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} went back to brands.")

    await state.set_state(SmartRecommendation.waiting_for_brands)

    data = await state.get_data()
    selected_brands = data.get("selected_brands", [])

    keyboard = get_brands_selection_keyboard(selected_brands)
    await callback.message.edit_text(
        "Есть ли предпочтения по бренду?\n"
        "Выберите один или несколько брендов:",
        reply_markup=keyboard
    )
    await callback.answer()


def get_additional_navigation_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Пропустить", callback_data="additional:skip")
    builder.button(text="Назад", callback_data="additional:back")
    builder.button(text="Отменить", callback_data="action:cancel")

    return builder.adjust(1).as_markup()


@router.message(SmartRecommendation.waiting_for_additional)
async def process_additional(message: Message, state: FSMContext):
    additional_text = message.text.strip()

    if len(additional_text) > 500:
        await message.answer(
            "Текст слишком длинный.",
            reply_markup=get_additional_navigation_keyboard()
        )
        return

    await state.update_data(additional_params=additional_text)
    logger.info(
        f"User {message.from_user.id} "
        f"wrote additional params: {additional_text[:100]}"
    )

    await show_preview(message, state)


@router.callback_query(
    SmartRecommendation.waiting_for_additional,
    F.data == "additional:skip"
)
async def skip_additional(callback: CallbackQuery, state: FSMContext):
    await state.update_data(additional_params="")

    await show_preview(callback, state)


@router.callback_query(
    SmartRecommendation.waiting_for_additional,
    F.data == "additional:back"
)
async def additional_back(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} went back to features.")

    await state.set_state(SmartRecommendation.waiting_for_features)

    data = await state.get_data()
    selected_features = data.get("selected_features", [])

    keyboard = get_features_selection_keyboard(selected_features)
    await callback.message.edit_text(
        "Что для вас наиболее важно в смартфоне?",
        reply_markup=keyboard
    )
    await callback.answer()


async def show_preview(message: Message, state: FSMContext):
    await state.set_state(SmartRecommendation.showing_preview)

    data = await state.get_data()

    budget = data.get("budget", "Не указан")
    brands = data.get("selected_brands", [])
    brands_text = ", ".join(b.title() for b in brands) if brands else "Любой"

    features = data.get("selected_features", [])
    features_map = {
        "camera": "Камера",
        "battery": "Батарея",
        "screen": "Экран",
        "performance": "Производительность",
        "storage": "Память",
        "gaming": "Игры"
    }
    features_text = ", ".join(
        features_map.get(f, f) for f in features
    ) if features else "Не выбраны"

    additional = data.get("additional_params", "")
    additional_text = additional if additional else "Не указаны"

    preview_text = (
        "<b>Предварительный просмотр:</b>\n\n"
        f"Бюджет: {budget}\n"
        f"Бренды: {brands_text}\n"
        f"Важные характеристики: {features_text}\n"
        f"Дополнительные параметры: {additional_text}"
    )

    keyboard = get_preview_keyboard()
    await message.answer(preview_text, reply_markup=keyboard)


async def show_preview_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.set_state(SmartRecommendation.showing_preview)

    data = await state.get_data()

    budget = data.get("budget", "Не указан")
    brands = data.get("selected_brands", [])
    brands_text = ", ".join(b.title() for b in brands) if brands else "Любой"

    features = data.get("selected_features", [])
    features_map = {
        "camera": "Камера",
        "battery": "Батарея",
        "screen": "Экран",
        "performance": "Производительность",
        "storage": "Память",
        "gaming": "Игры"
    }
    features_text = ", ".join(
        features_map.get(f, f) for f in features
    ) if features else "Не выбраны"

    additional = data.get("additional_params", "")
    additional_text = additional if additional else "Не указаны"

    preview_text = (
        "<b>Предварительный просмотр:</b>\n\n"
        f"Бюджет: {budget}\n"
        f"Бренды: {brands_text}\n"
        f"Важные характеристики: {features_text}\n"
        f"Дополнительные параметры: {additional_text}"
    )

    keyboard = get_preview_keyboard()
    await callback.message.edit_text(preview_text, reply_markup=keyboard)
    await callback.answer()


def get_preview_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Подобрать", callback_data="preview:confirm")
    builder.button(text="Изменить", callback_data="preview:edit")
    builder.button(text="Отменить", callback_data="action:cancel")

    return builder.adjust(1).as_markup()


@router.callback_query(
    SmartRecommendation.showing_preview,
    F.data == "preview:confirm"
)
async def confirm_and_show_result(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} confirmed smart recommendation")

    await state.set_state(SmartRecommendation.showing_results)

    result_text = (
        "<b>Результат:</b>\n\n"
    )

    await callback.message.edit_text(
        result_text,
        reply_markup=get_main_menu()
    )

    await state.clear()

    await callback.answer("Подбор завершен.")


@router.callback_query(
    SmartRecommendation.showing_preview,
    F.data == "preview:edit"
)
async def edit_from_preview(
    callback: CallbackQuery,
    state: FSMContext
):
    logger.info(f"User {callback.from_user.id} edited smart recommendation")

    await state.set_state(SmartRecommendation.waiting_for_additional)

    await callback.message.edit_text(
        "Есть ли предпочтения по дополнительным характеристикам?\n"
        "<i>Например: хочу компактный смартфон, наличие 3.5mm jack</i>\n"
        "Напишите текстом свои пожелания, либо пропустите этот шаг.",
        reply_markup=get_additional_navigation_keyboard()
    )
    await callback.answer()


@router.callback_query(
    F.data == "action:cancel",
    StateFilter(SmartRecommendation)
)
async def cancel_smart_recommendation(
    callback: CallbackQuery,
    state: FSMContext
):
    logger.info(f"User {callback.from_user.id} canceled smart recommendation")

    await state.clear()

    await callback.message.edit_text(
        "Подбор смартфона отменен.",
        reply_markup=get_main_menu()
    )

    await callback.answer("Отменено", show_alert=True)
