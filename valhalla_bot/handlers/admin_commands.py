from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import ADMINS
from database import get_user
import aiosqlite
from database import DB_NAME

router = Router()

ALL_SERVERS = ["RU", "KZ", "KRG", "UZB"]
ALL_ROLES = ["Мид", "Голд", "Лес", "Эксп", "Роум"]

class FilterState(StatesGroup):
    choosing = State()

def filter_keyboard(selected_server=None, selected_roles=None):
    selected_roles = selected_roles or []
    kb = []

    # Серверы
    kb.append([
        InlineKeyboardButton(
            text=("✅ " if selected_server == srv else "") + srv,
            callback_data=f"filter_server_{srv}"
        ) for srv in ALL_SERVERS
    ])

    # Роли по 2 в ряд
    for i in range(0, len(ALL_ROLES), 2):
        row = []
        for role in ALL_ROLES[i:i+2]:
            prefix = "✅ " if role in selected_roles else ""
            row.append(InlineKeyboardButton(text=prefix + role, callback_data=f"filter_role_{role}"))
        kb.append(row)

    # Показать
    kb.append([InlineKeyboardButton(text="📋 Показать", callback_data="filter_show")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "/users")
async def filter_users_start(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    await state.set_state(FilterState.choosing)
    await state.update_data(server=None, roles=[])
    await message.answer("Выберите фильтры для списка пользователей:", reply_markup=filter_keyboard())

@router.callback_query(FilterState.choosing, F.data.startswith("filter_server_"))
async def choose_server(callback: CallbackQuery, state: FSMContext):
    server = callback.data.split("_")[2]
    data = await state.get_data()
    await state.update_data(server=server)
    await callback.message.edit_reply_markup(reply_markup=filter_keyboard(server, data.get("roles", [])))

@router.callback_query(FilterState.choosing, F.data.startswith("filter_role_"))
async def toggle_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split("_")[2]
    data = await state.get_data()
    roles = data.get("roles", [])
    if role in roles:
        roles.remove(role)
    else:
        if len(roles) < 5:
            roles.append(role)
    await state.update_data(roles=roles)
    await callback.message.edit_reply_markup(reply_markup=filter_keyboard(data.get("server"), roles))

@router.callback_query(FilterState.choosing, F.data == "filter_show")
async def show_filtered_users(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server_filter = data.get("server")
    roles_filter = data.get("roles", [])

    query = "SELECT username, game_nick, server, roles FROM users"
    params = []
    conditions = []

    if server_filter:
        conditions.append("server = ?")
        params.append(server_filter)

    if roles_filter:
        for role in roles_filter:
            conditions.append("roles LIKE ?")
            params.append(f"%{role}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(query, params)
        users = await cursor.fetchall()

    if not users:
        await callback.message.edit_text("🙅‍♂️ Пользователи не найдены по фильтру.")
    else:
        text = "📋 <b>Пользователи:</b>\n\n"
        for u in users:
            username, nick, server, roles = u
            text += f"👤 @{username or '—'}\n🎮 {nick}\n🌍 {server} | 🛡 {roles}\n\n"
        await callback.message.edit_text(text, parse_mode="HTML")

    await state.clear()
