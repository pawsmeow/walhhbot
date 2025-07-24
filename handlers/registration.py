
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import ADMINS
from database import add_user, user_exists
from keyboards.inline import server_keyboard, roles_keyboard, admin_decision_keyboard

router = Router()

class Form(StatesGroup):
    nickname = State()
    game_id = State()
    server = State()
    roles = State()

@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    if await user_exists(message.from_user.id):
        await message.answer("Вы уже проходили регистрацию.")
        return
    await message.answer("Введите ваш никнейм в игре:")
    await state.set_state(Form.nickname)

@router.message(Form.nickname)
async def get_nick(message: Message, state: FSMContext):
    await state.update_data(nick=message.text)
    await message.answer("Введите ваш ID из игры:")
    await state.set_state(Form.game_id)

@router.message(Form.game_id)
async def get_id(message: Message, state: FSMContext):
    await state.update_data(game_id=message.text)
    await message.answer("Выберите сервер:", reply_markup=server_keyboard())
    await state.set_state(Form.server)

@router.callback_query(Form.server)
async def get_server(callback: CallbackQuery, state: FSMContext):
    server = callback.data.split("_")[1]
    await state.update_data(server=server, roles=[])
    await callback.message.edit_text("Выберите роли (от 1 до 5):", reply_markup=roles_keyboard([]))
    await state.set_state(Form.roles)

@router.callback_query(Form.roles, F.data.startswith("role_"))
async def select_roles(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split("_")[1]
    data = await state.get_data()
    roles = data["roles"]
    if role in roles:
        roles.remove(role)
    else:
        if len(roles) < 5:
            roles.append(role)
    await state.update_data(roles=roles)
    await callback.message.edit_reply_markup(reply_markup=roles_keyboard(roles))

@router.callback_query(Form.roles, F.data == "roles_done")
async def done_roles(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if len(data["roles"]) < 1:
        await callback.answer("Выберите хотя бы одну роль", show_alert=True)
        return
    await add_user(
        callback.from_user.id,
        callback.from_user.username,
        data["nick"],
        data["game_id"],
        data["server"],
        data["roles"]
    )
    msg = (
        f"📝 Новая анкета:"
        f"👤 @{callback.from_user.username}"
        f"🎮 Ник: {data['nick']}"
        f"🆔 ID: {data['game_id']}"
        f"🌍 Сервер: {data['server']}"
        f"🛡️ Роли: {', '.join(data['roles'])}"
        f"🔗 [Профиль](tg://user?id={callback.from_user.id})"
    )
    for admin_id in ADMINS:
        await callback.bot.send_message(admin_id, msg, reply_markup=admin_decision_keyboard(callback.from_user.id), parse_mode="Markdown")
    await callback.message.edit_text("Ваша анкета отправлена на проверку администратору.")
    await state.clear()
