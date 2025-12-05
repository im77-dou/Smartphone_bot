import logging
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import SmartphoneComparison
from bot.keyboards.inline import get_main_menu, get_cancel_keyboard

logger = logging.getLogger(__name__)
router = Router(name="comparison")


@router.message(Command("compare"))
async def start_comparison(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started comparison.")

    await state.clear()

    await state.set_state(SmartphoneComparison.waiting_for_first_model)

    await message.answer(
        "<b>Сравнение смартфонов:</b>\n\n"
        "Введите название первого смартфона:",
        reply_markup=get_cancel_keyboard()
    )


@router.callback_query(F.data == "menu:compare")
async def callback_start_comparison(
    callback: CallbackQuery,
    state: FSMContext
):
    logger.info(f"User {callback.from_user.id} started comparison.")

    await state.clear()

    await state.set_state(SmartphoneComparison.waiting_for_first_model)

    await callback.message.edit_text(
        "<b>Сравнение смартфонов:</b>\n\n"
        "Введите название первого смартфона:",
        reply_markup=get_cancel_keyboard()
    )

    await callback.answer()


@router.message(SmartphoneComparison.waiting_for_first_model)
async def process_first_model(message: Message, state: FSMContext):
    model_name = message.text.strip()

    if len(model_name) < 2:
        await message.answer(
            "Название слишком короткое.\n\n"
            "Введите название первого смартфона:",
            reply_markup=get_cancel_keyboard()
        )
        return
    if len(model_name) > 50:
        await message.answer(
            "Название слишком длинное.\n\n"
            "Введите название первого смартфона:",
            reply_markup=get_cancel_keyboard()
        )
        return

    await state.update_data(first_model=model_name)
    logger.info(f"User {message.from_user.id} set first model: {model_name}.")

    await state.set_state(SmartphoneComparison.waiting_for_second_model)

    await message.answer(
        "Введите название второго смартфона:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(SmartphoneComparison.waiting_for_second_model)
async def process_second_model(message: Message, state: FSMContext):
    model_name = message.text.strip()

    if len(model_name) < 2:
        await message.answer(
            "Название слишком короткое.\n\n"
            "Введите название второго смартфона:",
            reply_markup=get_cancel_keyboard()
        )
        return
    if len(model_name) > 50:
        await message.answer(
            "Название слишком длинное.\n\n"
            "Введите название второго смартфона:",
            reply_markup=get_cancel_keyboard()
        )
        return

    data = await state.get_data()
    first_model = data.get("first_model", "")

    if model_name.lower() == first_model.lower():
        await message.answer(
            "Вы выбрали один и тот же смартфон.\n\n"
            "Введите название второго смартфона:",
            reply_markup=get_cancel_keyboard()
        )
        return

    await state.update_data(second_model=model_name)
    logger.info(f"User {message.from_user.id} set second model: {model_name}.")

    result_text = (
        "<b>Сравнение смартфонов:</b>\n\n"
        f"<b>Первый смартфон:</b> {first_model}\n"
        f"<b>Второй смартфон:</b> {model_name}"
    )

    await message.answer(
        result_text,
        reply_markup=get_main_menu()
    )

    await state.clear()


@router.callback_query(
    F.data == "action:cancel",
    StateFilter(SmartphoneComparison)
)
async def cancel_comparison_callback(
    callback: CallbackQuery,
    state: FSMContext
):
    logger.info(f"User {callback.from_user.id} cancelled comparison.")
    await state.clear()

    await callback.message.edit_text(
        "Сравнение смартфонов отменено.\n\n"
        "Чтобы начать заново, используйте команду /compare",
        reply_markup=get_main_menu()
    )

    await callback.answer("Сравнение смартфонов отменено.", show_alert=True)


@router.message(
    Command("cancel"),
    StateFilter(SmartphoneComparison)
)
async def cancel_comparison_command(
    message: Message,
    state: FSMContext
):
    logger.info(f"User {message.from_user.id} cancelled comparison.")
    await state.clear()

    await message.answer(
        "Сравнение смартфонов отменено.\n\n"
        "Чтобы начать заново, используйте команду /compare",
        reply_markup=get_main_menu()
    )
