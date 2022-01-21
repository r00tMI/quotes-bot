from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from random import randint, randrange
import sys, os, time
import requests

admins = os.getenv("BOT_ADMINS", "")
admins = admins.split(",")

token = os.getenv("TELEGRAM_TOKEN")

update_url = os.getenv("BOT_UPDATE_URL")
buzz_update_url = os.getenv("BUZZ_UPDATE_URL")
if not token:
    print("No token in TELEGRAM_TOKEN")
    sys.exit(-1)

quoteslist = open("quotes.txt","r").readlines()
buzz = open("buzzwords.txt", "r").readlines()

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
        if not buzz_update_url:
            print("Buzzword update functionality is disabled, no BUZZ_UPDATE_URL defined")
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Update automatico buzzwords disabilitato")
        if update_url:
            try:
                with open("quotes.txt", "wb") as quotesfile:
                    quotesfile.write(requests.get(update_url).content)
                quoteslist = open("quotes.txt","r").readlines()
                print("Bot updated")
                context.bot.sendMessage(chat_id=update.message.chat_id, text="Bot aggiornato")
            except Exception as e:
                print(e)
                context.bot.sendMessage(chat_id=update.message.chat_id, text="Errore nell'aggiornamento del bot")
        if buzz_update_url:
            try:
                with open("buzzwords.txt", "wb") as quotesfile:
                    quotesfile.write(requests.get(buzz_update_url).content)
                buzz = open("buzzwords.txt","r").readlines()
                print("Buzz updated")
                context.bot.sendMessage(chat_id=update.message.chat_id, text="Buzzwords aggiornate")
            except Exception as e:
                print(e)
                context.bot.sendMessage(chat_id=update.message.chat_id, text="Errore nell'aggiornamento del bot")


def handlebuzz(update, context):
    response = None
    for bw in buzz:
        bw = bw.strip()
        if bw.lower() in update.message.text.lower():
            reduced_quoteslist = [x for x in quoteslist if bw.lower() in x.lower()]
            response = reduced_quoteslist[randint(0, len(reduced_quoteslist)-1)].strip()
            break
    if response:
        time.sleep(randrange(155, 289)/100)
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

def main():
    updater = Updater(token, use_context=True);
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("quotesupdate", quotesupdate, filters=Filters.chat_type.private))
    buzz_handler = MessageHandler(Filters.text & ~(Filters.command), handlebuzz)
    dp.add_handler(buzz_handler)
    
    updater.start_polling()
    print("================================")
    print("========= Bot Running ==========")
    print("================================")
    updater.idle()
        
if __name__ == "__main__":
    main()
