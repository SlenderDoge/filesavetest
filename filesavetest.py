import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os


token = str(os.environ.get("BOT_TOKEN"))

server_id = str(os.environ.get("SERVER_ID"))

filename = str(os.environ.get("FILENAME"))
filedata = None

Client = discord.Client()
bot = commands.Bot(command_prefix="!")


try:
	filehandle = open(filename, "r")
	filedata = json.load(filehandle)
except Exception as e:
	pass


@bot.event
async def on_ready():
	await bot.wait_until_ready()
	print (bot.user.name + " is ready")
	print ("ID: " + bot.user.id)

@bot.event
async def on_message(message):

	global server_id
	global filename
	global filedata

	if message.content[:6].lower() == "!save ":
		filedata = str(message.content[6:])
		filehandle = open(filename, "w")
		json.dump(filedata, filehandle)
		filehandle.close()

	elif message.content.lower().strip() == "!load":
		if filedata != None:
			await bot.send_message(message.channel, "Data: {0}".format(str(filedata)))
		else:
			await bot.send_message(message.channel, "No data saved yet!")

bot.run(token)
