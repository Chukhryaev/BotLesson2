import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)

posts = {}


def get_buttons_with_rating(message_id):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(*[types.InlineKeyboardButton(text=f"👍 {posts.get(message_id).get('like')}", callback_data=f"like"),
                  types.InlineKeyboardButton(text=f"👎 {posts.get(message_id).get('dislike')}",
                                             callback_data=f"dislike")])
    return buttons


@bot.channel_post_handler()
def channel_post(message):
    posts.update({message.message_id: {
        "like": 0,
        "dislike": 0
    }})
    bot.edit_message_text(f"{message.text}\n\nBy Alexey Chukhryaev", message.chat.id, message.message_id,
                          reply_markup=get_buttons_with_rating(message.message_id))


@bot.callback_query_handler(func=lambda call: call.data == "like")
def callback_like(call):
    bot.answer_callback_query(call.id, text=f"You voted Like")
    post = posts.get(call.message.message_id)
    posts.update({call.message.message_id: {
        "like": post.get('like') + 1,
        "dislike": post.get('dislike')
    }})
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=get_buttons_with_rating(call.message.message_id))


@bot.callback_query_handler(func=lambda call: call.data == "dislike")
def callback_dislike(call):
    bot.answer_callback_query(call.id, text=f"You voted Dislike")
    post = posts.get(call.message.message_id)
    posts.update({call.message.message_id: {
        "like": post.get('like'),
        "dislike": post.get('dislike') + 1
    }})
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=get_buttons_with_rating(call.message.message_id))


bot.polling(none_stop=True)
