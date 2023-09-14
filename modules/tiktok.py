# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk sosmed**

๏ **Perintah:** `tiktok` <link>
◉ **Keterangan:** Unduh tautan tiktak.
"""
import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None

from . import *

@ayra_cmd(pattern="tt(?: |$)(.*)")
async def _(event):
    if xxnx := event.pattern_match.group(1):
        links = xxnx.split()  # Splitting the input into separate links
    elif event.is_reply:
        links = [await event.get_reply_message()]  # Storing the replied message as a single link
    else:
        return await eod(event, "Berikan link tautan tiktok...")

    xx = await eor(event, "Processing...")
    chat = "@downloader_tiktok_bot"
    async with event.client.conversation(chat) as conv:
        try:
            for link in links:  # Iterating over each link
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1332941342)
                )
                await event.client.send_message(chat, link)
                response = await response
                if response.text.startswith("Forward"):
                    await xx.edit("Mengunggah...")
                else:
                    await xx.delete()
                    await event.client.send_file(
                        event.chat_id,
                        response.message.media,
                        caption=f"Upload By: {inline_mention(event.sender)}",
                    )
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await event.client(DeleteHistoryRequest(peer=chat, max_id=0))
                    await xx.delete()
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            for link in links:  # Iterating over each link
                await event.client.send_message(chat, link)
                response = await response
                if response.text.startswith("Forward"):
                    await xx.edit("Mengunggah...")
                else:
                    await xx.delete()
                    await event.client.send_file(
                        event.chat_id,
                        response.message.media,
                        caption=f"Upload By: {inline_mention(event.sender)}",
                    )
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await event.client(DeleteHistoryRequest(peer=chat, max_id=0))
                    await xx.delete()
