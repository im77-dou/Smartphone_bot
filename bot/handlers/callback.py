import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    get_main_menu,
    get_smartphone_menu,
    get_back_button
)


logger = logging.getLogger(__name__)

router = Router(name="callback")


@router.callback_query(F.data == "menu:main")
async def callback_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Главное меню:</b>\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "menu:recommend")
async def callback_recommend(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Подбор смартфона</b>\n\n"
        "Выберите действие:",
        reply_markup=get_smartphone_menu()
    )

    await callback.answer("Not available", show_alert=True)


@router.callback_query(F.data == "menu:compare")
async def callback_compare(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Сравнение смартфонов</b>\n\n"
        "Выберите",
        reply_markup=get_back_button()
    )

    await callback.answer()


@router.callback_query(F.data == "menu:help")
async def callback_help(callback: CallbackQuery):
    await callback.message.edit_text(
        "Используйте меню для навигации по боту.\n\n",
        "Кнопка <Назад> вернет в главное меню.",
        reply_markup=get_back_button()
    )

    await callback.answer()


@router.callback_query(F.data == "smartphone:start_recommend")
async def callback_start_recommend(callback: CallbackQuery):
    await callback.message.edit_text(
        "Подбор смартфона...",
        reply_markup=get_back_button()
    )

    await callback.answer("Not available")


@router.callback_query(F.data == "smartphone:popular")
async def callback_popular(callback: CallbackQuery):
    await callback.message.edit_text(
        "Популярные модели...",
        reply_markup=get_back_button()
    )

    await callback.answer("Not available")
