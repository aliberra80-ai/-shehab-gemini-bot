import os
import discord
from discord.ext import commands
from google import genai

# استدعاء الرموز السرية بأمان من إعدادات الاستضافة المجانية
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# إعداد ذكاء Gemini الاصطناعي
ai_client = genai.Client(api_key=GEMINI_KEY)

# إعداد بوت ديسكورد
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user.name}')

# أمر برميجي للرد بالذكاء الاصطناعي
@bot.command(name="اسأل")
async def ask_gemini(ctx, *, question: str):
    async with ctx.typing():
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=question,
            )
            # ديسكورد يمنع الرسائل الأطول من 2000 حرف
            await ctx.send(response.text[:2000])
        except Exception as e:
            await ctx.send(f"حدث خطأ أثناء الاتصال بـ Gemini: {e}")

# تشغيل البوت
bot.run(DISCORD_TOKEN)
