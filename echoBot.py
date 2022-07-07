import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

URL = "https://api.openweathermap.org/data/2.5/weather/"
APPID = "b4b5d496fb899aacb02b778068bd7372"

def get_weather_url(params):
    params["appid"] = APPID
    return requests.get(URL, params=params).json()

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    update.message.reply_html(
        f"Hi {user.mention_html()}! \n\n/today - Bugungi ob-haxo\n/tomorrow - ertagalik ob-havo \n/week - haftalik ob-havo"
    )


def today_command(update: Update, context: CallbackContext):
    city = "tashkent"
    
    if update.message.text!="/today":
        message_splited = update.message.text.split(" ")
        city = ' '.join(message_splited[1::])

    response = get_weather_url({'q': city})
    
    if response["cod"]!="404":
        data = response["weather"][0]["description"]
        update.message.reply_text(f"City: {city}\nWeather: {data}")
    else:
        update.message.reply_text(f"Not found")

def week_command(update: Update, context: CallbackContext):
    #
    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast/daily?&cnt=7&appid={APPID}")
    print(response)
    #data = response["weather"][0]["description"]
    data = "hh"
    update.message.reply_text(f"City: Toshkent\nWeather: {data}")


def help_command(update: Update, CallbackContext) -> None:
    update.message.reply_text("Help!")



def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)



def main() -> None:

    updater = Updater("5497289274:AAEdP_loU1R5fkYlevIs4YTiVLKrNUnZqyU")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("today", today_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == "__main__":

    main()