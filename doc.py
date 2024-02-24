from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update,
    ForceReply,
    LabeledPrice, InputInvoiceMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, PhotoSize, InputInvoiceMessageContent
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from dotenv import load_dotenv
import os
 
load_dotenv()

token = os.getenv("TOKEN")
channel_id = os.getenv("CHANNEL-ID")
chappa_token = os.getenv("CHAPPA-TOKEN")


START, RECIEVE_TITLE, RECIEVE_DESCRIPTION, RECIEVE_PRICE = range(4)


listing_attributes = ['title', 'description', 'price', '']
current_attribute = 0

reply_keyboard = [
    ["List a product", "Exit"],
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the conversation and ask user for input."""
    print("96")
    

    # keyboard = [
    #     [
    #         InlineKeyboardButton("List item for sale.", callback_data="1"),
    #         # InlineKeyboardButton("2", callback_data=2),
    #     ]
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=markup,
    )

    return START

async def start_listing_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("*")
    # category = listing_attributes[current_attribute]
    await update.message.reply_text(f"Your title?")
    # Application
    
    return RECIEVE_TITLE

# async def receive_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

#     """Store info provided by user and ask for the next category."""
#     global current_attribute

#     attribute = listing_attributes[current_attribute]

#     user_data = context.user_data
#     text = update.message.text
#     user_data[attribute] = text
    
#     current_attribute += 1
#     next_attribute = listing_attributes[current_attribute]

#     if (next_attribute):
#         await update.message.reply_text(f"Your {next_attribute.lower()}?")
#         return RECIEVE_INFO

#     current_attribute = 0
#     await done(update, context)

async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(1)
    user_data = context.user_data
    text = update.message.text
    user_data[listing_attributes[0]] = text

    await update.message.reply_text(f"Your description?")


    return RECIEVE_DESCRIPTION

async def receive_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(2)
    user_data = context.user_data
    text = update.message.text
    user_data[listing_attributes[1]] = text

    await update.message.reply_text(f"Your price?")

    return RECIEVE_PRICE

async def receive_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(3)
    user_data = context.user_data
    text = update.message.text
    user_data[listing_attributes[2]] = text

    # await update.message.reply_text(f"Your description?")
    await done(update, context)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    # done_reply_keyboard = [
    # ["List a another product"],
    # ]   

    # done_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data = context.user_data

    await update.message.reply_text(
        f"I learned these facts about you: {user_data}Until next time!",
    )

    await start_without_shipping_callback(user_data['title'], user_data['description'], user_data['price'], update, context)

    user_data.clear()
    
    # return ConversationHandler.END

async def start_without_shipping_callback(title, description, price, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
    payload = "I-LOVE-CHAPA"
    currency = "ETB"
    price = int(price)
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 1000)]

    photo_size = PhotoSize(file_id="AgACAgQAAxkBAAIBb2XYug6cwfjkHgOCu02-JQABZL7IPAACo78xG1w8yFK16nGLzR8mFQEAAwIAA3MAAzQE"
                           , file_unique_id="AQADo78xG1w8yFJ4", width=320, height=250)

    await context.bot.send_invoice(channel_id, title, description, payload, chappa_token, currency, prices, max_tip_amount=20, suggested_tip_amounts=[1,10,15]
        , photo_url="data:image/jpeg;base64,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"
        , photo_width=250, photo_height=350)

    

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    await update.message.reply_text("Thank you for your payment!")

def main() -> None:
    application = Application.builder().token(token).build()

    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CallbackQueryHandler(start_listing_info(Update) , pattern="1"))
    # application.add_handler(MessageHandler(filters.PHOTO, downloader))

    application.add_handler(MessageHandler(
                    filters.Regex("^(List a product)$"), start_listing_info
                ),
    )

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
    # entry_points=[CommandHandler("b", start_listing_info)],
    # entry_points=[CallbackQueryHandler(start_listing_info, "1")],   
    entry_points=[CommandHandler("start", start)],
 
    states={
            START: [
                MessageHandler(
                    filters.Regex("^(List a product)$"), start_listing_info
                ),
                # MessageHandler(filters.Regex("^Something else...$"), custom_choice),
            ],
            RECIEVE_TITLE: [
                MessageHandler(
                    filters.Regex(""), receive_title
                ),
            ],
            RECIEVE_DESCRIPTION: [
                MessageHandler(
                    filters.Regex(""), receive_description
                ),
            ],
            RECIEVE_PRICE: [
                MessageHandler(
                    filters.Regex("[0-9]"), receive_price
                ),
            ],
            # RECIEVE_INFO: [
            #     MessageHandler(
            #         filters.Regex(""), receive_info
            #     ),
            # ],
            
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()