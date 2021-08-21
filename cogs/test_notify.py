from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

mention = None

class Notify(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.notifier.start()
		self.channel = None

	def cog_unload(self):
		self.notifier.cancel()

	@tasks.loop(hours=0.5)
	async def notifier(self):
		now = datetime.now().strftime('%A:%H:%M')
		if self.channel:
			await self.channel.send(f"現在{now}です。テスト成功。")
		

	@commands.command()
	async def test_notify(self, ctx):
		Guild = ctx.guild
		self.channel = ctx.channel
		await ctx.send(f"「{ctx.channel.name}」にてテストを行います！")

def setup(bot):
	bot.add_cog(Notify(bot))