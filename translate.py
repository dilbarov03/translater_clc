import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import translators as ts

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TRANSLATE = 1

def g_translate(m, tolang):
   m = m.split('\n\n ')[0]
   text = "u"


   if len(m)<2900:
      try:
         text = ts.google(m,to_language=tolang)
      except Exception as e:
         #bot.send_message(1348219246,f"Error in gtrans function. \nInput was : {m}\n ERROR : {e}")
         text = "could not translate this"
   else:
      text = 'Text can not be longer than 2900 characters. \n Please try with shorter one.'
   return text


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    update.message.reply_html(
        f"Hi {user.mention_html()}! \n\nSend the text to translate"
    )

def echo(update: Update, context: CallbackContext) -> None:
   context.user_data['text'] = update.message.text

   keyboard = [['EN', 'UZ', 'RU']]

   markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

   update.message.reply_text("Choose the language: ", reply_markup=markup)
   return TRANSLATE

def translate(update, context):
   #markup = ReplyKeyboardRemove()
   langs = ['EN', 'UZ', 'RU']
   if update.message.text in langs:
      text = g_translate(context.user_data['text'], update.message.text.lower())
      update.message.reply_text(text)
      return TRANSLATE


def cancel():
   pass

def main() -> None:
   updater = Updater("5497289274:AAEdP_loU1R5fkYlevIs4YTiVLKrNUnZqyU")

   dispatcher = updater.dispatcher

   handler = ConversationHandler(
      entry_points=[MessageHandler(Filters.text & ~Filters.command, echo)],
      states={
            TRANSLATE: [MessageHandler(Filters.regex('^(EN|UZ|RU)$'), translate)]
            #TRANSLATE: [MessageHandler('translate', translate)],
      },
      fallbacks=[CommandHandler('cancel', cancel)],)
   # add the handler to the dispatcher
   dispatcher.add_handler(handler)

   # on different commands - answer in Telegram
   dispatcher.add_handler(CommandHandler("start", start))
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