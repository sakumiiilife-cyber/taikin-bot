import discord
from discord.ext import commands
from discord.ui import Button, View
import os

TOKEN = os.environ['TOKEN']

# ===== 設定 =====
WITH_MENTION = False  # メンションあり→True、なし→False
LEADER_ID = 0        # WITH_MENTION=True の場合、リーダーのDiscord IDを数字で入れる
MEMBERS = ['さくみ', 'いの', 'もちこ', 'しな', 'あずさ']
# ================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


class TaikinButton(Button):
    def __init__(self, member_name):
        super().__init__(
            label=f'{member_name}　退勤',
            custom_id=f'taikin_{member_name}',
            style=discord.ButtonStyle.primary
        )
        self.member_name = member_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if WITH_MENTION and LEADER_ID:
            content = (
                f'<@{LEADER_ID}> さん\n'
                f'本日の業務を終了します。\n'
                f'お疲れ様でした🙇🏻‍♀️\n\n'
                f'— {self.member_name}'
            )
        else:
            content = (
                f'本日の業務を終了します。\n'
                f'お疲れ様でした🙇🏻‍♀️\n\n'
                f'— {self.member_name}'
            )

        message = await interaction.channel.send(content, view=TaikinView())
　　　　 await message.add_reaction('❤️‍🔥')



class TaikinView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for member in MEMBERS:
            self.add_item(TaikinButton(member))


@bot.event
async def on_ready():
    bot.add_view(TaikinView())
    print(f'✅ {bot.user} 起動しました')


@bot.command()
async def setup(ctx):
    await ctx.message.delete()
    await ctx.send('📋 **退勤報告**\n下のボタンを押してください', view=TaikinView())


bot.run(TOKEN)
