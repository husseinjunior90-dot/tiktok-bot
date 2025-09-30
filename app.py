import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# التوكن من متغيرات البيئة
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# تطبيق Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# وظيفة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً! أرسل لي رابط فيديو تيكتوك وسأحاول تحميله لك.'
    )

# معالجة رسائل النص
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if 'tiktok.com' in text or 'vm.tiktok.com' in text:
        await update.message.reply_text('جاري معالجة الفيديو...')
        
        try:
            video_url = await download_tiktok_video(text)
            
            if video_url:
                await update.message.reply_video(video=video_url)
            else:
                await update.message.reply_text('عذراً، لم أتمكن من تحميل الفيديو.')
                
        except Exception as e:
            logging.error(f"Error: {e}")
            await update.message.reply_text('حدث خطأ أثناء معالجة الفيديو.')
    else:
        await update.message.reply_text('يرجى إرسال رابط تيكتوك صالح.')

async def download_tiktok_video(url):
    try:
        api_url = "https://www.tikwm.com/api/"
        payload = {"url": url}
        
        response = requests.post(api_url, data=payload)
        data = response.json()
        
        if data.get('code') == 0:
            video_url = "https://www.tikwm.com" + data['data']['play']
            return video_url
        return None
            
    except Exception as e:
        logging.error(f"Download error: {e}")
        return None

# تشغيل البوت
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
