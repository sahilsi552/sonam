
import asyncio
import os
import re

import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

from .. import QuantamBot as app
from aiohttp import ClientSession
aiohttpsession = ClientSession()

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")
import socket
from asyncio import get_running_loop
from functools import partial
import aiofiles


def paste(content):
    url ="https://pastebin.com/api/api_post.php"
    data = {"api_dev_key":"9Rfu50iV5l3EuRWATw7EDLuC37RED-C4","api_paste_code": content,"api_option": "paste"}
    response = requests.post(url, data=data)
    link=response.text
    return link
def paste2(content):
    url = 'https://dpaste.org/api/'
    payload = {'content': content.encode('utf-8'), 'format': 'url'}
    response = requests.post(url, data=payload)
    link2=response.text
    return link2
async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with aiohttpsession.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False

@app.on_message(filters.command("paste"))

async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message With /paste")
    m = await message.reply_text("Pasting...")
    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
    elif message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.file_size > 1048576:
            return await m.edit("You can only paste files smaller than 1MB.")
        if not pattern.search(document.mime_type):
            return await m.edit("Only text files can be pasted.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = paste(content)
    link2 = paste2(content)      
    button=InlineKeyboardMarkup([[(InlineKeyboardButton(text="• ᴘᴀsᴛᴇ ʟɪɴᴋ •", url=link))]])
   # button.add(InlineKeyboardButton("• ᴘᴀsᴛᴇ ʟɪɴᴋ 2 •", url=link2))
    try:
        await message.reply("ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴘᴀsᴛᴇ ʟɪɴᴋ :",reply_markup=button)
        await m.delete()     
    except Exception as e:
        await m.edit(f"{e} {link2}")
          


__MODULE__ = "Pᴀs​ᴛᴇ"
__HELP__ = """
 ᴘᴀsᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ғɪʟᴇ ᴀɴᴅ sʜᴏᴡs ʏᴏᴜ ᴛʜᴇ ʀᴇsᴜʟᴛ

 ❍ /paste  *:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ғɪʟᴇ
 """
