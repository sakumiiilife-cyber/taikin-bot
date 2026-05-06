import discord
from discord.ext import commands
from discord.ui import Button, View
import os

TOKEN = os.environ['TOKEN']

WITH_MENTION = False
LEADER_ID = 0
MEMBERS = ['さくみ', 'いの', 'もちこ', 'しな', 'あずさ']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


class TaikinButton(Button):
    def __init__(self, member_name):
        super().__init__(
            label=member_name + ' 退勤',
            custom_id='taikin_' + member_name,
            style=discord.ButtonStyle.secondary
        )
        self.member_name = member_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        content = (
            '本日の業務を終了します。\n'
            'お疲れ様でした\n\n'
            '— ' + self.member_name
        )
        message = await interaction.channel.send(content)
        await message.add_reaction('❤️‍\U0001f525')
        await interaction.channel.send('\U0001f4cb **退勤報告**\n下のボタンを押してください', view=TaikinView())


class TaikinView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for member in MEMBERS:
            self.add_item(TaikinButton(member))


@bot.event
async def on_ready():
    bot.add_view(TaikinView())
    print('Bot started: ' + str(bot.user))


@bot.command()
async def setup(ctx):
    await ctx.send('\U0001f4cb 退勤報告\n下のボタンを押してください', view=TaikinView())


bot.run(TOKEN)