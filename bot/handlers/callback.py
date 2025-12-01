import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    get_main_menu,
    get_smartphone_menu,
    get_back_button,
    get_reccomend_menu,
    get_settings_menu
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
        reply_markup=get_reccomend_menu()
    )

    await callback.answer()


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

    await callback.answer("Not available", show_alert=True)


@router.callback_query(F.data == "smartphone:popular")
async def callback_popular(callback: CallbackQuery):
    await callback.message.edit_text(
        "Популярные модели...",
        reply_markup=get_back_button()
    )

    await callback.answer("Not available", show_alert=True)


@router.callback_query(F.data == "recommend:smart")
async def callback_smart_recommend(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Умный подбор с помощью ChatGPT</b>\n\n"
        "Я задам вам несколько вопросов и подберу"
        "смартфон для вас.",
        reply_markup=get_back_button()
    )

    await callback.answer()


@router.callback_query(F.data == "recommend:manual")
async def callback_manual_recommend(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Подбор по параметрам</b>\n\n"
        "Укажите жалаемые параметры:\n"
        "1. Бюджет\n"
        "2. Бренд\n"
        "3. Характеристики\n",
        reply_markup=get_back_button()
    )

    await callback.answer()


@router.callback_query(F.data == "recommend:popular")
async def callback_popular_recommend(callback: CallbackQuery):
    await callback.message.edit_text(
        "Популярные модели...",
        reply_markup=get_back_button()
    )

    await callback.answer()


@router.callback_query(F.data == "settings:main")
async def callback_settings_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Настройки:</b>\n\n"
        "Выберите действие:",
        reply_markup=get_settings_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "settings:language")
async def callback_settings_language(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Язык интерфейса</b>\n\n"
        "Выберите язык:\n"
        "• Русский\n"
        "• English",
        reply_markup=get_back_button("settings:main", "Назад к настройкам")
    )

    await callback.answer()


@router.callback_query(F.data == "settings:clear_history")
async def callback_settings_clear_history(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>История очищена</b>\n\n"
        "Ваши предыдущие диалоги были удалены.",
        reply_markup=get_back_button("settings:main", "Назад к настройкам")
    )

    await callback.answer("История очищена", show_alert=True)
