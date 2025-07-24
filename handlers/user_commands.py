
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database import get_user, delete_user
from keyboards.inline import confirm_keyboard

router = Router()

@router.message(F.text == "/profile")
async def profile(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        _, _, _, nick, gid, server, roles, status = user
        await message.answer(f"👤 Ник: {nick}\n🆔 ID: {gid}\n🌍 Сервер: {server}\n🛡️ Роли: {roles}\n📄 Статус: {status}")
    else:
        await message.answer("Вы не зарегистрированы.")

@router.message(F.text == "/remove")
async def remove_prompt(message: Message):
    await message.answer("Вы уверены, что хотите удалить анкету?", reply_markup=confirm_keyboard())

@router.callback_query(F.data == "confirm_remove")
async def remove_confirm(callback: CallbackQuery):
    await delete_user(callback.from_user.id)
    await callback.message.edit_text("Ваша анкета удалена.")

@router.callback_query(F.data == "cancel_remove")
async def remove_cancel(callback: CallbackQuery):
    await callback.message.edit_text("Удаление отменено.")

@router.message(F.text == "/rules")
async def rules(message: Message):
    await message.answer("📏 Правила поведения участников Valhalla Gaming\n\n🚫 Запрещено: ...")

@router.message(F.text == "/reglament")
async def reglament(message: Message):
    await message.answer("📜 Регламент участия в матчах Valhalla Gaming\n\n❓ Что такое Valhalla Gaming? ...")
