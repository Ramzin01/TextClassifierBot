
import os
from telegram import Update
from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from classifier import classify_text





async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Привет! Я бот для классификации текстовых сообщений.\n"
        "Отправь сообщение, и я определю его категорию."
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text
    category = classify_text(text)

    await update.message.reply_text(
        f"Текст: {text}\n"
        f"Категория: {category}"
    )



def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "Не задан токен. Нужно настроить TELEGRAM_BOT_TOKEN."
        )

    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )

    app = (
        Application.builder()
        .token(token)
        .request(request)
        .get_updates_request(
            HTTPXRequest(
                connect_timeout=60,
                read_timeout=60,
                write_timeout=60,
                pool_timeout=60,
            )
        )
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Бот запущен. Для остановки нажми Ctrl+C.")
    app.run_polling()


if __name__ == "__main__":
    main()

