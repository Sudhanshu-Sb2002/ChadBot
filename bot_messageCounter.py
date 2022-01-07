import datetime as dt
from collections import deque
from datetime import datetime as datetime

import discord
from discord.ext import tasks, commands

update_time = dt.timedelta(minutes=1)
recent_time = dt.timedelta(minutes=15)


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Set the value of q_len (i.e the maximum number of messages that can be considered to be 'recent'
        self.q_len = 100
        self.meta_list = dict()

        print("I am a C H A D who counts message like creep")

    def startupvariables(self):

        # Creating the meta list- a dictionary with: (Keys - Guild objects(list of guilds where the bot is present),
        # Values - A dictionary with: (Keys-Text Channel Objects, Values- a list [creation time for all messages within
        # recent time, no. of recent messages(within recent time), no of messages]))


        for i in self.bot.guilds:
            self.meta_list[i] = self.server_data_init(i)

        self.update_list.start()
        self.update_status.start()
        # Ready message

        return

    @commands.command(name='startcount', help='starts the counting process')
    async def startcount(self, ctx):
        self.startupvariables()
        return

    def server_data_init(self,server):
        if server is not None:
            return {j: self.channel_data_init() for j in server.text_channels}
    def channel_data_init(self):
        # initialises the data collection list for channels
        return [deque(maxlen=self.q_len), 0, 0, True]
        # queue of times , recent messages , total messages, whether channel will count towards count

    def most_used_channel(self, server=None):
        if server is None:
            return self.most_used_channel_core(self.meta_list)
        else:
            return self.most_used_channel_core({server: self.meta_list[server]})

    def most_used_channel_core(self, server_list):
        max_messages, max_channel = 0, None
        max_data=None
        for server, server_data in server_list.items():
            print(server)
            for channel, channel_data in server_data.items():
                if channel_data[3]:
                    if channel_data[1] >= max_messages:
                        max_data=channel_data
                        max_messages = channel_data[1]
                        max_channel = channel

         # print(max_channel)
        return [max_channel,max_data]

    @commands.Cog.listener()
    async def on_message(self, message):
        # We do not bother with messages that are sent by bots

        if message.author == self.bot.user:
            return
        # Here we count all the messages not sent by bots and add them to counts
        try:

            if not message.author.bot and message.guild is not None:
                if message.channel in self.meta_list[message.guild]:
                        self.meta_list[message.guild][message.channel][0].append(message.created_at)
                        self.meta_list[message.guild][message.channel][1] = +1
                        self.meta_list[message.guild][message.channel][2] = +1
        except IndentationError and KeyError:
            pass
        await self.bot.process_commands(message)
        return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        self.meta_list[channel.guild][channel] = self.channel_data_init()
        return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        self.meta_list[channel.guild].pop(channel)
        return

    @tasks.loop(seconds=update_time.seconds)
    async def update_status(self):
        channel = self.most_used_channel(None)

        if channel is None:
            # print(2)
            # await bot.change_presence(activity=discord.Activity(status=discord.Status.idle, name='Type ]help for help', state='Being CHAD',details=" This Server is currently dead"))
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="]help (cos this server dead)"))
        else:
            # print(1)
            # await bot.change_presence(activity=discord.Activity(name='Watching #' + channel[0].name, state='Watching ]help',details=str(channel[0][1]) + " Messages sent in the last " + str(bot.recent_time.seconds / 60) + "minutes"))
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name='#' + channel[0].name))

    @tasks.loop(seconds=recent_time.seconds)
    async def update_list(self):

        current_time = datetime.now()
        for server, channel_list in self.meta_list.items():
            for channel, channel_data in channel_list.items():
                while len(channel_data[0]) > 0 and channel_data[0][0] + recent_time < current_time:
                    channel_data[0].popleft()
                    channel_data[1] -= 1

    @commands.command(name='top', help='gives the channel in this server with maximum usage "recently"')
    async def top(self, ctx):
        await ctx.send(self.channel_tag_in_message(self.most_used_channel(ctx.guild)[0]))
        return
    @commands.command(name='data', help='gives the channel usages')
    async def data(self, ctx):
        print(self.meta_list)
        print(self.meta_list[ctx.guild])
        print('\n'+str(self.meta_list[ctx.guild].items()))
        print('\n' + str(self.meta_list[ctx.guild].items()))
        x=''
        for i, j in self.meta_list[ctx.guild].items():

            x+=self.channel_tag_in_message(i)+"\t`"+str([j[2]])+"`"+"\n"
        await ctx.send(x)
        return
    @commands.command(name='stop_count',
                      help='Stops considering the mentioned channel for max message count(to disinclude spam channels)')
    async def stop_count(self, ctx, channel_id):

        channel_data = self.meta_list[ctx.guild][self.bot.get_channel(int(channel_id[2:-1]))]
        channel_data[3] = False
        await ctx.send(channel_id + "was removed.The current list of channels whose messages are being counted is:")
        await self.show_counted_channels(ctx)

    @commands.command(name='add_count', help='Adds the mentioned channel to max message count',
                      category='Most used channel')
    async def add_count(self, ctx, channel_id):

        channel_data = self.meta_list[ctx.guild][self.bot.get_channel(int(channel_id[2:-1]))]
        channel_data[3] = True
        await ctx.send(channel_id + "was added.The current list of channels whose messages are being counted is:")
        await self.show_counted_channels(ctx)

    @commands.command(name='show_counted_channels',
                      help='gives the list of channels being counted in the server for max channel count')
    async def show_counted_channels(self, ctx):
        x = ""
        for (guild, guild_data) in self.meta_list[ctx.guild].items():
            if guild_data[3]:
                x += self.channel_tag_in_message(guild) + '\n'
        await ctx.send(x)

    def channel_tag_in_message(self, channel):
        return '<#' + str(channel.id) + '>'
    # End of Class


def setup(bot):
    bot.add_cog(Status(bot))
