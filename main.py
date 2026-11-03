import os
import discord
from discord.ext import commands
from google import genai
from flask import Flask
import threading

# تشغيل خادم ويب وهمي لحل مشكلة Port في منصة Render المجانية
app = Flask('')
@app.route('/')
def home(): 
    return "البوت يعمل بنجاح ومستقر 24 ساعة!"

def run(): 
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run).start()

# استدعاء الرموز السرية بأمان
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

ai_client = genai.Client(api_key=GEMINI_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user.name}')

@bot.command(name="اسأل")
async def ask_gemini(ctx, *, question: str):
    async with ctx.typing():
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=question,
            )
            await ctx.send(response.text[:2000])
        except Exception as e:
            await ctx.send(f"حدث خطأ أثناء الاتصال بـ Gemini: {e}")

bot.run(DISCORD_TOKEN)
