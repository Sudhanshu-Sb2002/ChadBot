import discord
from discord.ext import tasks, commands
import asyncio
import datetime as dt
from datetime import datetime as datetime
from collections import deque
import random

global meta_list
global q_len
intents = discord.Intents.default()
intents.members = True
intents.presences=True
bot = commands.Bot(command_prefix=']', case_insensitive=True,intents=intents)

bot.update_time = dt.timedelta(minutes=5)
bot.recent_time = dt.timedelta(minutes=10)
bot.annoy_time=dt.timedelta(minutes=20)
bot.annoys=[]
def channel_data_init():
    # initialises the data collection list for channels
    return [deque(maxlen=q_len), 0, 0, True]
    # queue of times , recent messages , total messages, whether channel will count towards count


def initialise():
    global meta_list
    global q_len
    # Set the value of q_len (i.e the maximum number of messages that can be considered to be 'recent'
    q_len = 100

    # Creating the meta list- a dictionary with: (Keys - Guild objects(list of guilds where the bot is present),
    # Values - A dictionary with: (Keys-Text Channel Objects, Values- a list [creation time for all messages within
    # recent time, no. of recent messages(within recent time), no of messages]))
    meta_list = dict()
    guild_list = bot.guilds
    for i in guild_list:
        meta_list[i] = {j: channel_data_init() for j in i.text_channels}


def best_channel_in_servers(server_list):
    max_messages, max_channel = 0, None

    for server, server_data in server_list.items():
        # print(server)
        for channel, channel_data in server_data.items():
            if channel_data[3]:
                if channel_data[1] > max_messages:
                    max_messages = channel_data[1]
                    max_channel = channel
    try:
        # print(max_channel)
        return [max_channel, server_list[max_channel.guild][max_channel]]
    except AttributeError:
        return None


def best_channel(server=None):
    if server is None:
        return best_channel_in_servers(meta_list)
    else:
        return best_channel_in_servers({server: meta_list[server]})


def channels_printer(channel):
    return '<#'+str(channel.id)+'>'
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="]help"))

    # Final Ready message
    print("I am C H A D")


@bot.event
async def on_message(message):
    # We do not bother with messages that are sent by us

    if message.author == bot.user:
        return

    # Here we count all the messages not sent by bots and add them to counts
    try:

        if not message.author.bot and message.guild is not None:
            if message.channel in meta_list[message.guild]:
                meta_list[message.guild][message.channel][0].append(message.created_at)
                meta_list[message.guild][message.channel][1] = +1
                meta_list[message.guild][message.channel][2] = +1
    except NameError:
        pass
    await bot.process_commands(message)
    return


@bot.event
async def on_guild_channel_create(channel):
    global meta_list
    meta_list[channel.guild][channel] = channel_data_init()
    return


@tasks.loop(seconds=bot.update_time.seconds)
async def update_status():
    channel = best_channel(None)

    if channel is None:
        # print(2)
        # await bot.change_presence(activity=discord.Activity(status=discord.Status.idle, name='Type ]help for help', state='Being CHAD',details=" This Server is currently dead"))
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="]help (cos this server dead)"))
    else:
        # print(1)
        # await bot.change_presence(activity=discord.Activity(name='Watching #' + channel[0].name, state='Watching ]help',details=str(channel[0][1]) + " Messages sent in the last " + str(bot.recent_time.seconds / 60) + "minutes"))
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name='#' + channel[0].name))


@tasks.loop(seconds=bot.recent_time.seconds)
async def update_list():
    global meta_list
    current_time = datetime.now()
    for server, channel_list in meta_list.items():
        for channel, channel_data in channel_list.items():
            while len(channel_data[0]) > 0 and channel_data[0][0] + bot.recent_time < current_time:
                channel_data[0].popleft()
                channel_data[1] -= 1


@tasks.loop(seconds=bot.annoy_time.seconds)
async def annoyer(ctx, person_id):

    print(person_id)
    print(int(person_id[3:-1]))

    guild=ctx.guild
    person=guild.get_member(int(person_id[3:-1]))
    print(person)
    #channel = random.choice(list(meta_list[ctx.guild].keys()))
    print(person.status)
    if person.status is not discord.Status.offline:
        await person.send(person_id)
    else:
        annoy_waiter.start(ctx,person,person_id)
        annoyer.cancel()


@tasks.loop(seconds=120)
async def annoy_waiter(ctx, person,person_id):
    # channel = random.choice(list(meta_list[ctx.guild].keys()))
    if person.status != discord.Status.offline:
        annoyer.start(ctx,person_id)
        annoy_waiter.cancel()


@bot.command(name='set_annoy_time',help='set time interval between pinging (in minutes)')
async def set_annoy_time(ctx,minutes):
    annoyer.change_interval(seconds=dt.timedelta(minutes=int(minutes)).seconds)

@bot.command(name="hi", help="Greets a person ")
async def hi(ctx):
    await ctx.send("hi")

    return


@bot.command(name='top', help='gives the channel in this server with maximum usage "recently"')
async def top(ctx):
    await ctx.send(channels_printer(best_channel(ctx.guild)[0]))
    return


@bot.command(name='start', help='starts displaying message counts in status')
async def start(ctx):
    initialise()
    update_list.start()
    update_status.start()


@bot.command(name='stop_count',
             help='Stops considering the mentioned channel for max message count(to disinclude spam channels)')
async def stop_count(ctx, channel_id):
    global meta_list
    channel_data = meta_list[ctx.guild][bot.get_channel(int(channel_id[2:-1]))]
    channel_data[3] = False
    await ctx.send(channel_id+"was removed.The current list of channels whose messages are being counted is:")
    await show_counted_channels(ctx)

@bot.command(name='add_count', help='Adds the mentioned channel to max message count', category='Most used channel')
async def add_count(ctx, channel_id):
    global meta_list
    channel_data = meta_list[ctx.guild][bot.get_channel(int(channel_id[2:-1]))]
    channel_data[3] = True
    await ctx.send(channel_id+"was added.The current list of channels whose messages are being counted is:")
    await show_counted_channels(ctx)

@bot.command(name='show_counted_channels',
             help='gives the list of channels being counted in the server for max channel count')
async def show_counted_channels(ctx):
    x=""
    for (guild, guild_data) in meta_list[ctx.guild].items():
        if guild_data[3]:
            x+=channels_printer(guild)+'\n'
    await ctx.send(x)

@bot.command(name='annoy', help='pings a person in a random at intervals of 1 min')
async def annoy(ctx, person):
    annoyer.start(ctx, person)


@bot.command(name='stop_annoy', helps='stops pinging people')
async def stop_annoy(ctx):
    annoyer.stop()


bot.run('ODA2MzM5MjA1Mjc3ODEwNjk4.YBn_5w.MaJf4N7pSRdh_Vf8rSPnOqQNT6g')
