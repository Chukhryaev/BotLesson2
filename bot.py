import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.channel_post_handler()
def channel_post(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(*[types.InlineKeyboardButton(text="👍 Like", callback_data=f"like"),
                  types.InlineKeyboardButton(text="👎 Dislike", callback_data=f"dislike")])
    bot.edit_message_text(f"{message.text}\n\nBy Alexey Chukhryaev", message.chat.id, message.message_id,
                          reply_markup=buttons)


@bot.callback_query_handler(func=lambda call: True)
def query(call):
    bot.answer_callback_query(call.id, text=f"You voted {call.data}")


bot.polling(none_stop=True)
