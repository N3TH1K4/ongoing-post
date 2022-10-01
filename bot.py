from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.raw import functions, types
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
import asyncio
from pyrogram.errors import FloodWait
import config as c
from pyromod import listen
import queriestest as q
import requests
import os

app = Client("an", bot_token=c.BOT_TOKEN, api_id=c.API_ID, api_hash=c.API_HASH)

def shorten(description, info='anilist.co'):
    description = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        description += f'_{description}_[Read More]({info})'
    else:
        description += f"_{description}_"
    return description

def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]

url = 'https://graphql.anilist.co'

@app.on_message(filters.command("new"))
async def post_thing(client, message: Message):
    user_id = message.chat.id
    if message.reply_to_message:
        chaid = message.reply_to_message.forward_from_chat.id
    else:
        channel_id_msg = await app.ask(user_id, 'Please Add Me To The Channel And Send The `Channel ID`')
        channel_id = int(channel_id_msg.text)
    #print(channel_id)
        chaid = channel_id
    search_msg = await app.ask(user_id, 'Send The Name OF The anime')
    search = search_msg.text
    if len(search)<1:
        await app.send_message(user_id,"Oi Send a name and send /new again")
        return
    variables = {'search': search}
    json = requests.post(url,json={
        'query': q.anime_query,
        'variables': variables}).json()
    search = search.replace('','_')
    json = json['data']['Media']
    titleen = json['title']['english']
    titleja = json['title']['romaji']
    score = json['averageScore']
    surl = json['siteUrl']
    tyype=json['format']
    idm = json.get("id")
    dura = json['duration']
    duration = f"{dura}  Minutes Per Ep."
    cover = json['coverImage']['extraLarge']
    genres = ""
    for x in json['genres']:
            genres += f"{x}, "
    genres = genres[:-2]
    genres = genres.replace("Action", "👊Action").replace("Adventure", "🏕Adventure").replace("Comedy", "😂Comedy").replace("Drama", "💃Drama").replace("Ecchi", "😘Ecchi").replace("Fantasy", "🧚🏻‍♂️Fantasy").replace("Hentai", "🔞Hentai").replace("Horror", "👻Horror").replace("Mahou Shoujo", "🧙Mahou Shoujo").replace("Mecha", "🚀Mecha").replace("Music", "🎸Music").replace("Mystery", "🔎Mystery").replace("Psychological", "😵‍💫Psychological").replace("Romance", "❤️Romance").replace("Sci-Fi", "🤖Sci-Fi").replace("Slice of Life", "🍃Slice of Life").replace("Sports", "⚽️Sports").replace("Supernatural", "⚡️Supernatural").replace("Thriller", "😳Thriller")                                                                       
    invitel = await app.export_chat_invite_link(chaid)
    title_img = f"https://img.anili.st/media/{idm}"
    main_reply =f"""
**{titleen}** | `{titleja}` [{tyype}]

**Score:** ⭐️ {score} [Anilist]({surl})
**Duration:** {duration}
**Genres:** {genres}

© Managed By Otaku™ Network
"""
    final_reply =f"""
**{titleen}** | `{titleja}` [{tyype}]

**Score:** ⭐️ {score} [Anilist]({surl})
**Duration:** {duration}
**Genres:** {genres}

Powered By: **@Otaku_Network**
"""
    link = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="> Link <",
                        url=f"{invitel}",
                    )
                    ]])
    down = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="Download",
                        url=f"{invitel}",
                    )
                    ]])
    #print(invitel)
    response = requests.get(f"{cover}")
    file = open("image.jpg", "wb")
    file.write(response.content)
    photo = "image.jpg"
    title = f"{titleen} | {titleja}"
    await app.send_message(user_id,"Preview")
    await app.send_photo(user_id,photo=title_img,caption=final_reply,reply_markup=link)
    await app.send_photo(user_id,photo=cover,caption="Use This as the thumbnail and I'm Gonna Add this as the channel pic!")
    asks_msg = await app.ask(user_id, 'Should I send This? Then send **OK**\nIf you want to cancel send **NO**')
    asks = asks_msg.text
    if "ok" in asks or "OK" in asks or "Ok" in asks:   
        await app.send_photo(chaid,photo=title_img,caption=final_reply,reply_markup=link)
        await client.set_chat_photo(
            chat_id=chaid,
            photo=photo
        )
        await client.set_chat_title(
            chat_id=chaid,
            title=title
        )
       # await app.set_chat_description(chaid, final_reply)
        os.remove("image.jpg")
        await app.send_message(user_id,"**Sucessfully Sent The Post!**\n**Chat Photo Added!**\n**Chat Title Updated!**")
        ma_msg = await app.ask(user_id, 'Should I send This To The Main Channel?\nThen send **OK**\nIf you want to cancel send **NO**')
        mai = ma_msg.text
        main_id = -1001595817253
        ongc = -1001715463451
        if "ok" in mai or "OK" in mai or "Ok" in mai:
            if user_id == 1813305809 or user_id == 1930645496 or user_id==5235061478:
                await app.send_photo(main_id,photo=title_img,caption=main_reply,reply_markup=down)
                await app.send_sticker(main_id,"CAACAgUAAxkBAAIEe2LPzdkbPBM5gZLxLfOZyPKe-rAzAAKZAAOpmuYWfOMe2DS8IdceBA")
                await app.send_message(user_id,"**Sucessfully Sent The Post to the main!**")
                onlink = await app.ask(user_id, f'send The link of the channel that {titleja} posted')
                onlink = onlink.text
                downon = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="Download",
                        url=f"{onlink}",
                    )
                    ]])
                await app.send_photo(ongc,photo=title_img,caption=main_reply,reply_markup=downon)
                await app.send_sticker(main_id,"CAACAgUAAxkBAAETDC9jN6noVjESqLaWbzMIyoUJDmoloAACRgADqZrmFrGJK8tGuhUQKgQ")
                await app.send_message(user_id,"**Sucessfully Sent The Post to the Ongoing!**")
            else:
                await app.send_message(user_id,"**You Are Not From @Otaku_network So you cant do this**")
                return
        elif "No" in asks or "NO" in asks or "no" in asks:
            await app.send_message(user_id,"Cancellin' The Process!")
            return
    elif "No" in asks or "NO" in asks or "no" in asks:
        await app.send_message(user_id,"Cancellin' The Process!")
        return
    else:
        await app.send_message(user_id,"Give a valid answer!")

        
@app.on_message(filters.command("start"))
async def strt(client, message: Message):
    user_id = message.chat.id
    link = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="> Ongoing Anime Net <",
                        url="https://t.me/OngoingAnimeNet",
                    )
                    ],
                 [
                    InlineKeyboardButton(
                        text="> Otaku Network <",
                        url="https://t.me/Otaku_network",
                    )
                    ]])
    img = "https://www.akibagamers.it/wp-content/uploads/2019/03/zombie-land-saga-tae-yamada.jpg"
    txt = "Hello! **My name is Sumi Sakurasawa** Am a girl who can send posts like posts in **@Otaku_networkt**\nJust Send /new or reply /new to a message that forwarded From the chat you want to send a post\n\n**Note**: You must add me as an `admin` in channel or group"
    await app.send_photo(user_id,photo=img,caption=txt,reply_markup=link)

    
app.run()
print("Bot Started Successfully\n")
