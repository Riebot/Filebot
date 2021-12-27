#(©)Codexbotz

import asyncio
import base64

from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>👑 Owner : <a href='tg://user?id={OWNER_ID}'>ɴᴇᴇᴅ ɴᴀᴍᴇ</a>\n🎬 Channel : <a href='https://t.me/kosmantap_reborn'>Kos Mantap Reborn</a>\n☕ Managed by : <a href='https://t.me/SilenceSpe4ks'>Klik Disini</a></b>\n",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("❌ 𝗧𝘂𝘁𝘂𝗽 ❌", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except BaseException:
            pass
