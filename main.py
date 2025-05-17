import os
import discord
from discord.ext import commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True  # Pour lire les messages
intents.members = True          # Pour voir les membres
intents.guilds = True 
intents.presences = True        # Pour voir le statut des membres 
bot = commands.Bot(command_prefix='!', intents=intents)
token = os.environ['TOKEN_BOT_DISCORD']

CHANNEL_ID = 0
GUILD_ID = 0

@bot.command()
async def setChannel(ctx):
  global CHANNEL_ID
  CHANNEL_ID = ctx.channel.id
  global GUILD_ID
  GUILD_ID = ctx.guild.id
  await ctx.send(f"Le salon a été défini sur ce salon dans le serveur {ctx.guild.name}.")

@bot.command()
async def getChannelId(ctx):
  await ctx.send(ctx.channel.id)
@bot.command()
async def getGuildId(ctx):
  await ctx.send(ctx.guild.id)
  
  

@bot.event
async def on_ready():
  print("┌-------------------------------------------------------------------┐")
  print("|Premièrement, tu dois définir le salon avec la commande !setChannel|")
  print("└-------------------------------------------------------------------┘")
  update_online_members.start()
    
@tasks.loop(seconds=10)  # vérifie toutes les 30 secondes
async def update_online_members():
  if GUILD_ID == 0:
    return
  if(CHANNEL_ID == 0):
    return
    
  guild = bot.get_guild(GUILD_ID)
  if guild is None:
    return

  online_members = sum(1 for m in guild.members if m.status != discord.Status.offline and not m.bot)
  channel = guild.get_channel(CHANNEL_ID)

  if channel:
    await channel.edit(name=f"En ligne : {online_members}")
  

bot.run(token)