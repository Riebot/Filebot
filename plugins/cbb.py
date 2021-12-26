#(©)Codexbotz


from bot import Bot
from config import CHANNEL, GROUP, OWNER, OWNER_ID
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=f"<b>Info Bot :\n\n 👑 Owner: @{OWNER}\n 🎬 Channel: @{CHANNEL}\n ☕ Managed by : <a href='https://t.me/SilenceSpe4ks'>Klik Disini</a></b>\n",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ 𝐓𝐔𝐓𝐔𝐏 ❌", callback_data="close")]]
            ),
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except BaseException:
            pass
