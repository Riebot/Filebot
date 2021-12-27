#(©)Codexbotz

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


from bot import Bot
from config import ADMINS, START_MSG, OWNER_ID, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON
from database.sql import add_user, full_userbase, query_msg
from helper_func import decode, get_messages, subscribed

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("<code>Tunggu Sebentar...</code>")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("<b>Sedang Mengalami Kendala...</b>")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
               [
                    InlineKeyboardButton("📑 ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ", callback_data = "about"),
                    InlineKeyboardButton("ᴛᴜᴛᴜᴘ ❌", callback_data = "close"),
               ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None
                if not message.from_user.username
                else "@" + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True,
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    text = "<b>Kamu harus join atau bergabung ke channel terlebih dahulu agar bisa menonton videonya! Klik Disini jika sudah join dan Coba Lagi\n\njoin Channel Atau Group</b>"
    message_text = message.text
    try:
        command, argument = message_text.split()
        text = text + f"<b>Dan <a href='https://t.me/{client.username}?start={message.command[1]}'>Coba Lagi</a></b>"
    except ValueError:
        pass
    reply_markup = InlineKeyboardMarkup(
            [
                   InlineKeyboardButton("• ᴋʟɪᴋ ᴅɪsɪɴɪ •", url= client.invitelink),
                   InlineKeyboardButton("• ᴄᴏʙᴀ ʟᴀɢɪ •", url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ]
        )
        await message.reply(
        text = text,
        reply_markup = reply_markup,
        quote = True,
        disable_web_page_preview = True
    )
