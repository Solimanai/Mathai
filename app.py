from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai  # إذا كنت تستخدم ChatGPT من OpenAI
import speech_recognition as sr
from PIL import Image
import io

# ضع توكن البوت الخاص بك هنا
TELEGRAM_TOKEN = "7506802322:AAE3bQvPbXcXsytPe5sm1zurrXEux9NEjJU"
openai.api_key = "Isk-proj-Z3KD6AV3hZVGtjTn2IQ4DBz31jv8MiHC4PsEjwSjWfhpf7XhoJ5XPalltHYYUfDsHUitQwAqtRT3BlbkFJ8zevvjaeyukzc35e1uaOuRmaS1tbgtYDW-6-lChVVaBmZYUG8svXvzrRgPCqmOrtZyi4UdI-AA"  # إذا كنت تستخدم OpenAI

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل لي صورة، سؤال، أو صوت وسأقوم بمساعدتك.")

# معالجة النصوص (الأسئلة)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=50
    )
    answer = response.choices[0].text.strip()
    await update.message.reply_text(answer)

# معالجة الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo = Image.open(io.BytesIO(await photo_file.download_as_bytearray()))
    # هنا يمكنك معالجة الصورة باستخدام مكتبات التعرف على الصور
    await update.message.reply_text("تم استلام الصورة، ولكن لم أقم بعد بإعداد معالجة الصور.")

# معالجة الصوت
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await update.message.voice.get_file()
    audio_data = await voice_file.download_as_bytearray()
    
    # تحويل الصوت إلى نص باستخدام SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_data)) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        await update.message.reply_text(f"تم تحويل الصوت إلى نص: {text}")
    except sr.UnknownValueError:
        await update.message.reply_text("لم أتمكن من فهم الصوت.")
    except sr.RequestError:
        await update.message.reply_text("حدث خطأ في الخدمة الصوتية.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

