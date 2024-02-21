import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.config.conf import settings
from bot.general.base import (
    ACTION,
    CHECK_SUB,
    GEO,
    NICKNAME,
    PARTICIPATE,
    REWARD,
    SOURCE,
    VOLUME,
    cancel,
    check_subscription,
    choose_action,
    participation,
    set_geo,
    set_nickname,
    set_reward,
    set_source,
    set_volume,
    start,
)

logging.basicConfig(
    format="%(levelname)s | %(name)s | %(asctime)s | %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)


def main() -> None:
    app = ApplicationBuilder().token(settings.TG_API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_action)],
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_nickname)],
            GEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_geo)],
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_source)],
            VOLUME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_volume)],
            PARTICIPATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, participation)
            ],
            CHECK_SUB: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_subscription)
            ],
            REWARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_reward)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
