from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

class Notify(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.notifier.start()
		self.channel = None

	def cog_unload(self):
		self.notifier.cancel()

	@tasks.loop(seconds=1.0)
	async def notifier(self):
		now = datetime.now(pytz.timezone('Asia/Tokyo'))
		if self.channel:
			await self.channel.send(
				f"現在、{now.strftime('%Y/%m/%d %H:%M:%S')}です")

	@commands.command()
	async def set_notify_channel(self, ctx):
		self.channel = ctx.channel
		await ctx.send(f" 「{ctx.channel.name}」に時報を通知します！")

def setup(bot):
	bot.add_cog(Notify(bot))