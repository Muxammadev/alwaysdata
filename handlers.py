from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards import confirm_menu, channel_menu
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from config import CHANNEL_ID
from aiogram import Router, F
from states import SendLogin
import asyncio

router = Router()
message_ids={}



#--> CMD <--#
@router.message(Command("muxa"))
async def state_1(m: Message, state: FSMContext):
    await m.delete()
    await state.clear()
    message = await m.answer("Bot:")
    message_ids[m.from_user.id] = message.message_id
    await state.set_state(SendLogin.bot)


# --> BOT <--#
@router.message(SendLogin.bot)
async def state_2(m: Message, state: FSMContext):
    await state.update_data(bot=m.text)
    await m.delete()
    await m.bot.edit_message_text(text="Email:", message_id=message_ids[m.from_user.id], chat_id=m.from_user.id)
    await state.set_state(SendLogin.email)


#--> EMAIL <--#
@router.message(SendLogin.email)
async def state_3(m: Message, state: FSMContext):
    await state.update_data(email=m.text)
    await m.delete()
    await m.bot.edit_message_text(text="Password:", message_id=message_ids[m.from_user.id], chat_id=m.from_user.id)
    await state.set_state(SendLogin.password)


#--> PASSWORD <--#
@router.message(SendLogin.password)
async def state_4(m: Message, state: FSMContext):
    await state.update_data(password=m.text)
    await m.delete()
    await m.bot.edit_message_text(text="SSH link:", message_id=message_ids[m.from_user.id], chat_id=m.from_user.id)
    await state.set_state(SendLogin.ssh_link)


#--> LINK <--#
@router.message(SendLogin.ssh_link)
async def state_5(m: Message, state: FSMContext):
    await state.update_data(ssh_link=m.text)
    await m.delete()
    await m.bot.edit_message_text(text="SSH login:", message_id=message_ids[m.from_user.id], chat_id=m.from_user.id)
    await state.set_state(SendLogin.ssh_login)


#--> LOGIN <--#
@router.message(SendLogin.ssh_login)
async def state_6(m: Message, state: FSMContext):
    await state.update_data(ssh_login=m.text)
    await m.delete()
    await m.bot.edit_message_text(text="SSH password:", message_id=message_ids[m.from_user.id], chat_id=m.from_user.id)
    await state.set_state(SendLogin.ssh_pass)


#--> SSH-PASSWORD <--#
@router.message(SendLogin.ssh_pass)
async def state_7(m: Message, state: FSMContext):
    await state.update_data(ssh_pass=m.text)
    user_data = await state.get_data()
    await m.delete()
    bot = user_data["bot"]
    email = user_data["email"]
    password = user_data["password"]
    ssh_link = user_data["ssh_link"]
    ssh_login = user_data["ssh_login"]
    ssh_pass = user_data["ssh_pass"]

    message = (
        f"<b>Bot:</b> {bot}\n"
        f"<b>Login:</b> <code>{email}</code>\n"
        f"<b>Parol:</b> <code>{password}</code>\n\n"
        f"<b>SSH:</b> {ssh_link}\n"
        f"<b>Login:</b> <code>{ssh_login}</code>\n"
        f"<b>Parol:</b> <code>{ssh_pass}</code>"
    )
    await m.bot.edit_message_text(text=message,
                                  message_id=message_ids[m.from_user.id],
                                  chat_id=m.from_user.id,
                                  reply_markup=confirm_menu())
    await state.set_state(SendLogin.confirm)

@router.callback_query(F.data == "HA" or F.data == "YO'Q")
async def state_8(c: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if c.data == "YO'Q" and current_state == SendLogin.confirm:
        await c.message.bot.delete_message(chat_id=c.from_user.id, message_id=message_ids[c.from_user.id])
        await c.answer(text="❌ Bekor qilindi.", show_alert=True)
    elif c.data == "HA" and current_state == SendLogin.confirm:
        await c.message.bot.delete_message(chat_id=c.from_user.id, message_id=message_ids[c.from_user.id])
        user_data = await state.get_data()
        bot = user_data["bot"]
        email = user_data["email"]
        password = user_data["password"]
        ssh_link = user_data["ssh_link"]
        ssh_login = user_data["ssh_login"]
        ssh_pass = user_data["ssh_pass"]

        message = (
            f"<b>Bot:</b>\n"
            f"<b>Username:</b> {bot}\n"
            f"<b>Login:</b> <code>{email}</code>\n"
            f"<b>Parol:</b> <code>{password}</code>\n\n"
            f"<b>SSH:</b> <a href='{ssh_link}'>Link</a>\n"
            f"<b>Login:</b> <code>{ssh_login}</code>\n"
            f"<b>Parol:</b> <code>{ssh_pass}</code>")
        try:
            await c.bot.send_message(CHANNEL_ID, message, reply_markup=channel_menu(bot=bot[1:], ssh=ssh_link))
            await c.answer(text="Yuborildi ✅", show_alert=True)
        except Exception as e:
            print(e)
            await c.answer(text=str(e), show_alert=True)
        await state.clear()


@router.message()
async def message_received(message: Message):
    await message.delete()
