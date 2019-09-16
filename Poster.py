import logging

from telegram.ext import Updater, CommandHandler

from Ploter import plot
import HHStatus

def Loop():
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

	updater = Updater(token=config.token)

	# bot = telegram.Bot(token='773057189:AAG37T3Y7d-quTjNrwPDMeU9FxOWeGHJCa8')

    def start(bot, update):
        plot_photo = plot()
        max_speed, trust, quality, hitrate, hathrate = HHStatus.parser(HHStatus.fetch())
        bot.send_message(chat_id=update.message.chat_id, text="Max Speed: "+max_speed+"\nTrust: "+trust+"\nQuality: "+quality+"\nHitrate: "+hitrate+"\nHathrate: "+hathrate)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(plot_photo, "rb"))
    
    
    updater.dispatcher.add_handler(CommandHandler('get_status', start))
    
    updater.start_polling()
    updater.idle()
