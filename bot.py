from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

user_data = {}


async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_data[user.id] = user.first_name
    await update.message.reply_text("Salom! Admin bilan bog‘lanish uchun shunchaki xabar yuboring.")


async def user_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text

    admin_text = (f"📩 *Yangi xabar*\n"
                  f"👤 [ {user.first_name} ](tg://user?id={user.id})\n"
                  f"🆔 `{user.id}`\n"
                  f"📋 `/reply {user.id}`\n\n"
                  f"{text}")
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")

    await update.message.reply_text("✅ Xabaringiz adminga yuborildi. Javob kuting.")


async def reply(update: Update, context: CallbackContext):
    if update.message.chat_id != ADMIN_ID:
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Foydalanish formati: `/reply user_id xabar`")
        return

    user_id = args[0]
    reply_text = " ".join(args[1:])

    try:
        user_id = int(user_id)
        if user_id in user_data:
            user_name = user_data[user_id]
            await context.bot.send_message(chat_id=user_id, text=f"📩 *Admin javobi:*\n\n{reply_text}", parse_mode="Markdown")
            await update.message.reply_text(f"✅ Xabar {user_name} ga yuborildi.")
        else:
            await update.message.reply_text("❌ Foydalanuvchi ma'lumotlari topilmadi.")
    except ValueError:
        await update.message.reply_text("❌ Noto‘g‘ri foydalanuvchi ID!")


async def admin_wrong_message(update: Update, context: CallbackContext):
    if update.message.chat_id == ADMIN_ID:
        await update.message.reply_text(f"❌ Javob yuborish uchun quyidagi formatdan foydalaning:\n\n`/reply` user ID xabar", parse_mode="Markdown")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Chat(ADMIN_ID), user_message))

    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_ID), admin_wrong_message))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()