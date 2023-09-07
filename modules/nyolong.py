# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Pinterest**

๏ **Perintah:** `copy` <link>
◉ **Keterangan:** Colong media dari ch private.

๏ **Perintah:** `curi` <balas pesan>
◉ **Keterangan:** Curi pap timer.
"""

import os
import re
import time
import asyncio
from datetime import datetime
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from . import LOGS, time_formatter, downloader, random_string
from telethon.errors.rpcerrorlist import ChatForwardsRestrictedError, UserBotError, MediaEmptyError
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.functions.channels import (
    GetAdminedPublicChannelsRequest,
    InviteToChannelRequest,
    LeaveChannelRequest,
)
from telethon.tl.functions.contacts import GetBlockedRequest
from telethon.tl.functions.messages import AddChatUserRequest, GetAllStickersRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    Channel,
    Chat,
    InputMediaPoll,
    Poll,
    PollAnswer,
    TLObject,
    User,
)
from telethon.utils import get_peer_id
try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None

from . import *
LOG_CHANNEL = udB.get_key("LOG_CHANNEL")


# Source: https://github.com/UsergeTeam/Userge/blob/7eef3d2bec25caa53e88144522101819cb6cb649/userge/plugins/misc/download.py#L76
REGEXA = r"^(?:(?:https|tg):\/\/)?(?:www\.)?(?:t\.me\/|openmessage\?)(?:(?:c\/(\d+))|(\w+)|(?:user_id\=(\d+)))(?:\/|&message_id\=)(\d+)(?:\?single)?$"
DL_DIR = "resources/downloads"


def rnd_filename(path):
    if not os.path.exists(path):
        return path
    spl = os.path.splitext(path)
    rnd = "_" + random_string(5).lower() + "_"
    return spl[0] + rnd + spl[1]




@ayra_cmd(pattern="copy(?: |$)(.*)")
async def copy(e):
    ghomst = await e.eor("`checking...`")
    args = e.pattern_match.group(1)
    if not args:
        reply = await e.get_reply_message()
        if reply and reply.text:
            args = reply.message
        else:
            return await eod(ghomst, "Give a tg link to download", time=10)
    
    remgx = re.findall(REGEXA, args)
    if not remgx:
        return await ghomst.edit("`probably a invalid Link !?`")

    try:
        chat, id = [i for i in remgx[0] if i]
        channel = int(chat) if chat.isdigit() else chat
        msg_id = int(id)
    except Exception as ex:
        return await ghomst.edit("`Give a valid tg link to proceed`")

    try:
        msg = await e.client.get_messages(channel, ids=msg_id)
    except Exception as ex:
        return await ghomst.edit(f"**Error:**  `{ex}`")

    start_ = datetime.now()
    if (msg and msg.media) and hasattr(msg.media, "photo"):
        dls = await e.client.download_media(msg, DL_DIR)
    elif (msg and msg.media) and hasattr(msg.media, "document"):
        fn = msg.file.name or f"{channel}_{msg_id}{msg.file.ext}"
        filename = rnd_filename(os.path.join(DL_DIR, fn))
        try:
            dlx = await downloader(
                filename,
                msg.document,
                ghomst,
                time.time(),
                f"Downloading {filename}...",
            )
            dls = dlx.name
        except MessageNotModifiedError as err:
            LOGS.exception(err)
            return await xx.edit(str(err))
    else:
        return await ghomst.edit("`Message doesn't contain any media to download.`")

    end_ = datetime.now()
    ts = time_formatter(((end_ - start_).seconds) * 1000)
    await ghomst.edit(f"**Downloaded in {ts} !!**\n » `{dls}`")

@ayra_cmd(pattern=r"curi(?: |$)(.*)")
async def pencuri(event):
    dia = await event.get_reply_message()
    botlog = LOG_CHANNEL
    xx = await event.eor("`...`", time=2)
    if not dia:
        return
    anjing = dia.text or None
    pap = await event.client.download_media(dia)
    try:
        await event.client.send_file(
             botlog,
             pap,
             caption="Pap nya...")
    except Exception as e:
        print(e)
