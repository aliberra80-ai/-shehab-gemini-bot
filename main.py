import discord
import os
import requests
import json
from flask import Flask
from threading import Thread

# 1. إعداد خادم Flask لضمان بقاء السيرفر يعمل على Render
app = Flask('')

@app.route('/')
def home():
    return "Your Bot is Ready and Live! 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعداد صلاحيات البوت للديسكورد
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')

@client.event
async def on_message(message):
    # تجنب رد البوت على نفسه
    if message.author == client.user:
        return

    # إرسال النص مباشرة إلى واجهة جوجل عبر طلب HTTP رسمي يتخطى القيود
        try:
        async with message.channel.typing():
                        api_key = os.getenv("GEMINI_API_KEY")
            url = f"https://googleapis.com{api_key}"
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": message.content}]}]
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = response.json()
            
            # طريقة استخراج النص الصحيحة من استجابة جوجل لـ Gemini 1.5 Flash
            bot_reply = response_data['candidates'][0]['content']['parts'][0]['text']
            
            await message.reply(bot_reply)


            
    except Exception as e:
        print(f"Error: {e}")
        await message.reply("عذراً، واجهت مشكلة في الاتصال بالذكاء الاصطناعي حالياً.")

# تشغيل البوت قيد الحياة لـ Render
keep_alive()

# تشغيل البوت باستخدام التوكن الموثق
client.run(os.getenv('DISCORD_TOKEN'))
