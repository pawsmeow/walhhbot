
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ALL_SERVERS = ["RU", "KZ", "KRG", "UZB"]
ALL_ROLES = ["Мид", "Голд", "Лес", "Эксп", "Роум"]

def server_keyboard(selected=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=f"{'✅ ' if selected == s else ''}{s}",
                callback_data=f"server_{s}"
            ) for s in ALL_SERVERS
        ]]
    )

def roles_keyboard(selected_roles):
    buttons = []
    for i in range(0, len(ALL_ROLES), 2):
        row = []
        for role in ALL_ROLES[i:i+2]:
            prefix = "✅ " if role in selected_roles else ""
            row.append(InlineKeyboardButton(text=prefix + role, callback_data=f"role_{role}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="✅ Готово", callback_data="roles_done")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_remove"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_remove")
    ]])

def admin_decision_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_{user_id}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}")
    ]])
