from discord.ext import commands 
import discord 
import asyncio

class Greet(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def hello(self, ctx):
		def check_message_author(msg):
			return msg.author == ctx.author

		await ctx.send(f"こんにちは、{ctx.author.name}さん！！")
		await ctx.send("気分はどうかな？")

		msg = await self.bot.wait_for('message' , check=check_message_author)
		await ctx.send(f" 「{msg.content}」という気分なんだね！！！")

def setup(bot):
	bot.add_cog(Greet(bot))