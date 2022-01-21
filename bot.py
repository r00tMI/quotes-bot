from telegram.ext import Updater, CommandHandler
from random import randint
import sys, os
import requests

admins = os.getenv("BOT_ADMINS", "")
admins = admins.split(",")

token = os.getenv("TELEGRAM_TOKEN")

update_url = os.getenv("BOT_UPDATE_URL")
if not token:
    print("No token in TELEGRAM_TOKEN")
    sys.exit(-1)

quoteslist = open("quotes.txt","r").readlines()

def get_random_quote():
    return quoteslist[randint(0, len(quoteslist)-1)].strip()

def quote(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text=get_random_quote())

def quotesupdate(update, context):
    global admins, quoteslist
    user = update.message.from_user
    if str(user.id) in admins:
        print("Update command issued by admin, updating")
        if not update_url:
            print("Update functionality is disabled, no BOT_UPDATE_URL defined")
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Update automatico disabilitato")
            return
        try:
            with open("quotes.txt", "wb") as quotesfile:
                quotesfile.write(requests.get(update_url).content)
            quoteslist = open("quotes.txt","r").readlines()
            print("Bot updated")
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Bot aggiornato")
        except Exception as e:
            print(e)
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Errore nell'aggiornamento del bot")
def main():
    updater = Updater(token, use_context=True);
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("quotesupdate", quotesupdate))

    updater.start_polling()
    print("================================")
    print("========= Bot Running ==========")
    print("================================")
    updater.idle()
        
if __name__ == "__main__":
    main()
