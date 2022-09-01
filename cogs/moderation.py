import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)

            if reason is not None:
                await ctx.send(f"{member} has been banned from the server for the reason \"{reason}\"")
                await member.send(f"You have been banned from {ctx.guild.name} for the reason \"{reason}\"")
            else:
                await ctx.send(f"{member} has been banned from the server!")
                await member.send(f"You have been banned from {ctx.guild.name} with no reason provided!")
        else:
            await ctx.send("Hey " + ctx.message.author.mention + ", you are missing required permissions for this command!")

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)

            if reason is not None:
                await ctx.send(f"{member} has been kicked from the server for the reason \"{reason}\"")
                await member.send(f"You have been kicked from {ctx.guild.name} for the reason \"{reason}\"")
            else:
                await ctx.send(f"{member} has been kicked from the server!")
                await member.send(f"You have been kicked from {ctx.guild.name} with no reason provided!")
        else:
            await ctx.send("Hey " + ctx.message.author.mention + ", you are missing required permissions for this command!")


def setup(client):
    client.add_cog(Moderation(client))
