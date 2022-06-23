import discord
from discord.ext import commands
import random
import asyncio
import os

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
#tic tac toe game
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]
@client.command()
async def game(ctx, p1: discord.Member, p2: discord.Member):
	global count
	global player1
	global player2
	global turn
	global gameOver

	if gameOver:
		global board
		board = [
		    ":white_large_square:", ":white_large_square:",
		    ":white_large_square:", ":white_large_square:",
		    ":white_large_square:", ":white_large_square:",
		    ":white_large_square:", ":white_large_square:",
		    ":white_large_square:"
		]
		turn = ""
		gameOver = False
		count = 0

		player1 = p1
		player2 = p2

		# print the board
		line = ""
		for x in range(len(board)):
			if x == 2 or x == 5 or x == 8:
				line += " " + board[x]
				await ctx.send(line)
				line = ""
			else:
				line += " " + board[x]

		# determine who goes first
		num = random.randint(1, 2)
		if num == 1:
			turn = player1
			await ctx.send(" <@" + str(player1.id) + ">your turn.")
		elif num == 2:
			turn = player2
			await ctx.send(" <@" + str(player2.id) + ">your turn.")
	else:
		await ctx.send("Wait for the current match to end")


@client.command()
async def place(ctx, pos: int):
	global turn
	global player1
	global player2
	global board
	global count
	global gameOver

	if not gameOver:
		mark = ""
		if turn == ctx.author:
			if turn == player1:
				mark = ":regional_indicator_x:"
			elif turn == player2:
				mark = ":o2:"
			if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
				board[pos - 1] = mark
				count += 1

				# print the board
				line = ""
				for x in range(len(board)):
					if x == 2 or x == 5 or x == 8:
						line += " " + board[x]
						await ctx.send(line)
						line = ""
					else:
						line += " " + board[x]

				checkWinner(winningConditions, mark)
				print(count)
				if gameOver == True:
					await ctx.send(mark + " Won")
				elif count >= 9:
					gameOver = True
					await ctx.send("tie")

				# switch turns
				if turn == player1:
					turn = player2
				elif turn == player2:
					turn = player1
			else:
				await ctx.send("Wtf")
		else:
			await ctx.send("It's not your turn.")
	else:
		await ctx.send("For a new game type ?game ")


def checkWinner(winningConditions, mark):
	global gameOver
	for condition in winningConditions:
		if board[condition[0]] == mark and board[
		    condition[1]] == mark and board[condition[2]] == mark:
			gameOver = True


@game.error
async def tictactoe_error(ctx, error):
	print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Tag 2 players")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("Dont't forget to ping player")


@place.error
async def place_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Type the position you want")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("Type  an appropriate position")	
#8ball
@client.command(pass_context=True)
async def ball(ctx, statement=None):
	answers = [
	    'As I see it, yes.', 'Ask again later.', 'Better not tell you now.',
	    'Cannot predict now.', 'Concentrate and ask again.',
	    'Don’t count on it.', 'It is certain.', 'It is decidedly ',
	    'Most likely.', 'My reply is no.', 'My sources say no.',
	    'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.',
	    'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.',
	    'Yes – definitely.', 'You may rely on it.',  
	      '50/50'  
	]
	if statement == None:
		await ctx.message.channel.send(
		    'What do you want??? Give me a question.'
		)
	else:
		item_1 = random.choice(answers)
		await ctx.channel.send(item_1)
client.run("YOUR TOKEN")