import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)

posts = {}


@bot.channel_post_handler()
def channel_post(message):
    posts.update({message.message_id: {
        "like": 0,
        "dislike": 0
    }})
    buttons = types.InlineKeyboardMarkup()
    buttons.add(*[types.InlineKeyboardButton(text=f"👍 {posts.get(message.message_id).get('like')}", callback_data=f"like"),
                  types.InlineKeyboardButton(text=f"👎 {posts.get(message.message_id).get('dislike')}", callback_data=f"dislike")])
    bot.edit_message_text(f"{message.text}\n\nBy Alexey Chukhryaev", message.chat.id, message.message_id,
                          reply_markup=buttons)


@bot.callback_query_handler(func=lambda call: call.data == "like")
def callback_like(call):
    bot.answer_callback_query(call.id, text=f"You voted Like")
    post = posts.get(call.message.message_id)
    posts.update({call.message.message_id: {
        "like": post.get('like') + 1,
        "dislike": post.get('dislike')
    }})
    buttons = types.InlineKeyboardMarkup()
    buttons.add(
        *[types.InlineKeyboardButton(text=f"👍 {posts.get(call.message.message_id).get('like')}", callback_data=f"like"),
          types.InlineKeyboardButton(text=f"👎 {posts.get(call.message.message_id).get('dislike')}",
                                     callback_data=f"dislike")])
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=buttons)



@bot.callback_query_handler(func=lambda call: call.data == "dislike")
def callback_dislike(call):
    bot.answer_callback_query(call.id, text=f"You voted Dislike")
    post = posts.get(call.message.message_id)
    posts.update({call.message.message_id: {
        "like": post.get('like'),
        "dislike": post.get('dislike') + 1
    }})
    buttons = types.InlineKeyboardMarkup()
    buttons.add(
        *[types.InlineKeyboardButton(text=f"👍 {posts.get(call.message.message_id).get('like')}", callback_data=f"like"),
          types.InlineKeyboardButton(text=f"👎 {posts.get(call.message.message_id).get('dislike')}",
                                     callback_data=f"dislike")])
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=buttons)


bot.polling(none_stop=True)
