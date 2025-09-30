import os
import requests
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# تشغيل البوت في thread منفصل
def run_bot():
    application = Application.builder().token(TOKEN).build()
    
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('مرحباً! أرسل رابط تيكتوك للتحميل.')
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if 'tiktok.com' in text or 'vm.tiktok.com' in text:
            await update.message.reply_text('جاري التحميل...')
            try:
                api_url = "https://www.tikwm.com/api/"
                payload = {"url": text}
                response = requests.post(api_url, data=payload)
                data = response.json()
                
                if data.get('code') == 0:
                    video_url = "https://www.tikwm.com" + data['data']['play']
                    await update.message.reply_video(video=video_url)
                else:
                    await update.message.reply_text('فشل التحميل!')
            except:
                await update.message.reply_text('حدث خطأ!')
        else:
            await update.message.reply_text('أرسل رابط تيكتوك فقط.')
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.run_polling()

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    # تشغيل البوت في thread منفصل
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # تشغيل Flask
    app.run(host='0.0.0.0', port=10000)
