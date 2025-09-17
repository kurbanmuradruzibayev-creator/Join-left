from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")  # .env faylidan tokenni o'qish

def delete_join(update, context):
    try:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Xato: {e}")  # Xatolarni log qilish

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, delete_join))  # Yangi a'zo xabari
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, delete_join))  # Chiqish xabari
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
