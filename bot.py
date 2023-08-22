from asyncio import sleep, create_task, get_event_loop
import logging
from pyrogram import Client, filters, idle
from pyrogram.enums import ChatType
from pyrogram.errors import YouBlockedUser, FloodWait
from pyrogram.handlers import MessageHandler, EditedMessageHandler
from pyrogram.utils import ainput


logging.getLogger("pyrogram").setLevel(logging.WARNING)

user = "modyvotlx"
user_bot = "eeobot"


async def join_chat(link, app):
    try:
        if '+' in link or 'joinchat' in link:
            await app.join_chat(link)
        else:
            await app.join_chat(link.replace('https://t.me/', ''))
    except FloodWait as e:
        await sleep(e.value)
    except Exception as e:
        print(e)


async def auto_start_in_bot(app):
    while not await sleep(180):
        if not app.stop:
            try:
                await app.send_message(user_bot, '/start')
            except YouBlockedUser:
                await app.unblock_user(user_bot)
                await sleep(0.4)
                await app.send_message(user_bot, '/start')


async def keko_tmwel_bots2(c, msg):
    points = int(msg.reply_markup.inline_keyboard[0][0].text.split(': ')[1])
    if points >= 100 and c.give_links:
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data='sendtocount'
            )
        except:
            pass
        await sleep(1)
        await msg.reply(points - 30)
    else:
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data='col'
            )
        except:
            pass
        await sleep(1)
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data='col3'
            )
        except:
            pass


async def keko_tmwel_bots3(c, msg):
    await join_chat(msg.reply_markup.inline_keyboard[0][0].url, c)
    await sleep(1)
    try:
        await c.request_callback_answer(
            chat_id=msg.chat.id,
            message_id=msg.id,
            callback_data=msg.reply_markup.inline_keyboard[1][0].callback_data
        )
    except:
        pass


async def keko_tmwel_bots4(c, msg):
    ay = False
    for lin in msg.text.split('\n'):
        if 't.me' in lin:
            ay = lin
            break
    if not ay:
        return
    link = 'http' + ay.split('http')[1]
    if ' ' in link:
        link = link.split(' ')[0]
    await join_chat(link, c)
    await sleep(1)
    await c.send_message(user_bot, '/start')


async def keko_tmwel_bots5(c, msg):
    ay = False
    for lin in msg.text.split('\n'):
        if 't.me' in lin:
            ay = lin
            break
    if not ay:
        return
    link = 'http' + ay.split('http')[1]
    try:
        await c.send_message(user, link)
    except:
        await sleep(1)
        c.give_links = False
        try:
            await c.request_callback_answer(
                chat_id=msg.chat.id,
                message_id=msg.id,
                callback_data=msg.reply_markup.inline_keyboard[0][0].callback_data
            )
        except:
            pass
        return
    await c.block_user(user_bot)
    c.stop = True
    async for dialog in c.get_dialogs():
        if dialog.chat.type != ChatType.PRIVATE:
            try:
                await c.leave_chat(dialog.chat.id, delete=True)
            except:
                pass
    await sleep(86400)
    c.stop = False


async def main():
    userbots = []
    n = 0
    while not await sleep(1):
        n += 1
        session = await ainput("session :\n")
        app = Client(f"user:{n}", 7720093, '51560d96d683932d1e68851e7f0fdea2', session_string=session)
        """
        if session == '' or not session or session is None:
            await app.authorize()
        if not await app.connect():
            print('error in connect')
            continue
        """
        try:
            await app.start()
        except Exception as e:
            print(e)
            continue
        app.stop = False
        app.give_links = True
        handlers_msg = {
            keko_tmwel_bots2: filters.user(user_bot) & filters.regex('والمجموعات عن طريق التجميع النقاط'),
            keko_tmwel_bots5: filters.user(user_bot) & filters.regex('ارسل الرابط للشخص المراد تحويل النقاط له'),
            keko_tmwel_bots4: filters.user(user_bot) & filters.regex('https'),
        }
        handlers_edit = {
            keko_tmwel_bots3: filters.user(user_bot) & filters.regex('اشترك في '),
        }
        for handler_func, handler_filters in handlers_msg.items():
            app.add_handler(MessageHandler(handler_func, handler_filters))
        for handler_func, handler_filters in handlers_edit.items():
            app.add_handler(EditedMessageHandler(handler_func, handler_filters))
        userbots.append(app)
        try:
            await app.send_message(user_bot, '/start')
        except YouBlockedUser:
            await app.unblock_user(user_bot)
            await sleep(0.4)
            await app.send_message(user_bot, '/start')
        create_task(auto_start_in_bot(app))
        print(f'[{app.me.id}] -start')
    await idle()
    for app2 in userbots:
        await app2.stop()


get_event_loop().run_until_complete(main())
