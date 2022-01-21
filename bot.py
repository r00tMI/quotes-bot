from telegram.ext import Updater, CommandHandler
from random import randint
import sys, os

token = os.getenv("TELEGRAM_TOKEN")
if not token:
    print("No token in TELEGRAM_TOKEN")
    sys.exit(-1)

quoteslist = open("quotes.txt","r").readlines()

def get_random_quote():
    return quoteslist[randint(0, len(quoteslist)-1)].strip()

def quote(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text=get_random_quote())

def main():
    updater = Updater(token, use_context=True);
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("quote", quote))

    updater.start_polling()
    print("================================")
    print("========= Bot Running ==========")
    print("================================")
    updater.idle()
        
if __name__ == "__main__":
    main()
