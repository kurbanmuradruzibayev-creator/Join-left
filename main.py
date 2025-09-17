from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Bot tokeningizni shu yerga yozing
TOKEN = 'YOUR_BOT_TOKEN_HERE'

async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Service xabarlarni (new_chat_members, left_chat_member) o'chirish funksiyasi.
    Bu handler faqat guruh xabarlariga ishlaydi.
    """
    if update.effective_chat.type in ['group', 'supergroup']:
        message = update.message
        # Agar xabar service xabari bo'lsa (qo'shish yoki o'chirish)
        if message.new_chat_members or message.left_chat_member or message.migrate_to_chat_id or message.migrate_from_chat_id:
            try:
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=message.message_id
                )
                print(f"Service xabar o'chirildi: {message.message_id}")
            except Exception as e:
                print(f"Xatoni o'chirishda: {e}")

def main():
    # Application yaratish
    application = Application.builder().token(TOKEN).build()
    
    # Handler qo'shish: barcha xabarlarga (faqat service uchun filter ishlatish mumkin)
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, delete_service_messages))
    
    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
