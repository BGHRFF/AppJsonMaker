

import os
from configs import Configs
from pyromod import listen
from asyncio import TimeoutError
from core.steps import StartSteps
from pyrogram import Client, filters, idle
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

app = Client(
    session_name=Configs.SESSION_NAME,
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN,
)


@app.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start_command(_, m: Message):
    await m.reply_text(
        "Salam mən heroku app.json düzəltmək üçün botam\n\n"
        "Heroku proqramınız üçün app.json faylını düzəltmək üçün,\n"
        "Basın /f",
        quote=True,
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("f") & ~filters.edited & filters.private)
async def f_command(bot: Client, m: Message):
    editable = await m.reply_text(
        "Please wait ...",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Prosesi ləğv edin", callback_data="cancelProcess")]]
        ),
    )
    try:
        app_json = await StartSteps(bot, editable)
        if os.path.exists(app_json):
            await bot.send_document(
                chat_id=m.chat.id,
                document=app_json,
                caption="**Made by @HerokuAppJson_Bot**",
            )
            await editable.edit(" `app.json` göndərildi !!")
            os.remove(app_json)
        else:
            await editable.edit(" `app.json` hazırlamaq mümkün olmadı !!\n\n" "Yenidən sınayın.")
    except TimeoutError:
        pass


@app.on_callback_query()
async def cb_handler(_, cb: CallbackQuery):
    if "cancelProcess" in cb.data:
        await cb.message.edit("Proses ləğv olundu!")


app.start()
print("Bot Başladıldı!")
idle()
app.stop()
print("Bot Dayandırıldı!")
