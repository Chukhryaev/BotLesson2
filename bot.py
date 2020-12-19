import config
import telebot

bot = telebot.TeleBot(config.TOKEN)


@bot.channel_post_handler()
def channel_post(message):
	bot.edit_message_text(f"{message.text}\n\nBy Alexey Chukhryaev", message.chat.id, message.message_id)


bot.polling(none_stop=True)
