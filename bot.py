from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,CallbackQuery
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filterss.admin import IsBotAdminFilter
from filterss.check_sub_channel import IsCheckSubChannels
from keyboard_buttons import admin_keyboard,buttons
from aiogram.fsm.context import FSMContext
from middlewares.throttling import ThrottlingMiddleware #new
from states.reklama import Adverts
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time 
from aiogram.types import CallbackQuery
from val import to_sum


#sozlash
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()



#start komandasi uchun javob
@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id)
        await message.answer(text="Assalomu alaykum, botimizga xush kelibsiz!\nBotimiz orqali siz valyutalar narxini /valyuta kommandasi orqali bilib olishingiz mumkin\nValyuta ustiga bosing 👇👇👇",reply_markup=buttons.valyut)
    except:
        await message.answer(text="Assalomu alaykum!boyomizga xush kelibsiz foydalanish uchun\nValyuta ustiga bosing 👇👇👇",reply_markup=buttons.valyut)

    await message.delete()









#kanalga obuna bo'lishni tekshirish uchun
@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message:Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)

@dp.message(Command("help"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="bu valyuta kursi boti ")

@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.5)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.message(F.text=="Valyuta")
async def vayuta(message:Message):
    await message.answer(text="Valyuta tanlang!", reply_markup=buttons.currency)

# @dp.message(Command("valyuta"))
# async def button_answer(message: Message):
#     await message.answer(text="Valyuta tanlang!", reply_markup=buttons.currency)
#     await message.delete()
    
@dp.callback_query(F.data != 'back')
async def valyuta_answer(callback: CallbackQuery):
    await callback.message.answer(text=f"{to_sum(callback.data)}", reply_markup=buttons.back)
    await callback.message.delete()
    
@dp.callback_query(F.data == 'back')
async def valyuta_back(callback: CallbackQuery):
    await callback.message.answer(text="Valyuta tanlang!", reply_markup=buttons.currency)
    await callback.message.delete()



#bot ishga tushganini xabarini yuborish
@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)


#bot ishni yakunlaganining xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)


async def main() -> None:

    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    
    #malumotlar bazasini yaratish
    db = Database(path_to_db="users.db")

    #flood ni oldini olish
    dp.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))

    #foydalanuvchilar jadvalini yaratish
    db.create_table_users()

    #birlamchi komandalar
    await set_default_commands(bot)

    #botni ishga tushirish
    await dp.start_polling(bot)
    




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())