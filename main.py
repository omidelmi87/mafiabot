import logging
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
#from telegram.ext import Application
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
ROOT, CREATE, JOIN, MODE1, MODE2, MODE3, MODE4 = range(6)
# Callback data
cb_CREATE, cb_JOIN, cb_MODE1, cb_MODE2, cb_MODE3, cb_MODE4, cb_MODE1_opt1, cb_MODE1_opt2, \
    cb_MODE2_opt1, cb_MODE2_opt2, cb_MODE3_opt1, cb_MODE3_opt2, cb_MODE4_opt1, cb_MODE4_opt2 = range(13)

def start(update: Update, context: CallbackContext) -> int:
    """Sends a message with three inline buttons attached."""
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).

    Option_1 = "ایجاد بازی"
    Option_2 = "شرکت در بازی"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(cb_CREATE)),
            InlineKeyboardButton(Option_2, callback_data=str(cb_JOIN)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    Welcome_Message = "به بات خانواده رویال مافیا خوش آمدید. برای ادامه یکی از گزینه ها را انتخاب کنید."
    update.message.reply_text(Welcome_Message, reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `ROOT` now
    return ROOT


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    Option_1 = "ایجاد بازی"
    Option_2 = "شرکت در بازی"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(cb_CREATE)),
            InlineKeyboardButton(Option_2, callback_data=str(cb_JOIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    Welcome_Message = "به بات خانواده رویال مافیا خوش آمدید. برای ادامه یکی از گزینه ها را انتخاب کنید."
    update.message.reply_text(Welcome_Message, reply_markup=reply_markup)
    return ROOT


def create(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    Option_1 = "تکاور"
    Option_2 = "رویال"
    Option_3 = "مذاکره"
    Option_4 = "روسی"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(MODE1)),
            InlineKeyboardButton(Option_2, callback_data=str(MODE2)),
            InlineKeyboardButton(Option_3, callback_data=str(MODE3)),
            InlineKeyboardButton(Option_4, callback_data=str(MODE4)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    Message = "لطفا سناریوی مورد نظر خود را انتخاب کنید."
    query.edit_message_text(

        text=Message, reply_markup=reply_markup
    )
    return ROOT


def join(update: Update, context: CallbackContext) -> int:
    """Ask user the game id"""
    Message = "لطفا شماره بازی را وارد کنید:"
    update.message.reply_text(Message)
    user_input = update.message.text
    game_id = str.lower(user_input)
    update.message.reply_text(game_id)

    return ROOT


# تکاور
def mode1(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    Option_1 = "10 نفره"
    Option_2 = "13 نفره"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(cb_MODE1_opt1)),
            InlineKeyboardButton(Option_2, callback_data=str(cb_MODE1_opt2)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    Message = "لطفا تعداد بازیکنان حاضر در بازی را مشخص کنید."
    query.edit_message_text(
        text=Message, reply_markup=reply_markup
    )
    # Transfer to conversation state `CREATE`
    return CREATE


# رویال
def mode2(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    Option_1 = "10 نفره"
    Option_2 = "13 نفره"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(cb_MODE2_opt1)),
            InlineKeyboardButton(Option_2, callback_data=str(cb_MODE2_opt2)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    Message = "لطفا تعداد بازیکنان حاضر در بازی را مشخص کنید."
    query.edit_message_text(
        text=Message, reply_markup=reply_markup
    )
    # Transfer to conversation state `CREATE`
    return CREATE


# مذاکره
def mode3(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    Option_1 = "10 نفره"
    Option_2 = "12 نفره"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(cb_MODE3_opt1)),
            InlineKeyboardButton(Option_2, callback_data=str(cb_MODE3_opt2)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    Message = "لطفا تعداد بازیکنان حاضر در بازی را مشخص کنید."
    query.edit_message_text(
        text=Message, reply_markup=reply_markup
    )
    # Transfer to conversation state `CREATE`
    return CREATE


# روسی
def mode4(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    Option_1 = "8 نفره"
    Option_2 = "10 نفره"
    keyboard = [
        [
            InlineKeyboardButton(Option_1, callback_data=str(cb_MODE4_opt1)),
            InlineKeyboardButton(Option_2, callback_data=str(cb_MODE4_opt2)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    Message = "لطفا تعداد بازیکنان حاضر در بازی را مشخص کنید."
    query.edit_message_text(
        text=Message, reply_markup=reply_markup
    )
    # Transfer to conversation state `CREATE`
    return CREATE


# تکاور 10 نفره
def mode1_opt1(update: Update, context: CallbackContext) -> None:



def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    API_Token = "5597241763:AAHGMKfDI02Rd3O7UB1eTNswsYukJFeNtvc"
    updater = Updater(API_Token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ROOT: [
                CallbackQueryHandler(create, pattern='^' + str(cb_CREATE) + '$'),
                CallbackQueryHandler(join, pattern='^' + str(cb_JOIN) + '$'),
            ],
            CREATE: [
                CallbackQueryHandler(mode1, pattern='^' + str(cb_MODE1) + '$'),
                CallbackQueryHandler(mode2, pattern='^' + str(cb_MODE2) + '$'),
                CallbackQueryHandler(mode3, pattern='^' + str(cb_MODE3) + '$'),
                CallbackQueryHandler(mode4, pattern='^' + str(cb_MODE4) + '$'),
            ],
            JOIN: [
                CallbackQueryHandler(end, pattern="پایان"),
            ],
            MODE1: [
                CallbackQueryHandler(mode1_opt1, pattern='^' + str(cb_MODE1_opt1) + '$'),
                CallbackQueryHandler(mode1_opt2, pattern='^' + str(cb_MODE1_opt2) + '$'),
            ],
            MODE2: [
                CallbackQueryHandler(mode2_opt1, pattern='^' + str(cb_MODE2_opt1) + '$'),
                CallbackQueryHandler(mode2_opt2, pattern='^' + str(cb_MODE2_opt2) + '$'),
            ],
            MODE3: [
                CallbackQueryHandler(mode3_opt1, pattern='^' + str(cb_MODE3_opt1) + '$'),
                CallbackQueryHandler(mode3_opt2, pattern='^' + str(cb_MODE3_opt2) + '$'),
            ],
            MODE4: [
                CallbackQueryHandler(mode4_opt1, pattern='^' + str(cb_MODE4_opt1) + '$'),
                CallbackQueryHandler(mode4_opt2, pattern='^' + str(cb_MODE4_opt2) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

"""
updater = Updater(API_Token, use_context=True)

def start(update: Update, context: CallbackContext):
    markup = ReplyKeyboardMarkup(keyboard=[['Create', KeyboardButton(text='Logo')]])
    update.message.reply_text("به بات خانواده رویال خوش آمدید.", reply_markup=markup)

def help(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")

def telegram_url(update: Update, context: CallbackContext):
    update.message.reply_text("telegram channel link here")

def archive_url(update: Update, context: CallbackContext):
    update.message.reply_text("telegram archive channel link here")

# Function will Filter out all the unknown commands sent by the user
# and reply to the message written inside it.
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

# Function for creating a match
def create(update: Update, context: CallbackQueryHandler):
    #query = update.callback_query
    update.edit_message_text(text="Selected option: {}")
# Function for joining a match
# Function for creating a channel for groups to chat
# Summary of the match

#updater.dispatcher.add_handler(CommandHandler('شروع', start))
#updater.dispatcher.add_handler(CommandHandler('کمک', help))
#updater.dispatcher.add_handler(CommandHandler('کانال تلگرام خانواده رویال مافیا', telegram_url))
#updater.dispatcher.add_handler(CommandHandler('کانال تلگرام آرشیو بازی ها', archive_url))
updater.dispatcher.add_handler(CommandHandler('Start', start))
updater.dispatcher.add_handler(CommandHandler('Help', help))
updater.dispatcher.add_handler(CommandHandler('Channel', telegram_url))
updater.dispatcher.add_handler(CommandHandler('Archive', archive_url))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands
updater.dispatcher.add_handler(CallbackQueryHandler(create))

"""



