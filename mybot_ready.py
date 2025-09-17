import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # عشان يتابع الأعضاء الجدد

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول باسم: {bot.user}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="✨〢𝐖𝐞𝐥𝐜𝐨𝐦𝐞")  # غير اسم الروم إذا تبينه
    if channel:
        embed = discord.Embed(
            title="👑 WELCOME TO 7F 👑",
            description=(
                f" {member.mention}\n\n"
                "https://canary.discord.com/channels/1394091822661373972/1415074648478978169\n"
                "🎉 **استمتع مع الشباب**\n"
            ),
            color=0xffcc00
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_image(url="https://i.ibb.co/cXNF0Kwg/2025-09-13-134516.png")
        embed.set_footer(text="7F Server")
        await channel.send(embed=embed)

# حطي التوكن بين علامتي التنصيص هنا
bot.run("MTQxNjg1MDk4OTg2NDE5MDAzNQ.Gk7tz4.gaMAsQY0xwBLOA4MKzYO6gL-OGLXJlMwaGlhd4")
