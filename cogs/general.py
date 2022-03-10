import os
import nextcord
import yaml
import DnD4py as dnd
from nextcord.ext import commands
from nextcord.ui import Button, View
import subprocess
import re
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

if "DnDBot" not in str(os.getcwd()):
    os.chdir("./DnDBot")
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

    def remove_tags(self, text):
        cleantext = re.sub(CLEANR, '', text)
        return cleantext

    @commands.command(name="search")
    async def search(self, context, *query):
        """
        Check if the bot is alive.
        """
        try:
            terms = " ".join(query)
            res = self.remove_tags(subprocess.check_output(f"lookup5e {terms}", universal_newlines=True)[:1000])
        except:
            res = "Not found"

        embed = nextcord.Embed(
            color=config["success"]
        )
        embed.add_field(
            name="Result",
            value=res,
            inline=True
        )
        embed.set_footer(
            text=f"Searched by: {context.message.author}"
        )

        await context.send(embed=embed)
    




def setup(bot):
    bot.add_cog(general(bot))
