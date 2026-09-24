import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image
import easyocr
from io import BytesIO
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
reader = easyocr.Reader(['en', 'ru'])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Сейчас распознаю текст...")
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        image = Image.open(BytesIO(photo_bytes))
        
        results = reader.readtext(image, detail=0)
        text = "\n".join(results)
        
        if text.strip():
            await update.message.reply_text(f"📝 Текст:\n\n{text}")
        else:
            await update.message.reply_text("❌ Текст не найден")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет!\n📸 Отправь мне фото с текстом!")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.COMMAND, start))
    
    print("✅ Бот запущен!")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
