import discord
from discord.ext import commands
import random
import asyncio

client = commands.Bot(command_prefix='?')   #you can use any command prefix you want
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online,
	                             activity=discord.Game('League of Legends'))
  print('Logged In {0.user}'.format(client))                    #print to get a notification when the bot is running

@client.event
async def on_member_join(member):
    channel = client.get_channel(834071669538553866)
    await channel.send("Welcome to the server{}!!!\n".format(member.mention))       #welcomes new members in the server

@client.command(pass_context=True)          
async def delete(ctx,messages=2):                              #delete messages(command) - 2 by default
	await ctx.channel.purge(messages)

@client.event
async def on_reaction_add(reaction, user):
 guild = client.guilds[0] 
 if user.id != client.user.id:
    if reaction.emoji == ('✅'):
        await reaction.channels.send("Approved")                 #add whatever you want 

                                                                #guess the number game
async def check_guess(count, choice, lives, nr, ctx):
	try:
		attempt = int(choice.content)
		if attempt == nr:
			await ctx.message.channel.send('You guessed!!!!!!!!!Poggers')
			return
		if (lives <= 1):
			await ctx.message.channel.send(
			    'You don''t have any lives left.The number I was thinking of was {}.'
			    .format(nr))
			return
		else:
			if attempt > nr:
				count += 1
				lives = 4 - count
				await ctx.message.channel.send(
				    "Wrong!!! The number I'm thinking of i smaller.You have {} lives left"
				    .format(lives))
				choice = await client.wait_for(
				    'message',
				    check=lambda message: message.author == ctx.author)
				asyncio.create_task(
				    check_guess(count, choice, lives, nr, ctx))
			elif attempt < nr:
				count += 1
				lives = 4 - count
				await ctx.message.channel.send(
				    "Wrong!!! The number I'm thinking of i bigger.You have {} lives left"
				    .format(lives))
				choice = await client.wait_for(
				    'message',
				    check=lambda message: message.author == ctx.author)
				asyncio.create_task(
				    check_guess(count, choice, lives, nr, ctx))
	except ValueError:
		await ctx.channel.send('You can''t type this number')
		choice = await client.wait_for(
		    'message', check=lambda message: message.author == ctx.author)
		asyncio.create_task(check_guess(count, choice, lives, nr, ctx))

@client.command(pass_context=True)
async def guess(ctx):
	nr = random.randint(1, 20)
	count = 0
	index = 1
	lives = 3
	await ctx.message.channel.send(
	    'You have 4 attempts to guess a number from 1 to 20')
	choice = await client.wait_for(
	    'message', check=lambda message: message.author == ctx.author)
	asyncio.create_task(check_guess(count, choice, lives, nr, ctx))
