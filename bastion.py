import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime
from discord.enums import Status

bot = commands.Bot(command_prefix = commands.when_mentioned_or('!'), description = 'Bastion')
answer = ('DO IT!', 'Nope', 'I don\'t think so :\\', 'It sucks.', 'Dunno :C',)
response = ('Doo-woo.', 'Boo boo doo de doo.', 'Dweet! Dweet! Dweet!',
            'Hee hoo hoo hoo-wee, hee hee hoo hoo hoo-wee.', 'Zwee?')

modes = {'hide' : True,     #отвечает только в black_forest
         'defense' : False, #посылает всех, кроме меня
         'log' : True,      #лог в консоль
         'greet': True,     #приветствует всех прибывших
         'users_log' : True,#лог пользователей в канале log
         'spam' : False} #ухади
#read help
with open('help.txt', 'r', encoding = 'utf-8') as file:
    help_message = file.read()

#read token
with open('token.txt', 'r', encoding = 'utf-8') as file:
    token = file.read()

def log(*message):
    '''Prints log record'''
    print(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    for msg in message:
        print(msg, end=' ')
    print('\n------')

@bot.event
async def on_ready():
    await bot.send_message(bot.get_channel('321752343009951755'), 'I\'m alive! BOOP!')
    if modes['log']:
        log('Logged in as:\n', bot.user.name, '\n', bot.user.id)

    #await client.change_presence(game=discord.Game(name='game'))

#######################
#Non-stadrard commands#
#######################
@bot.event
async def on_message(message):

#do not reply myself
    if message.author == bot.user:
        return

#if hide
    elif modes['hide'] and message.channel.name != 'black_forest':
        return

#if defense
    elif modes['defense'] and message.author.id != '214030651588870144': #Добавь сюда and message.author.id != 'твой id'
        msg = 'INTRUDERS! \*LSHIFT, LEFT CLICK\* GET THE FUCK OUT, '                                       #Если хочешь чтобы он тебя не посылал в дефенс моде
        msg += '{0.author.mention}!'.format(message)                                                       #Id можно получить по !my_id
        await bot.send_message(message.channel, msg)
        if modes['log']:
            log('Intruder:', message.author.name)

        return

#override !help
    elif message.content.startswith('!help'):
        msg = '{0.author.mention}, '.format(message)
        msg += help_message
        await bot.send_message(message.channel, msg)
        if modes['log']:
            log('Help requested from', message.author.name)

        return

#Bastion!
    #elif message.content.startswith('Bastion!'):
    elif message.content == '<@321783873853980672>':
        msg = '{0.author.mention}, '.format(message)
        msg += random.choice(response)
        await bot.send_message(message.channel, msg)
        if modes['log']:
            log('Responded to', message.author.name)

        return

#Bastion .. ?
    elif bot.user.mentioned_in(message) and message.content.endswith('?'):
        msg = '{0.author.mention}, '.format(message)
        msg += random.choice(answer)
        await bot.send_message(message.channel, msg)
        if modes['log']:
            log('Answered to', message.author.name)

        return

    else:
        await bot.process_commands(message) #Run standart command meth

###################
#Standard commands#
###################

#bot_kill
@bot.command(description = 'Shutdown', pass_context = 'True')
async def bot_kill(ctx):
    await bot.reply('BOOoooop.. :C')
    await bot.close()
    if modes['log']:
        log('Shutdown by', ctx.message.author.name)
    raise SystemExit


#channel
@bot.command(description = 'Channel name/id', pass_context = 'True')
async def channel(ctx):
    #msg = '{0.author.mention}, '.format()
    #msg += message.channel.name
    await bot.reply(ctx.message.channel.name + '\n' + ctx.message.channel.id)
    if modes['log']:
        log('!channel by', ctx.message.author.name)

#set_game
@bot.command(description = 'Set playing... status', pass_context = 'True')
async def set_game(ctx, game = None):
    if game == None:
        await bot.change_presence(game = None)
        await bot.reply('I wanna play something :C')
    else:
        await bot.change_presence(game = discord.Game(name = game))
        await bot.reply('Now I\'m playing ' + game)
    if modes['log']:
        log('!set_game by', ctx.message.author.name, '\n', str(game))

#hide
@bot.command(description = 'Working in black_forest only', pass_context = 'True')
async def hide(ctx):
    modes['hide'] = not modes['hide']
    msg = 'Stealth mode '

    if modes['hide']:
        msg += 'ON'
    else:
        msg += 'OFF'

    await bot.reply(msg)
    if modes['log']:
        log(msg, 'by', ctx.message.author.name)

#defense
@bot.command(description = 'Responding to owner only', pass_context = 'True')
async def defense(ctx):
    modes['defense'] = not modes['defense']
    msg = 'Defense mode '

    if modes['defense']:
        msg += 'ON'
    else:
        msg += 'OFF'

    await bot.reply(msg)
    if modes['log']:
        log(msg, 'by', ctx.message.author.name)

#greet
@bot.command(description = 'Greet everyone, who logged in', pass_context = 'True')
async def greet(ctx):
    modes['greet'] = not modes['greet']
    msg = 'Greet mode '

    if modes['greet']:
        msg += 'ON'
    else:
        msg += 'OFF'

    await bot.reply(msg)
    if modes['log']:
        log(msg, 'by', ctx.message.author.name)

#users_log
@bot.command(description = 'Print to log channel', pass_context = 'True')
async def users_log(ctx):
    modes['users_log'] = not modes['users_log']
    msg = 'Log mode '

    if modes['users_log']:
        msg += 'ON'
    else:
        msg += 'OFF'

    await bot.reply(msg)
    if modes['log']:
        log(msg, 'by', ctx.message.author.name)

#mode
@bot.command(description = 'Print mode', pass_context = 'True')
async def mode(ctx):
    msg = '\nStealth mode '
    if modes['hide']:
        msg += 'ON'
    else:
        msg += 'OFF'

    msg += '\nDefense mode '
    if modes['defense']:
        msg += 'ON'
    else:
        msg += 'OFF'

    msg += '\nGreet mode '
    if modes['greet']:
        msg += 'ON'
    else:
        msg += 'OFF'

    msg += '\nLog mode '
    if modes['users_log']:
        msg += 'ON'
    else:
        msg += 'OFF'

    await bot.reply(msg)

    if modes['log']:
        log('!modes', ctx.message.author.name)

#my_id
@bot.command(description = 'Print your ID', pass_context = 'True')
async def my_id(ctx):
    await bot.reply(ctx.message.author.id)
    if modes['log']:
        log('Id requested by', ctx.message.author.name)

#tts
@bot.command(description = 'Text-to-Speech', pass_context = 'True')
async def tts(ctx, msg):
    await bot.say(msg, tts=True)
    if modes['log']:
        log('TTS used by', ctx.message.author.name, '\nMessage: \"', msg, '\"')

#spam
@bot.command(description = 'SPAM DIS', pass_context = 'True')
async def spam(ctx, msg = 'SPAM'):
    modes['spam'] = not modes['spam']
    if modes['log']:
        if modes['spam']:
            log(ctx.message.author.name, 'started spam')
        else:
            log(ctx.message.author.name, 'stopped spam')
    while modes['spam']:
        await bot.say(msg)

###########
#Listeners#
###########

#Greet everyone who connects
@bot.listen('on_member_update')
async def greet(before, after):
    if not modes['greet']:
        return

    if before.status == Status.offline and after.status == Status.online:
        await bot.send_message(bot.get_channel('320955467700502528'), 'Hi there, ' + '{0.mention}!'.format(after))
        if modes['log']:
            log('Greeted', after.name)

#WRONG GAEM XD
@bot.listen('on_member_update')
async def wrong_game(before, after):
    if after.game == None:
        return
    
    if after.game.name == 'League of Legends' or after.game.name == 'DOTA 2':
        await bot.send_message(bot.get_channel('320955467700502528'), '{0.mention}, '.format(after) + 'сейчас бы в 2к17 в жопу подолбиться :\\')
        if modes['log']:
            log(after.name, 'Lel\'d')

#Members log
@bot.listen('on_member_update')
async def members_log(before, after):
    if not modes['users_log']:
        return

    if before.status == Status.offline and after.status == Status.online:
        msg = datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' {0.name} logged in.'.format(after)
        await bot.send_message(bot.get_channel('322963563431854080'), msg)
    elif before.status == Status.online and after.status == Status.offline:
        msg = datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' {0.name} logged out.'.format(after)
        await bot.send_message(bot.get_channel('322963563431854080'), msg)

bot.run(token)
