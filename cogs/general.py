import os
import nextcord
import yaml
import DnD4py as dnd
from nextcord.ext import commands
from nextcord.ui import Button, View
import subprocess
import re
from pathlib import Path
import json
import requests

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

    def generate_embed(self, res, index, max_index):
        embed = nextcord.Embed(
            title=res["results"][index]["name"],
            color=config["success"]
        )
        for key in res["results"][index]:
            if key in ["name", "document_slug", "document_title", "route", "slug", "highlighted"]:
                continue
            value = res["results"][index][key]
            if len(value) == 0:
                continue
            if len(value) > 1000:
                value = value[:1000] + "..."
            embed.add_field(
                name=key,
                value=value,
                inline=False
            )
        embed.set_footer(
            text=f"{index+1}/{max_index}"
        )
        return embed

    @commands.command(name="search")
    async def search(self, context, *query):
        """
        Search the 5e SRD
        """
        terms = " ".join(query)
        res = json.loads(requests.get(f"https://api.open5e.com/search/?text={terms}").text)
        count = res["count"]
        self.currIndex = 0

        for index, r in enumerate(res["results"]):
            if r["name"].lower() == terms.lower():
                self.currIndex = index
                break

        embed = self.generate_embed(res, self.currIndex, count)
        previous_button = Button(label="<", style=nextcord.ButtonStyle.red)

        async def previous_callback(interaction):
            # edit the embed to show the previous result
            currEmbed = interaction.message.embeds[0].to_dict()
            index = int(currEmbed["footer"]["text"].split("/")[0]) - 1
            if (index + 1) < 0:
                index = count - 1
            else:
                index = index - 1
            newembed = self.generate_embed(res, index, count)
            await interaction.message.edit(embed=newembed)
        
        next_button = Button(label=">", style=nextcord.ButtonStyle.red)

        async def next_callback(interaction):
            # edit the embed to show the previous result
            currEmbed = interaction.message.embeds[0].to_dict()
            index = int(currEmbed["footer"]["text"].split("/")[0]) - 1
            if (index + 1) >= count:
                index = 0
            else:
                index = index + 1
            newembed = self.generate_embed(res, index, count)
            await interaction.message.edit(embed=newembed)
        
        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view = View(timeout=1000)
        view.add_item(previous_button)
        view.add_item(next_button)

        await context.send(embed=embed, view=view)




def setup(bot):
    bot.add_cog(general(bot))
