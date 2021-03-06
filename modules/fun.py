# -*- coding: utf-8 -*-
#
# Copyright 2019, JohnnyCarcinogen ( https://github.com/JohnRipper/ ), All rights reserved.
#
# Created by dev at 2/8/20
# This file is part of QuantumJump.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import random

from lib.cog import Cog
from lib.command import Command, makeCommand


class Fun(Cog):
    def __init__(self, bot):
        super().__init__(bot)


    @makeCommand(aliases=["roll"], description="<sides> <dice>, default is single 6 sided")
    async def roll(self, c: Command):
        parts = c.message.split(" ")
        if len(c.message) == 0:
            await self.send_message(self.rolldice())
        elif len(parts) == 1 and c.message.isdigit():
            await self.send_message(self.rolldice(dice=int(c.message.strip())))
        elif parts[0].isdigit() and parts[1].isdigit():
            await self.send_message(
                self.rolldice(sides=int(parts[0]), dice=int(parts[1])))
        else:
            await self.send_message("I need numbers m8")

    def rolldice(self, sides=6, dice=1):
        if sides > 20 or dice > 15:
            msg = f"D&D dice only has 20 sides, wtf m8 and {dice} is way too many dice"
            return msg
        else:
            rolled = []
            total = 0
            faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            for die in range(dice):
                r = random.randint(1, sides)
                total += r
                if sides == 6 and self.settings["fancy_dice"]:
                    rolled.append(faces[r - 1])
                else:
                    rolled.append(str(r))
            msg = ":game_die: You roll {} for a total of {}".format(
                " ".join(rolled), total)
            return msg

    # TODO
    @makeCommand(aliases=["8ball"], description="<query> standard magic 8ball")
    async def eightball(self, c: Command):
        query = c.message
        if len(query) < 3:
            await self.send_message("You must ask a question.")
        else:
            # https://en.wikipedia.org/wiki/Magic_8-Ball#Possible_answers
            replies = [
                "It is certain.", "It is decidedly so.", "Without a doubt.",
                "Yes - definitely.", "You may rely on it.",
                "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                "Signs point to yes.", "Reply hazy, try again.",
                "Ask again later.", "Better not tell you now.",
                "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Very doubtful"
            ]
            custom = self.settings["8ballcustom"]
            # append custom replies if they exist
            if len(custom) > 0:
                replies.append([c for c in custom])
            msg = "{}".format(random.choice(replies))
            await self.send_message(msg)

    @makeCommand(aliases=["rate"], description="<user> rate someones appearance")
    async def rate(self, c: Command):
        rates = [
            "0/10", "1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10",
            "8/10", "9/10", "10/10"
        ]


        if not self.settings["allow_rate"]:
            msg = "I am the earth."
        elif len(c.message.strip()) == 0:
            msg = "I'd rate {} a {}".format(c.data.handle, random.choice(rates))
        elif c.message.startswith("my "):
            torate = c.message.lstrip("my ")
            msg = "I'd rate {}'s {} {}".format(c.data.handle, torate, random.choice(rates))
        else:
            msg = "I'd rate {} a {}".format(c.message, random.choice(rates))
        await self.send_message(msg)
