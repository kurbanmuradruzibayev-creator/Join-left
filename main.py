import telebot
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get TOKEN from environment variables
TOKEN = os.getenv("TOKEN")
if not TOKEN or ":" not in TOKEN:
    logging.error("Bot token is invalid or not found")
    raise ValueError("Bot token noto‘g‘ri yoki topilmadi")

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Multilingual responses
LANGUAGES = {
    'en': {
        'welcome': "Welcome! This bot removes group join/leave messages.",
        'no_permission': "I don't have permission to delete messages. Please make me an admin.",
        'error': "An error occurred while processing the request."
    },
    'uz': {
        'welcome': "Xush kelibsiz! Bu bot guruhga qo'shilish/chiqish xabarlarini o‘chiradi.",
        'no_permission': "Xabarlarni o‘chirish uchun ruxsatim yo‘q. Iltimos, meni admin qiling.",
        'error': "So‘rovni bajarishda xatolik yuz berdi."
    }
}

# Default language (can be changed dynamically if needed)
DEFAULT_LANG = 'en'

# Function to get message text based on language
def get_message(key, lang=DEFAULT_LANG):
    return LANGUAGES.get(lang, LANGUAGES[DEFAULT_LANG])[key]

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    lang = DEFAULT_LANG  # You can implement logic to detect user language if needed
    bot.reply_to(message, get_message('welcome', lang))

# Handler for new chat members (join messages)
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_members(message):
    try:
        # Delete the "new member" message
        bot.delete_message(message.chat.id, message.message_id)
        logging.info(f"Deleted new member message in chat {message.chat.id}")
    except telebot.apihelper.ApiTelegramException as e:
        if "chat not found" in str(e) or "not enough rights" in str(e):
            lang = DEFAULT_LANG
            bot.reply_to(message, get_message('no_permission', lang))
        else:
            logging.error(f"Error deleting message: {e}")
            lang = DEFAULT_LANG
            bot.reply_to(message, get_message('error', lang))

# Handler for left chat members (leave messages)
@bot.message_handler(content_types=['left_chat_member'])
def handle_left_member(message):
    try:
        # Delete the "left member" message
        bot.delete_message(message.chat.id, message.message_id)
        logging.info(f"Deleted left member message in chat {message.chat.id}")
    except telebot.apihelper.ApiTelegramException as e:
        if "chat not found" in str(e) or "not enough rights" in str(e):
            lang = DEFAULT_LANG
            bot.reply_to(message, get_message('no_permission', lang))
        else:
            logging.error(f"Error deleting message: {e}")
            lang = DEFAULT_LANG
            bot.reply_to(message, get_message('error', lang))

# Start the bot
try:
    logging.info("Bot is starting...")
    bot.infinity_polling()
except Exception as e:
    logging.error(f"Bot crashed: {e}")
