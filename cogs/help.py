import os
import sys

import nextcord
import yaml
from nextcord.ext import commands

if "DaddyBot" not in str(os.getcwd()):
    os.chdir("./DaddyBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Help(commands.Cog, name="helpmedaddy"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helpmedaddy")
    async def helpmedaddy(self, context):
        """
        List all commands from every Cog the bot has loaded.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = nextcord.Embed(title="Help", description="List of available commands:", color=config["success"])
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            print(i)
            if i not in ["owner", "template"]:
                commands = cog.get_commands()
                command_list = [command.name for command in commands]
                command_description = [command.help for command in commands]
                help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
                embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
