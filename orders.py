import discord
from discord.ext import commands
import os
import sys

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="#", intents=intents, help_command=None)

# =============================
# رومات اللوج لكل حدث/أمر
# =============================
log_channels = {
    "join_leave": "join-leave-log",     # دخول/خروج الأعضاء
    "message": "message-log",           # تعديل/حذف الرسائل
    "mod": "mod-log",                   # طرد/حظر/فك حظر/ميوت
    "admin": "admin-log",               # قفل/فتح الشات، إعطاء/سحب رتب
    "clear": "clear-log"                # مسح الرسائل
}

# =============================
# عند تشغيل البوت
# =============================
@bot.event
async def on_ready():
    print(f"✅ تم تشغيل البوت: {bot.user}")
    guild = bot.guilds[0]
    for key, name in log_channels.items():
        if not discord.utils.get(guild.text_channels, name=name):
            await guild.create_text_channel(name)
            print(f"✅ تم إنشاء روم: {name}")

# =============================
# لوجات الأحداث
# =============================
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=log_channels["join_leave"])
    if channel:
        embed = discord.Embed(title="📥 عضو جديد",
                              description=f"دخل {member.mention} السيرفر 🎉",
                              color=0x2ecc71)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name=log_channels["join_leave"])
    if channel:
        embed = discord.Embed(title="📤 خروج عضو",
                              description=f"خرج {member.mention} من السيرفر.",
                              color=0xe74c3c)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    channel = discord.utils.get(message.guild.text_channels, name=log_channels["message"])
    if channel:
        embed = discord.Embed(title="🗑️ رسالة محذوفة",
                              description=f"**الكاتب:** {message.author.mention}\n**الروم:** {message.channel.mention}",
                              color=0xf1c40f)
        embed.add_field(name="المحتوى:", value=message.content or "فارغ", inline=False)
        await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    channel = discord.utils.get(before.guild.text_channels, name=log_channels["message"])
    if channel:
        embed = discord.Embed(title="✏️ تعديل رسالة",
                              description=f"**الكاتب:** {before.author.mention}\n**الروم:** {before.channel.mention}",
                              color=0x3498db)
        embed.add_field(name="قبل:", value=before.content or "فارغ", inline=False)
        embed.add_field(name="بعد:", value=after.content or "فارغ", inline=False)
        await channel.send(embed=embed)

# =============================
# أوامر البوت بالعربي
# =============================
@bot.command(name="بنج")
async def ping(ctx):
    await ctx.send("🏓 البوت شغال!")

@bot.command(name="اعادة_تشغيل")
async def restart(ctx):
    await ctx.send("🔄 جاري إعادة تشغيل البوت...")
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(name="مسح")
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 تم مسح {amount} رسالة.", delete_after=3)
    # لوج المسح
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["clear"])
    if channel:
        embed = discord.Embed(title="🗑️ تم مسح رسائل",
                              description=f"{ctx.author.mention} مسح {amount} رسالة في {ctx.channel.mention}",
                              color=0xf1c40f)
        await channel.send(embed=embed)

@bot.command(name="مساعدة")
async def help(ctx):
    embed = discord.Embed(title="📜 أوامر البوت", color=0x3498db)
    embed.add_field(name="#بنج", value="اختبار البوت", inline=False)
    embed.add_field(name="#اعادة_تشغيل", value="إعادة تشغيل البوت", inline=False)
    embed.add_field(name="#مسح [عدد]", value="مسح عدد من الرسائل", inline=False)
    embed.add_field(name="#طرد @عضو [سبب]", value="طرد عضو", inline=False)
    embed.add_field(name="#حظر @عضو [سبب]", value="حظر عضو", inline=False)
    embed.add_field(name="#فك_حظر الاسم#1234", value="فك الحظر عن عضو", inline=False)
    embed.add_field(name="#ميوت @عضو [سبب]", value="إعطاء ميوت", inline=False)
    embed.add_field(name="#فك_ميوت @عضو", value="فك الميوت", inline=False)
    embed.add_field(name="#قفل", value="لقفل الروم الحالي", inline=False)
    embed.add_field(name="#فتح", value="لفتح الروم الحالي", inline=False)
    embed.add_field(name="#اعطاء_رتبة @عضو رتبة", value="إعطاء رتبة لعضو", inline=False)
    embed.add_field(name="#سحب_رتبة @عضو رتبة", value="سحب رتبة من عضو", inline=False)
    embed.add_field(name="#قفل_جميع_الرومات", value="لقفل كل الرومات النصية", inline=False)
    embed.add_field(name="#فتح_جميع_الرومات", value="لفتح كل الرومات النصية", inline=False)
    await ctx.send(embed=embed)

# =============================
# أوامر الإدارة مع لوج لكل أمر
# =============================

# طرد عضو
@bot.command(name="طرد")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.mention} | السبب: {reason}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["mod"])
    if channel:
        embed = discord.Embed(title="👢 تم طرد عضو",
                              description=f"{member.mention} تم طرده بواسطة {ctx.author.mention}\nالسبب: {reason}",
                              color=0xe67e22)
        await channel.send(embed=embed)

# حظر عضو
@bot.command(name="حظر")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم حظر {member.mention} | السبب: {reason}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["mod"])
    if channel:
        embed = discord.Embed(title="🔨 تم حظر عضو",
                              description=f"{member.mention} تم حظره بواسطة {ctx.author.mention}\nالسبب: {reason}",
                              color=0xe74c3c)
        await channel.send(embed=embed)

# فك حظر عضو
@bot.command(name="فك_حظر")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"✅ تم فك الحظر عن {user.mention}")
            channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["mod"])
            if channel:
                embed = discord.Embed(title="✅ فك الحظر",
                                      description=f"{user.mention} تم فك الحظر بواسطة {ctx.author.mention}",
                                      color=0x2ecc71)
                await channel.send(embed=embed)
            return
    await ctx.send("❌ العضو غير موجود في قائمة البان.")

# ميوت
@bot.command(name="ميوت")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="بدون سبب"):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)
    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f"🔇 تم إعطاء ميوت لـ {member.mention} | السبب: {reason}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["mod"])
    if channel:
        embed = discord.Embed(title="🔇 تم ميوت لعضو",
                              description=f"{member.mention} بواسطة {ctx.author.mention}\nالسبب: {reason}",
                              color=0xf39c12)
        await channel.send(embed=embed)

# فك ميوت
@bot.command(name="فك_ميوت")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 تم فك الميوت عن {member.mention}")
        channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["mod"])
        if channel:
            embed = discord.Embed(title="🔊 فك الميوت",
                                  description=f"{member.mention} بواسطة {ctx.author.mention}",
                                  color=0x2ecc71)
            await channel.send(embed=embed)
    else:
        await ctx.send("❌ العضو ما عليه ميوت.")

# =============================
# أوامر القفل والفتح مع لوج خاص
# =============================

# قفل الشات الحالي
@bot.command(name="قفل_الشات")
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 تم قفل هذا الروم: {ctx.channel.mention}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["admin"])
    if channel:
        embed = discord.Embed(title="🔒 قفل الشات",
                              description=f"{ctx.author.mention} قفل الروم {ctx.channel.mention}",
                              color=0xe74c3c)
        await channel.send(embed=embed)

# فتح الشات الحالي
@bot.command(name="فتح_الشات")
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 تم فتح هذا الروم: {ctx.channel.mention}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["admin"])
    if channel:
        embed = discord.Embed(title="🔓 فتح الشات",
                              description=f"{ctx.author.mention} فتح الروم {ctx.channel.mention}",
                              color=0x2ecc71)
        await channel.send(embed=embed)

# إعطاء رتبة
@bot.command(name="اعطاء_رتبة")
@commands.has_permissions(manage_roles=True)
async def give_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ تم إعطاء {role.name} لـ {member.mention}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["admin"])
    if channel:
        embed = discord.Embed(title="✅ إعطاء رتبة",
                              description=f"{ctx.author.mention} أعطى {member.mention} رتبة {role.name}",
                              color=0x2ecc71)
        await channel.send(embed=embed)

# سحب رتبة
@bot.command(name="سحب_رتبة")
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ تم سحب {role.name} من {member.mention}")
    channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["admin"])
    if channel:
        embed = discord.Embed(title="❌ سحب رتبة",
                              description=f"{ctx.author.mention} سحب {role.name} من {member.mention}",
                              color=0xe74c3c)
        await channel.send(embed=embed)

# قفل كل الرومات النصية
@bot.command(name="قفل_جميع_الرومات")
@commands.has_permissions(manage_channels=True)
async def lock_all(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 تم قفل كل الرومات النصية!")
    admin_channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["admin"])
    if admin_channel:
        embed = discord.Embed(title="🔒 قفل جميع الرومات",
                              description=f"{ctx.author.mention} قفل كل الرومات النصية",
                              color=0xe74c3c)
        await admin_channel.send(embed=embed)

# فتح كل الرومات النصية
@bot.command(name="فتح_جميع_الرومات")
@commands.has_permissions(manage_channels=True)
async def unlock_all(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 تم فتح كل الرومات النصية!")
    admin_channel = discord.utils.get(ctx.guild.text_channels, name=log_channels["admin"])
    if admin_channel:
        embed = discord.Embed(title="🔓 فتح جميع الرومات",
                              description=f"{ctx.author.mention} فتح كل الرومات النصية",
                              color=0x2ecc71)
        await admin_channel.send(embed=embed)

# =============================
# تشغيل البوت
# =============================
bot.run("MTQxNjg1MDk4OTg2NDE5MDAzNQ.Gk7tz4.gaMAsQY0xwBLOA4MKzYO6gL-OGLXJlMwaGlhd4")
