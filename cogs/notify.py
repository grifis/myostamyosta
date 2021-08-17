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

	@tasks.loop(seconds=60)
	async def notifier(self):
		now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
		if now == '22:20':
			if self.channel:
				await self.channel.send(f"{mention} 現在{now}です。テスト成功。")
		if now == '22:30':
			if self.channel:
				await self.channel.send(f"{mention} 現在{now}です。テスト成功")
		if now == '22:40':
			if self.channel:
				await self.channel.send(f"{mention} 現在{now}です。テスト成功")
		if now == '22:50':
			if self.channel:
				await self.channel.send(f"{mention} 現在{now}です。テスト成功")

	@commands.command()
	async def set_notify_channel(self, ctx):
		Guild = ctx.guild
		Role = Guild.get_role(877141493016580156)
		self.channel = ctx.channel
		global mention
		mention = Role.mention
		await ctx.send(f"{Role.mention} 「{ctx.channel.name}」にてテストを行います！")

def setup(bot):
	bot.add_cog(Notify(bot))