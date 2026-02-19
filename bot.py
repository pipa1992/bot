import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь текст, и я сгенерирую изображение 🎨")


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("Генерирую... ⏳")

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        with open("image.png", "wb") as f:
            f.write(response.content)

        await update.message.reply_photo(photo=open("image.png", "rb"))
    else:
        await update.message.reply_text("Ошибка генерации 😢 Попробуй позже.")


app = ApplicationBuilder().token(8272487181:AAF4tThM_B5GByYycDSwgc-RWmFi2S7wUEg).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

app.run_polling()

