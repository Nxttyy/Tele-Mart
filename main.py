from telegram import ForceReply, Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from handle_http import get_update_http
from dotenv import load_dotenv
import os
 
load_dotenv()

token = os.getenv("TOKEN")
bot = Bot(token=token)

channel_id = "-1002095318844"

# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def get_chat_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # data = get_update_http()
    caption = """
        Line 1,
        Line 2,
        Line 3

    """
    # await send_chat()
    # await update.message.reply_text(data)
    await bot.send_photo(chat_id=channel_id, photo="AgACAgQAAxkBAAMoZdUvhoDfjVCanQmwWaqq_nDJo1IAAi69MRsjx7FSdjEGrYpsu7IBAAMCAAN4AAM0BA"
                        , caption=caption)

    await bot.send_dice(chat_id=channel_id)

async def send_chat():
    await bot.send_media_group(chat_id=channel_id, media="AgACAgQAAxkBAAMoZdUvhoDfjVCanQmwWaqq_nDJo1IAAi69MRsjx7FSdjEGrYpsu7IBAAMCAAN4AAM0BA")
    
    await bot.sendMessage(chat_id=channel_id, text='text')



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7042146370:AAFZZsYSR8LZ9hc8E9iwGdAMxF94OSnX9iI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("update", get_chat_update))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, get_chat_update))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()