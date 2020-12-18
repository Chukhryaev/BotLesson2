import config
import telebot

bot = telebot.TeleBot(config.TOKEN)


@bot.channel_post_handler()
def channel_post(message):
	print(message)


bot.polling(none_stop=True)
