# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Chatbot**

๏ **Perintah:** `ai` <berikan pertanyaan>
◉ **Keterangan:** Sangat berguna untuk kebutuhan.

๏ **Perintah:** `img` <query>
◉ **Keterangan:** Mencari gambar menggunakan ai.
"""
import requests


from . import LOGS, ayra_cmd, eod, inline_mention, udB
from .database.ai import OpenAi, get_chatbot_reply

async def chatgpt(text) -> str:
    url = "https://api.safone.me/chatgpt"
    payloads = {
        "message": text,
        "chat_mode": "assistant",
        "dialog_messages": "[{'bot': '', 'user': ''}]"
    }
    rsp = None
    try:
        response = requests.post(
            f"{url}",
            json=payloads,
            headers={"Content-Type": "application/json"}
        ).json()
        if not (response and "message" in response):
            rsp = "Invalid Response from Server"
        else:
            rsp = response.get("message")
    except BaseException as excp:
        rsp = f"Error: {excp}"

    return rsp


@ayra_cmd(pattern="(ai|ask)( (.*)|$)")
async def chatgpt_support(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await event.edit(
            "`Mohon berikan permintaan!`"
        )
        return

    x = await event.edit("`Memproses...`")
    rsp = await chatgpt(msg)

    if rsp:
        await x.edit(rsp)
    else:
        await x.edit("ChatGPT tidak ada merespon.")

    

@ayra_cmd(pattern="img( (.*)|$)")
async def imge(event):
    question = event.pattern_match.group(2)
    if not question:
        await event.eor("`Mohon berikan pertanyaan untuk menggunakan AI.`")
        return
    msg = await event.eor("`Processing...`")
    try:
        response = OpenAi().photo(question)
        await event.client.send_file(
            event.chat_id, file=response, reply_to=event.message.id
        )
        await msg.delete()
    except Exception as error:
        await event.eor(str(error))


@ayra_cmd(pattern="repai")
async def im_lonely_chat_with_me(event):
    if event.reply_to:
        message = (await event.get_reply_message()).message
    else:
        try:
            message = event.text.split(" ", 1)[1]
        except IndexError:
            return await eod(
                event, "Balas ke pesan pengguna atau beri saya id/username", time=10
            )
    reply_ = await get_chatbot_reply(message=message)
    await event.eor(reply_)


@ayra_cmd(pattern="addai")
async def add_chatBot(event):
    await chat_bot_fn(event, type_="add")


@ayra_cmd(pattern="remai")
async def rem_chatBot(event):
    await chat_bot_fn(event, type_="remov")


@ayra_cmd(pattern="listai")
async def lister(event):
    key = udB.get_key("CHATBOT_USERS") or {}
    users = key.get(event.chat_id, [])
    if not users:
        return await event.eor("`Belum ada pengguna yang ditambahkan AI.`", time=5)
    msg = "**Daftar Total Pengguna yang Diaktifkan AI Dalam Obrolan Ini :**\n\n"
    for i in users:
        try:
            user = await event.client.get_entity(int(i))
            user = inline_mention(user)
        except BaseException:
            user = f"`{i}`"
        msg += f"• {user}\n"
    await event.eor(msg, link_preview=False)


async def chat_bot_fn(event, type_):
    if event.reply_to:
        user_ = (await event.get_reply_message()).sender
    else:
        temp = event.text.split(maxsplit=1)
        try:
            user_ = await event.client.get_entity(await event.client.parse_id(temp[1]))
        except BaseException as er:
            LOGS.exception(er)
            user_ = event.chat if event.is_private else None
    if not user_:
        return await eod(
            event,
            "Balas ke pesan pengguna atau beri saya id/username untuk menambahkan ChatBot AI!",
        )
    key = udB.get_key("CHATBOT_USERS") or {}
    chat = event.chat_id
    user = user_.id
    if type_ == "add":
        if key.get(chat):
            if user not in key[chat]:
                key[chat].append(user)
        else:
            key.update({chat: [user]})
            await event.eor(f"**Ditambahkan untuk CHATBOT:**\n{inline_mention(user_)}")
    elif type_ == "remov":
        if key.get(chat):
            if user in key[chat]:
                key[chat].remove(user)
            if chat in key and not key[chat]:
                del key[chat]
                await event.eor(f"**Dihapus untuk CHATBOT:**\n{inline_mention(user_)}")
    udB.set_key("CHATBOT_USERS", key)
