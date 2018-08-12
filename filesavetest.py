import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import os


token = str(os.environ.get("BOT_TOKEN"))

server_id = str(os.environ.get("SERVER_ID"))

storage_server_id = str(os.environ.get("STORAGE_SERVER_ID"))
storage_channel_id = str(os.environ.get("STORAGE_CHANNEL_ID"))


Client = discord.Client()
bot = commands.Bot(command_prefix="!")


async def get_latest_bot_message(storage_channel_object):

	message_object_found = False
	async for message_object in bot.logs_from(storage_channel_object):
		if message_object.author.id == bot.user.id:
			message_object_found = True
			return message_object
			break
	if not message_object_found:
		return None



async def save_data(data_to_save):

	global storage_server_id
	global storage_channel_id

	storage_server_object = bot.get_server(storage_server_id)
	storage_channel_object = storage_server_object.get_channel(storage_channel_id)

	message_object = await get_latest_bot_message(storage_channel_object)

	if message_object == None:
		await bot.send_message(storage_channel_object, data_to_save)
	else:
		await bot.edit_message(message_object, new_content=data_to_save)



async def load_data():

	global storage_server_id
	global storage_channel_id

	storage_server_object = bot.get_server(storage_server_id)
	storage_channel_object = storage_server_object.get_channel(storage_channel_id)

	message_object = await get_latest_bot_message(storage_channel_object)

	if message_object == None:
		return None
	else:
		return message_object.content



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
		await save_data(str(message.content[6:]))



	elif message.content.lower().strip() == "!load":
		filedata = await load_data()
		if filedata == None:
			await bot.send_message(message.channel, "No data saved yet!")
		else:
			print("Loaded")
			await bot.send_message(message.channel, "Data: {0}".format(filedata))



bot.run(token)

