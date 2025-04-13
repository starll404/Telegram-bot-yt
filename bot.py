import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from pytube import YouTube

TOKEN = "7926865868:AAEcmatickD8F8r2gKQvhy6bZtej4P6uQDc"  

async def start(update: Update, context):
    await update.message.reply_text(
        "📹 Привет! Я бот для скачивания видео с YouTube.\n"
        "Просто отправь мне ссылку на видео, и я пришлю его тебе!\n"
        "Для аудио используй /audio [ссылка]"
    )

async def download_video(update: Update, context):
    url = update.message.text
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video_path = video.download(filename="video.mp4")
        
        await update.message.reply_video(video=open(video_path, "rb"))
        os.remove(video_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def download_audio(update: Update, context):
    try:
        url = update.message.text.split()[1]  
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        audio_path = audio.download(filename="audio.mp3")
        
        await update.message.reply_audio(audio=open(audio_path, "rb"))
        os.remove(audio_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем все обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("audio", download_audio))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    app.run_polling()

if __name__ == "__main__":
    main()