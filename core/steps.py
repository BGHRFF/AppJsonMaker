# (c) @AbirHasan2005

import os
import json
import inflect as __inflect
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file
from core.fix import FixEnvData

inflect = __inflect.engine()
ikeyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Cancel Process", callback_data="cancelProcess")]]
)


async def StartSteps(bot: Client, editable: Message):
    heroku_app = {
        "name": "",
        "logo": "",
        "description": "",
        "keywords": list(),
        "repository": "",
        "website": "",
        "success_url": "",
        "env": dict(),
        "stack": "",
        "buildpacks": list(),
        "formation": dict(),
    }
    ## --- Step 1 --- ##
    await editable.edit(
        "**Addım 1:**\n" "Heroku proqram adınızı bizə göndərin.", reply_markup=ikeyboard
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    if input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    heroku_app["name"] = input_m.text
    await input_m.delete(True)
    ## --- Step 2 --- ##
    await editable.edit(
        "**Addım 2:**\n"
        "İndi mənə Heroku Tətbiq Təsvirinizi göndərin.\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["description"] = input_m.text
    if input_m.text.startswith("/skip"):
        del heroku_app["description"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    await input_m.delete(True)
    ## --- Step 3 --- ##
    await editable.edit(
        "**Addım 3:**\n"
        "İndi mənə Heroku Tətbiq Açar sözlərinizi göndərin.\n"
        "Vergüldən istifadə edərək ayırın(`,`)\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["keywords"] = input_m.text.replace(" ", "").split(",")
    if input_m.text.startswith("/skip"):
        del heroku_app["keywords"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    await input_m.delete(True)
    ## --- Step 4 --- ##
    await editable.edit(
        "**Addım 4:**\n" "İndi mənə GitHub Repository Linkinizi göndərin.",
        reply_markup=ikeyboard,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["repository"] = input_m.text
    if input_m.text.startswith("/skip"):
        del heroku_app["repository"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    await input_m.delete(True)
    ## --- Step 5 --- ##
    await editable.edit(
        "**Addım 5:**\n"
        "İndi isə mənə vebsayt linkinizi göndərin.\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["website"] = input_m.text
    if input_m.text.startswith("/skip"):
        del heroku_app["website"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    await input_m.delete(True)
    ## --- Step 6 --- ##
    await editable.edit(
        "**Addım 6:**\n"
        "İndi mənə Uğurlu URL-nizi göndərin.\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    heroku_app["success_url"] = input_m.text
    if input_m.text.startswith("/skip"):
        del heroku_app["success_url"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    await input_m.delete(True)
    ## --- Step 7 --- ##
    await editable.edit(
        "**Addım 7:**\n"
        "İndi ENV konfiqurasiyalarının vaxtıdır!\n\n"
        "Əgər hazırdırsa /done\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
    )
    env_inputs_running = True
    env_count = 1
    while env_inputs_running:
        _cache_m = await editable.reply_text(
            f"Mənə göndərin {inflect.ordinal(env_count)} ENV adı & dəyəri.\n\n"
            "**Qeyd:** __boşluq olmadan ENV adı və\n"
            "(__`:`__) təsviri, dəyəri, tələb olunan, generatoru müəyyən etmək üçün istifadə edin.__"
        )
        input_m: Message = await bot.listen(editable.chat.id, timeout=600)
        if input_m.text.startswith("/skip"):
            del heroku_app["env"]
            env_inputs_running = False
            await _cache_m.delete(True)
            continue
        elif input_m.text.startswith("/done"):
            env_inputs_running = False
            await _cache_m.delete(True)
            continue
        elif input_m.text.startswith("/"):
            return await input_m.continue_propagation()
        input_str = input_m.text.split(":", 5)
        env_count += 1
        if len(input_str) < 5:
            while len(input_str) < 5:
                input_str.append("")
        input_str = await FixEnvData(input_str)
        heroku_app["env"][f"{input_str[0].upper()}"] = {
            "description": f"{input_str[1]}",
            "required": f"{input_str[3]}",
        }
        if input_str[2] != "":
            heroku_app["env"][f"{input_str[0].upper()}"]["value"] = f"{input_str[2]}"
        if input_str[4] != "":
            heroku_app["env"][f"{input_str[0].upper()}"][
                "generator"
            ] = f"{input_str[4]}"
        await input_m.delete(True)
        await _cache_m.delete(True)
    ## --- Step 8 --- ##
    await editable.edit(
        "**Addım 8:**\n"
        "İndi isə Heroku adını göndrəin [Buildpacks](https://telegra.ph/Heroku-Default-Buildpacks-09-27) list.\n"
        "Bununla ayırın (`|`)\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
        disable_web_page_preview=True,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    input_buildpacks = input_m.text.split("|")
    for i in range(len(input_buildpacks)):
        heroku_app["buildpacks"].append({"url": f"{input_buildpacks[i]}"})
    if input_m.text.startswith("/skip"):
        del heroku_app["buildpacks"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    await input_m.delete(True)
    ## --- Step 9 --- ##
    await editable.edit(
        "**Addım 9:**\n"
        "Hansı proses növü?\n"
        "Göndərin [`web`] vəya [`worker`]\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    if input_m.text.startswith("/skip"):
        pass
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    process_type = input_m.text.lower().strip()
    if process_type not in ["web", "worker"]:
        process_type = "worker"
    heroku_app["formation"][f"{process_type}"] = {}
    await input_m.delete(True)
    ## --- Step 10 --- ##
    await editable.edit(
        "**Addım 10:**\n"
        "Dyno Type nə olacaq?\n"
        "Göndərin [`free`] vəya [`hobby`] vəya [`standard-1x`] vəya "
        "[`standard-2x`] vəya [`performance-m`] vəya [`performance-l`]\n\n"
        "[Official Documentation](https://devcenter.heroku.com/articles/dyno-types)\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
        disable_web_page_preview=True,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    if input_m.text.startswith("/skip"):
        pass
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    dyno_type = input_m.text.lower()
    if dyno_type not in [
        "free",
        "hobby",
        "standard-1x",
        "standard-2x",
        "performance-m",
        "performance-l",
    ]:
        dyno_type = "free"
    heroku_app["formation"][f"{process_type}"] = {"quantity": 1, "size": f"{dyno_type}"}
    await input_m.delete(True)
    ## --- Step 11 --- ##
    await editable.edit(
        "**Addım 11:**\n"
        "Heroku Tətbiqiniz üçün JPG formatında mənə Loqo göndərin.\n\n"
        "Bu addımı keçmək üçün /skip",
        reply_markup=ikeyboard,
        disable_web_page_preview=True,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    if input_m.text and input_m.text.startswith("/skip"):
        del heroku_app["logo"]
    elif input_m.text and input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    elif input_m.photo:
        await editable.edit("Processing Logo ...")
        logo_jpg = await bot.download_media(
            input_m,
            file_name=f"./downloads/logo/{str(editable.chat.id)}/{str(editable.message_id)}/",
        )
        resp = upload_file(logo_jpg)
        logo_jpg = f"https://telegra.ph/{resp[0]}"
        heroku_app["logo"] = logo_jpg
    else:
        del heroku_app["logo"]
    await input_m.delete(True)
    ## --- Step 11 --- ##
    await editable.edit(
        "**Addım 12:**\n"
        "Mənı [Heroku Stack](https://devcenter.heroku.com/articles/stack) səviyyəsini göndərin.\n"
        "Buradan: [`container`, `heroku-20`, `heroku-18`, `heroku-16`]",
        reply_markup=ikeyboard,
        disable_web_page_preview=True,
    )
    input_m: Message = await bot.listen(editable.chat.id, timeout=600)
    if input_m.text.startswith("/skip"):
        del heroku_app["stack"]
    elif input_m.text.startswith("/"):
        return await input_m.continue_propagation()
    else:
        heroku_stack_level = input_m.text.lower().strip()
        if heroku_stack_level not in [
            "container",
            "heroku-20",
            "heroku-18",
            "heroku-16",
        ]:
            heroku_stack_level = "heroku-20"
        heroku_app["stack"] = heroku_stack_level
    await input_m.delete(True)
    ## --- Make --- ##
    await editable.edit("Hazırlanır `app.json` ...")
    app_json_f = os.path.join("downloads", str(editable.chat.id), str(editable.message_id))
    if not os.path.exists(app_json_f):
        os.makedirs(app_json_f)
    app_json = os.path.join(app_json_f, "app.json")
    js = json.dumps(heroku_app, indent=4, separators=(",", ": "))
    with open(app_json, "w+") as f:
        f.write(js)
    return app_json
