import certifi
from pymongo.mongo_client import MongoClient
from telegram import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.error import TelegramError
from telegram.ext import ContextTypes, ConversationHandler

from bot.config.conf import settings
from bot.general.keyboards import (
    choose_action_keyboard1,
    choose_action_keyboard1_ru,
    choose_action_keyboard2,
    choose_action_keyboard2_ru,
    language_keyboard,
    participation_keyboard,
    participation_keyboard_ru,
    set_geo_keyboard,
    set_geo_keyboard_ru,
    set_reward_keyboard,
    set_reward_keyboard_ru,
)

# match context.user_data["localization"]:
#         case "Русский":
#             text = ""
#         case "English":
#             text = ""


ACTION, NICKNAME, GEO, SOURCE, VOLUME, PARTICIPATE, CHECK_SUB, REWARD = range(8)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    client = MongoClient(settings.MONGODB_CLIENT_URL, tlsCAFile=certifi.where())
    db = client["empirepartnersbot"]
    winners = db["winners"]
    if winners.find_one({"user_id": update.effective_user.id}):
        await update.message.reply_text(
            "Вы уже получали мерч, его можно получить лишь единожды.\n\n"
            "You already won your merch."
        )
        return ConversationHandler.END

    reply_markup = ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Выберите язык/Choose your language",
        reply_markup=reply_markup,
    )
    return ACTION


async def choose_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["localization"] = update.message.text
    print(f"Language: {context.user_data['localization']}")

    match context.user_data["localization"]:
        case "Русский":
            text1 = "Привет!\nЧтобы получить стильный мерч от Empire Partners, нужно выполнить два действия:\n1. Подписаться на наш канал"
            text2 = "2. Заполнить анкету"
            keyboard1 = choose_action_keyboard1_ru
            keyboard2 = choose_action_keyboard2_ru
        case "English":
            text1 = "If you want to get stylish merch from Empire Partners you need to do two simple steps:\n1. Fill out the form"
            text2 = "Follow our channel"
            keyboard1 = choose_action_keyboard1
            keyboard2 = choose_action_keyboard2

    reply_markup = InlineKeyboardMarkup(keyboard1)
    await update.message.reply_text(
        text1,
        reply_markup=reply_markup,
    )
    reply_markup = ReplyKeyboardMarkup(keyboard2)
    await update.message.reply_text(
        text2,
        reply_markup=reply_markup,
    )
    return NICKNAME


async def set_nickname(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваш логин в Telegram"
        case "English":
            text = "Provide your Telegram login"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return GEO


async def set_geo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["nickname"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваше ГЕО"
            reply_markup = ReplyKeyboardMarkup(set_geo_keyboard_ru)
        case "English":
            text = "Specify your GEO"
            reply_markup = ReplyKeyboardMarkup(set_geo_keyboard)

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return SOURCE


async def set_source(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["geo"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваш источник трафика"
        case "English":
            text = "Specify your traffic source"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return VOLUME


async def set_volume(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["source"] = update.message.text

    match context.user_data["localization"]:
        case "Русский":
            text = "Укажите Ваш объем трафика в месяц"
        case "English":
            text = "Specify you traffic volume per month"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return PARTICIPATE


async def participation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    context.user_data["volume"] = update.message.text
    match context.user_data["localization"]:
        case "Русский":
            text = "Вы хотите принять участие в RS Affiliate Tournament - арбитражном турнире с призовым фондом $300 000?"
            keyboard = participation_keyboard_ru
        case "English":
            text = "Do you want to take part in the RS Affiliate Tournament - an arbitrage tournament with a prize pool of $300,000?"
            keyboard = participation_keyboard

    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return CHECK_SUB


async def check_subscription(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    match context.user_data["localization"]:
        case "Русский":
            check_text = "Проверяем Вашу подписку на канал..."
            success_text = (
                "Готово, мерч ваш!\nВыберите свой крутой мерч для получения: "
            )
            fail_text = "Вам осталось совсем немного для получения мерча от Empire Partners!\nПодпишитесь на канал https://t.me/empire_partners\nПосле этого напишите Готово"
            set_reward_keyboard_localizated = set_reward_keyboard_ru
        case "English":
            check_text = "We are checking your subscription to the channel..."
            success_text = (
                "All done! The merch is yours now!\nChoose your cool merch to receive:"
            )
            fail_text = "You have almost received your merch from Empire Partners! Follow our channel https://t.me/empire_partners\nAfter that type Done"
            set_reward_keyboard_localizated = set_reward_keyboard

    if update.message.text.lower() not in ["готово", "done"]:
        context.user_data["participation"] = update.message.text

    # Check for rewards availability
    client = MongoClient(settings.MONGODB_CLIENT_URL, tlsCAFile=certifi.where())
    db = client["empirepartnersbot"]
    rewards = db["rewards"]
    for reward in rewards.find():
        if reward["amount"] <= 0:
            match reward["name"]:
                case "шоппер":
                    set_reward_keyboard_localizated[0] = (
                        set_reward_keyboard_localizated[0][1:]
                    )
                case "брелок":
                    set_reward_keyboard_localizated[0] = (
                        set_reward_keyboard_localizated[0][:1]
                        + set_reward_keyboard_localizated[0][2:]
                    )
                case "кардхолдер":
                    set_reward_keyboard_localizated[0] = (
                        set_reward_keyboard_localizated[0][:-1]
                    )
    if not set_reward_keyboard_localizated[0]:
        return REWARD

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        check_text,
        reply_markup=reply_markup,
    )

    chat_member = await context.bot.get_chat_member(
        chat_id=settings.CHANNEL_NAME, user_id=update.effective_user.id
    )
    if chat_member.status in ["member", "administartor", "creator"]:
        success_reply_markup = ReplyKeyboardMarkup(set_reward_keyboard_localizated)
        await update.message.reply_text(
            success_text,
            reply_markup=success_reply_markup,
        )
        return REWARD
    else:
        reply_markup = ReplyKeyboardRemove()
        await update.message.reply_text(
            fail_text,
            reply_markup=reply_markup,
        )
        return CHECK_SUB


async def set_reward(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> ConversationHandler.END:
    context.user_data["reward"] = update.message.text

    winner = {
        "user_id": update.effective_user.id,
        "langauge": context.user_data["localization"],
        "nickname": context.user_data["nickname"],
        "geo": context.user_data["geo"],
        "source": context.user_data["source"],
        "volume": context.user_data["volume"],
        "reward": context.user_data["reward"],
    }
    winner["reward"] = winner["reward"].lower()

    match winner["reward"]:
        case "shopper":
            winner["reward"] = "шоппер"
        case "keychain":
            winner["reward"] = "брелок"
        case "phone cardholder":
            winner["reward"] = "кардхолдер"

    client = MongoClient(settings.MONGODB_CLIENT_URL, tlsCAFile=certifi.where())
    db = client["empirepartnersbot"]
    winners = db["winners"]
    winners.insert_one(winner)
    rewards = db["rewards"]
    reward = rewards.find_one({"name": winner["reward"]})
    rewards.update_one(reward, {"$set": {"amount": reward["amount"] - 1}})

    match context.user_data["localization"]:
        case "Русский":
            text = (
                "Выбор сделан!) Забери свой мерч на стенде 104В!\nСпасибо за участие!"
            )
        case "English":
            text = "The choice is made! Pick up your merch at stand 104B!\nThanks for taking part!"

    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> ConversationHandler.END:
    print("cancel")
    return ConversationHandler.END
