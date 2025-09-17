
import discord
from discord.ext import commands
from flask import Flask
import threading

# -------- keep_alive --------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
# ----------------------------

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready! Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="✨〢𝐖𝐞𝐥𝐜𝐨𝐦𝐞")
    if channel:
        await channel.send(f"أهلاً وسهلاً بك يا {member.mention} 💖")

# ---- شغل keep_alive ثم البوت ----
keep_alive()
bot.run("توكن_البوت_هنا")
