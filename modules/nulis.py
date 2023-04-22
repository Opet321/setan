# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Nulis**

๏ **Perintah:** `nulis` <berikan pesan/balas pesan>
◉ **Keterangan:** Buat kamu yg males nulis.
"""

from telethon.errors import ChatSendMediaForbiddenError
import requests
from . import *


@ayra_cmd(pattern=r"(N|n)ulis( (.*)|$)")
async def handwrite(event):
    reply_msg = await event.get_reply_message()
    if reply_msg:
        text = reply_msg.text
    else:
        text = event.pattern_match.group(3)
    m = await event.reply("`Processing...`")
    req = requests.get(f"https://api.sdbots.tk/write?text={text}").url
    try:
        await event.client.send_file(event.chat.id, req, caption=f"Ditulis Oleh: {OWNER_NAME}")
    except ChatSendMediaForbiddenError:
        await m.edit("Dilarang mengirim media digrup ini 😥!")
        return
    await m.delete()