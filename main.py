import discord
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. إعداد خادم Flask صغير لضمان بقاء السيرفر يعمل على Render
app = Flask('')

@app.route('/')
def home():
    return "Your service is live 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعداد مفتاح ذكاء Gemini الاصطناعي
# تهيئة Gemini مع استخدام بروكسي لتخطي حظر خوادم Render
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    client_options={"api_endpoint": "https://generativelanguage.googleapis.com"}
)

model = genai.GenerativeModel("gemini-1.5-flash")


# 3. إعداد صلاحيات البوت للديسكورد
intents = discord.Intents.default()
intents.message_content = True  # قراءة محتوى الرسائل عادية

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تسجيل الدخول بنجاح باسم: {client.user}')

@client.event
async def on_message(message):
    # منع البوت من الرد على الرسائل الخاصة به
    if message.author == client.user:
        return

    try:
        # إرسال إشعار للمستخدم بأن البوت يقوم بالكتابة حالياً
        async with message.channel.typing():
            # إرسال نص رسالتك إلى ذكاء Gemini الاصطناعي لجلب الرد
            response = model.generate_content(message.content)
            
            # إرسال رد الذكاء الاصطناعي إلى روم الديسكورد
            await message.reply(response.text)
    except Exception as e:
        print(f"حدث خطأ أثناء معالجة الذكاء الاصطناعي: {e}")
        await message.reply("عذراً، واجهت مشكلة في الاتصال بالعقل المفكر لـ Gemini حالياً.")


# تشغيل خادم البقاء قيد الحياة لـ Render
keep_alive()

# تشغيل البوت باستخدام توكن ديسكورد المخزن بأمان
client.run(os.getenv('DISCORD_TOKEN'))
