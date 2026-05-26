import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_KEY"]

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
history = {}

SYSTEM = "Ты — персональный помощник по жизни. Помогаешь с личным брендом, юридическими вопросами, финансами, тайм-менеджментом, спортом, учёбой и бытом. Давай конкретные советы. Отвечай на русском языке."

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    if uid not in history:
        history[uid] = []
    history[uid].append({"role": "user", "content": text})
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM,
        messages=history[uid]
    )
    reply = response.content[0].text
    history[uid].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
