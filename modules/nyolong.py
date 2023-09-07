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
import glob 
import asyncio
import io
import random
import time 
import os
import re
import asyncio

from . import (
    LOGS,
    downloader,
    eor,
    fast_download,
    get_all_files,
    get_string,
    time_formatter,
    ayra_cmd,
    set_attributes,
)

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

@ayra_cmd(
    pattern="ul( (.*)|$)",
)
async def _(event):
    msg = await event.eor(get_string("com_1"))
    match = event.pattern_match.group(1)
    if match:
        match = match.strip()
    if not event.out and match == ".env":
        return await event.reply("`You can't do this...`")
    stream, force_doc, delete = (
        False,
        True,
        False,
    )
    if "--stream" in match:
        stream = True
        force_doc = False
    if "--delete" in match:
        delete = True
    arguments = ["--stream", "--delete"]
    if any(item in match for item in arguments):
        match = (
            match.replace("--stream", "")
            .replace("--delete", "")
            .strip()
        )
    if match.endswith("/"):
        match += "*"
    results = glob.glob(match)
    if not results and os.path.exists(match):
        results = [match]
    if not results:
        try:
            await event.reply(file=match)
            return await event.try_delete()
        except Exception as er:
            LOGS.exception(er)
        return await msg.eor(get_string("ls1"))
    for result in results:
        if os.path.isdir(result):
            c, s = 0, 0
            for files in get_all_files(result):
                attributes = None
                if stream:
                    try:
                        attributes = await set_attributes(files)
                    except KeyError as er:
                        LOGS.exception(er)
                try:
                    file, _ = await event.client.fast_uploader(
                        files, show_progress=True, event=msg, to_delete=delete
                    )
                    await event.client.send_file(
                        event.chat_id,
                        file,
#                       supports_streamin=stream,
#                       force_document=force_doc,
#                       thumb=None,
#                       attributes=attributes,
                        caption=f"",
                        reply_to=event.reply_to_msg_id or event,
                    )
                    s += 1
                except (ValueError, IsADirectoryError):
                    c += 1
            break
        attributes = None
        if stream:
            try:
                attributes = await set_attributes(result)
            except KeyError as er:
                LOGS.exception(er)
        file, _ = await event.client.fast_uploader(
            result, show_progress=True, event=msg, to_delete=delete
        )
        await event.client.send_file(
            event.chat_id,
            file,
#            supports_streaming=stream,
#            thumb=None,
#            force_document=force_doc,
#            attributes=attributes,
            caption=f"",
        )
    await msg.try_delete()
