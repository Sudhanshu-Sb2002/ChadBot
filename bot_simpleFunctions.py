import discord
from discord.ext import commands
from discord.ui import Button
from discord.ui import View

player1keyword = "playa1"
player2keyword = "playa2"
endword = "end"


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        print("C H A D can say hi")
        # Ready message

    @commands.command(name='Hi', help='Biggest Brains function')
    async def Hi(self, ctx):
        button = Button(label="Hello", style=discord.ButtonStyle.link,
                        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", emoji="👋")
        view = View(timeout=100000)
        view.add_item(button)
        await ctx.send("Hi fellow Chad.", view=view)
        return

    @commands.command(name='ping', help='returns ping\latency  AND pings u')
    async def ping(self, ctx):
        await ctx.reply('Pong! {0}'.format(round(self.bot.latency * 100, 1)))
        return

    @commands.command(name="tictactoe", help="play Tic tac Toe")
    async def tictactoe(self, ctx):
        view = TicTacToe(ctx.message.author)
        await ctx.send("Tic Tac Toe match initiated by " +ctx.message.author.name,view=view)

class Button2(Button):
    def __init__(self):

        super().__init__(label="Player 2 Ready?", style=discord.ButtonStyle.green, row=3,
                       custom_id=player2keyword)

    async def callback(self,interaction):

        self.view.player2 = interaction.user

        self.view.currentplayer=self.view.player1
        for i in self.view.buttons:
            i.disabled = False

        self.view.statusbutton.label = self.view.player1.name + "'s turn"
        self.view.remove_item(self)
        forfiet = [i for i in self.view.children if i.custom_id == endword][0]
        forfiet.label="Forfeit the match (accept defeat?)"
        await interaction.response.edit_message( content=self.view.player1.name +" (X) vs (O) "+self.view.player1.name,view=self.view)

class TicTacToe(View):

    def __init__(self, player1):
        super().__init__()
        self.player1 = player1
        self.player2 = None
        self.currentplayer = self.player1
        self.statusbutton = Button(label="Player 2 to be decided.........", style=discord.ButtonStyle.link,
                                   url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", row=4)
        self.buttons = [XObutton( labels="_", rows=i// 3) for i in range(0, 9)]
        for i in range(0, 9):
            self.add_item(self.buttons[i])
        self.add_item(self.statusbutton)


        self.p2button=Button2()


        self.add_item(self.p2button)


    def xoro(self, user):
        print(user,self.currentplayer,self.player1)


        if user == self.player1 == self.currentplayer:
            return 'X', discord.ButtonStyle.blurple
        elif user == self.player2  ==self.currentplayer:
            return '0', discord.ButtonStyle.green
        else:
            print("poopsieee")
            return '_',discord.ButtonStyle.gray

    def changeplayer(self, user):
        if user == self.player1:
            self.statusbutton.label = self.player1.name + "'s turn"
            return self.player2
        else:
            self.statusbutton.label = self.player2.name + "'s turn"
            return self.player1

    def diagnalswin(self):
        buttons = self.buttons
        if buttons[0].label ==buttons[4].label == buttons[8].label != '_':
            self.whowon(buttons[0].label)

            return True
        if buttons[2].label ==buttons[4].label ==buttons[6].label != '_':
            self.whowon(buttons[0].label)

            return True
        return False

    def rowwin(self, index,):
        buttons = self.buttons

        if buttons[index*3 + 0].label ==buttons[index*3 + 1].label ==buttons[index*3 + 2].label != '_':
            self.whowon(buttons[index*3 + 0].label)

            return True
        return False

    def column_win(self, index):
        buttons = self.buttons
        if buttons[index + 0].label ==buttons[index + 3].label ==buttons[index + 6].label != '_':
            self.whowon(buttons[index + 0].label)

            return True
        return False

    def whowon(self, winningcharacter):

        if winningcharacter == 'X':

            for i in self.buttons:
                if i.label=='X':
                    i.style=discord.ButtonStyle.green
                elif i.label=='O':
                    i.style = discord.ButtonStyle.red

            self.statusbutton.label = self.player1.name + " Won!!!"

        elif winningcharacter == 'O':
            for i in self.buttons:
                if i.label == 'O':
                    i.style = discord.ButtonStyle.green
                elif i.label == 'X':
                    i.style = discord.ButtonStyle.red

            if self.player2 != None:

                self.statusbutton.label = self.player2.name + " Won!!! \n gg wp ez"
            if self.player2 ==None:
                self.statusbutton.label=self.player1.name+" forfeited, cos he aint go no frands"
        forfiet=[i for i in self.children if i.custom_id == endword][0]
        forfiet.disabled=True
        forfiet.style=discord.ButtonStyle.gray
        for i in self.buttons:
            i.disabled = True

    def checkwin(self):
        print('yop')
        self.diagnalswin()
        print('yop')
        self.rowwin(0)
        self.rowwin(1)
        self.rowwin(2)
        self.column_win(0)
        self.column_win(1)
        self.column_win(2)
        for i in self.buttons:
            if i.label=='_':
                return
        forfiet = [i for i in self.children if i.custom_id == endword][0]
        forfiet.disabled = True
        for i in self.buttons:
            i.disabled = True
        self.statusbutton.label ="Draw Match"



    @discord.ui.button(label=" Stop Searching ", style=discord.ButtonStyle.red, row=3, custom_id=endword)
    async def button_callback(self, button, interaction):
        if interaction.user == self.player1:
            self.whowon('O')
        elif interaction.user == self.player2:
            self.whowon('X')
        await interaction.response.edit_message(view=self)



class XObutton(Button):

    def __init__(self, labels, rows):
        super().__init__(label=labels, row=rows, disabled=True)


    async def callback(self, interaction):

        new_label,new_buttonstyle = TicTacToe.xoro(self.view, interaction.user)

        if new_label == '_':
            return
        self.label = new_label
        self.style = new_buttonstyle
        self.disabled = True
        print(1)
        self.view.currentplayer = TicTacToe.changeplayer(self.view, interaction.user)
        TicTacToe.checkwin(self.view)
        print(self.view)
        await interaction.response.edit_message(view=self.view)



def setup(bot):
    bot.add_cog(Basic(bot))
