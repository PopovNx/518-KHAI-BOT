from logging import exception
from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models.day import Days
from datetime import datetime
from service import format_rosp, get_now
router = Router()


def get_keyboard(selected_day=None):
    days = Days.objects()
    buttons = []
    for day in days:
        text = day.name
        if day.num == selected_day:
            text = f'✅ {text}'
        if day.num == get_now()[0]:
            text = f'{text} 🔥'
        buttons.append([InlineKeyboardButton(
            text=text, callback_data=f"day:{day.num}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.message(commands=['getweek'])
async def command_message(message: Message):
    await message.answer("Выберите день недели", reply_markup=get_keyboard())


@router.callback_query(lambda callback_query: callback_query.data.startswith('day:'))
async def set_day(callback: CallbackQuery):
    nm = int(callback.data.split(':')[1])
    day = Days.objects(num=nm).first()
    try:
        await callback.message.edit_text(format_rosp(day.num), reply_markup=get_keyboard(day.num), parse_mode='HTML')
    except exception:
        pass
         
    await callback.answer()
