import json, logging
from telegram import Update, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, PreCheckoutQueryHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode

TOKEN = "8648458601:AAE-Rb0Y0ZAWuKJt3MZFwBzq0S9STRMBDSE"
MINI_APP_URL = "https://personawoodoo.github.io/WILLD-GIFT/index.html"
CHANNEL_LINK = "https://t.me/VILLD_GIFT"
START_PHOTO = "https://i.supaimg.com/435c46f7-76b1-41ba-82e2-1f1a0a964f2c/494659da-9570-4253-8576-31ccbe9a3905.jpg"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "🎁 <b>VILLD GIFT</b>\n\n"
        "<b>БЕСПЛАТНОЕ ОТКРЫТИЕ</b>\n<b>КАЖДЫЕ 24 ЧАСА!</b>\n\n"
        f"<b>📢 Канал:</b> {CHANNEL_LINK}"
    )
    kb = [[InlineKeyboardButton("🎰 ИГРАТЬ", web_app={"url": MINI_APP_URL})],
          [InlineKeyboardButton("📢 Канал", url=CHANNEL_LINK),
           InlineKeyboardButton("👥 Пригласить", switch_inline_query="ref")]]
    try:
        await update.message.reply_photo(START_PHOTO, caption=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)
    except:
        await update.message.reply_text(caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.HTML)

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.effective_message.web_app_data.data)
    except:
        return
    if data.get("action") == "buy_stars":
        amount = data["amount"]
        await context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=f"Пополнение {amount} ⭐",
            description=f"Покупка {amount} звёзд для VILLD GIFT",
            payload=f"stars_{amount}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(f"{amount} ⭐", amount * 100)],
            start_parameter="buy_stars"
        )
        await update.effective_message.reply_text("Счёт отправлен. Нажмите кнопку для оплаты.")
    else:
        await update.effective_message.reply_text("Данные получены, но действие не распознано.")

async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Оплата прошла! Ваш баланс пополнен. Зайдите в мини‑приложение.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.run_polling()

if __name__ == "__main__":
    main()
