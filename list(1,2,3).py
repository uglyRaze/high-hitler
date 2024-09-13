import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Вставьте ваш токен бота
TOKEN = '7511757571:AAGQ4mnDzqHqRh69qpHx-Oy4NTKQ9QqWJdQ'
CHANNEL_ID = '@GlobCripto'

bot = telebot.TeleBot(TOKEN)

def check_subscription(user_id: int) -> bool:
    try:
        # Используем метод get_chat_member для проверки подписки
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
    return False

@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id

    if check_subscription(user_id):
        show_farm_menu(message.chat.id)
    else:
        markup = InlineKeyboardMarkup()
        subscribe_button = InlineKeyboardButton("Подписаться", url="https://t.me/GlobCripto")
        check_button = InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")
        markup.add(subscribe_button)
        markup.add(check_button)
        bot.send_message(message.chat.id, f"Пожалуйста, подпишитесь на канал [{CHANNEL_ID}](https://t.me/GlobCripto) и нажмите 'Проверить подписку'.", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def callback_check_subscription(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        bot.send_message(call.message.chat.id, "Принято✅")
        show_farm_menu(call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id, f"Вы ещё не подписаны на канал {CHANNEL_ID}. Пожалуйста, подпишитесь и попробуйте снова.")

def show_farm_menu(chat_id):
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url="https://luminous-churros-fb45ea.netlify.app/")
    start_farm_button = InlineKeyboardButton("Начать фарм", web_app=web_app_info)
    markup.add(start_farm_button)
    bot.send_message(chat_id, "Вы успешно подписаны! Что вы хотите сделать дальше?", reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)