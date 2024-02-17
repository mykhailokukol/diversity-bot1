from telegram import InlineKeyboardButton

language_keyboard = [
    [
        InlineKeyboardButton("Русский", callback_data="ru"),
        InlineKeyboardButton("English", callback_data="en"),
    ]
]

choose_action_keyboard1_ru = [
    [
        InlineKeyboardButton(
            "Подписаться на канал",
            url="https://t.me/empire_partners",
        )
    ],
]
choose_action_keyboard2_ru = [[InlineKeyboardButton("Заполнить анкету")]]

set_geo_keyboard_ru = [
    [
        InlineKeyboardButton("Индия"),
        InlineKeyboardButton("Бангладеш"),
        InlineKeyboardButton("Турция"),
    ],
    [
        InlineKeyboardButton("Канада"),
        InlineKeyboardButton("Узбекистан"),
        InlineKeyboardButton("Казахстан"),
    ],
]
set_reward_keyboard_ru = [
    [
        InlineKeyboardButton("Шоппер"),
        InlineKeyboardButton("Брелок"),
        InlineKeyboardButton("Кардхолдер"),
    ]
]

# ========================================= ENGLISH ===================================

choose_action_keyboard1 = [
    [
        InlineKeyboardButton(
            "Follow our channel",
            url="https://t.me/empire_partners",
        )
    ],
]
choose_action_keyboard2 = [[InlineKeyboardButton("Fill out the form")]]

set_geo_keyboard = [
    [
        InlineKeyboardButton("India"),
        InlineKeyboardButton("Bangladesh"),
        InlineKeyboardButton("Türkiye"),
    ],
    [
        InlineKeyboardButton("Canada"),
        InlineKeyboardButton("Uzbekistan"),
        InlineKeyboardButton("Kazakhstan"),
    ],
]
set_reward_keyboard = [
    [
        InlineKeyboardButton("Shopper"),
        InlineKeyboardButton("Keychain"),
        InlineKeyboardButton("Phone Cardholder"),
    ]
]
