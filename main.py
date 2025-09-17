import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get("TOKEN")  # set TOKEN in env (or paste token string here)

def remove_status_messages(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat_id = msg.chat.id
    msg_id = msg.message_id

    # new_chat_members, left_chat_member, new_chat_title, new_chat_photo, delete_chat_photo, migrate_to_chat_id, migrate_from_chat_id, pinned_message ...
    # Filters.status_update will match these service messages.
    try:
        # Bot must be admin with 'Delete messages' permission
        context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except Exception as e:
        # ignore failures (lack of permission, message already deleted, etc.)
        # optional: log e
        pass

def main():
    if not TOKEN:
        print("TOKEN environment variable not set.")
        return

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Catch all status update service messages (join/leave/pinned/migrate/etc.)
    dp.add_handler(MessageHandler(Filters.status_update, remove_status_messages))

    # Optional: also remove plain text "welcome" messages (if you want)
    # dp.add_handler(MessageHandler(Filters.text & Filters.group, remove_text_messages))

    updater.start_polling()
    print("Bot started")
    updater.idle()

if __name__ == "__main__":
    main()
