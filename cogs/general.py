import os
import random
import sys
import hmtai
import nextcord
import yaml
import glob
import pathlib
import requests
from nextcord.ext import commands
from nextcord.ui import Button, View


if "DaddyBot" not in str(os.getcwd()):
    os.chdir("./DaddyBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Check if the bot is alive.
        """
        embed = nextcord.Embed(
            color=config["success"]
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.set_footer(
            text=f"Pong request by {context.message.author}"
        )
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))
