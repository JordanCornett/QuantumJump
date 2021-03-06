import re

import aiohttp
from bs4 import BeautifulSoup as bs4

from lib.cog import Cog, event
from lib.objects import Message


class Autourl(Cog):
    @event("room::message")
    async def message(self, message: Message):
        msg = message.message
        match = re.findall(self.settings["pattern"], msg)
        # workaround for youtube playing
        if re.match(r"\A.?yt", msg) or message.handle == self.bot_settings.nickname:
            pass
        elif msg.startswith(self.settings["exclusion_char"]) or len(match) == 0:
            pass
        else:
            if self.ignore_msg(match[0]) is False:
                title = await self.get_title(match[0])
                if title:
                    await self.send_message(f"[ {title} ]")

    def ignore_msg(self, msg: str):
        for each in self.settings["ignores"]:
            if re.search(each, msg):
                return True
            else:
                return False

    def iswhitelisted(self, url: str) -> bool:
        if self.settings["whitelist_mode"]:
            for possible in self.settings["whitelist"]:
                if re.search(possible, url):
                    return True

    async def get_title(self, url: str):
        url = url.strip()
        connector = None
        # TODO allow exclusive whitelist mode
        if self.settings["use_tor"] and not self.iswhitelisted(url):
            try:
                from aiohttp_socks import SocksConnector
                connector = SocksConnector.from_url(
                    self.settings["tor_addr"])
            except ImportError:
                raise ImportError
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = bs4(text, "html.parser")
                    if soup is not None:
                        try:
                            title = soup.title.string
                        except AttributeError as error:
                            pass
                        else:
                            return title.strip()
