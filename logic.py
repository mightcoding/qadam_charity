from telebot import TeleBot, types
from db import get_gifts_by_price, get_gift_details, delete_gift

def start(message, bot: TeleBot):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Выбрать подарок", callback_data="choose_price"))
    bot.send_message(message.chat.id, "✨Добро пожаловать! Нажмите на 'Выбрать подарок', чтобы начать:", reply_markup=markup)

def price_menu(call, bot: TeleBot):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("До 15 тысяч тг", callback_data="price_under_15k"))
    markup.add(types.InlineKeyboardButton("Больше 15 тысяч тг", callback_data="price_more_15k"))
    bot.edit_message_text("🎀 Выберите диапазон цен: ", call.message.chat.id, call.message.id, reply_markup=markup)

def gift_menu(call, bot: TeleBot):
    price_range = call.data
    if price_range == "price_under_15k":
        gifts = get_gifts_by_price("under_15k")
    elif price_range == "price_more_15k":
        gifts = get_gifts_by_price("more_15k")
    else:
        gifts = []

    if not gifts:
        bot.edit_message_text("Подарки в этом диапазоне не найдены.", call.message.chat.id, call.message.id)
        return

    markup = types.InlineKeyboardMarkup()
    for gift in gifts:
        markup.add(types.InlineKeyboardButton(gift[1], callback_data=f"gift_{gift[0]}"))
    markup.add(types.InlineKeyboardButton("Назад", callback_data="choose_price"))
    bot.edit_message_text("Выберите подарок:", call.message.chat.id, call.message.id, reply_markup=markup)

def gift_details(call, bot: TeleBot):
    gift_id = int(call.data.split("_")[1])
    gift = get_gift_details(gift_id)
    if not gift:
        bot.edit_message_text("Подарок не найден. Пожалуйста, выберите другой.", call.message.chat.id, call.message.id)
        return
    name, price, description, link = gift
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Купить полностью", callback_data=f"buy_full_{gift_id}"))
    if price > 15000:
        markup.add(types.InlineKeyboardButton("Частичная оплата", callback_data=f"partial_{gift_id}"))
    markup.add(types.InlineKeyboardButton("Выбрать другой подарок", callback_data="choose_price"))
    bot.edit_message_text(
        f"*{name}*\nЦена: {price} тг\n{description}\n\nАдрес школы для отправки: Туркестан 32/1 (МША)",
        call.message.chat.id, call.message.id, parse_mode="Markdown", reply_markup=markup
    )

def partial_payment(call, bot: TeleBot):
    bot.edit_message_text("Для частичной оплаты переведите нужную сумму на Kaspi Карту: 1234 5678 9012 3456",
                          call.message.chat.id, call.message.id)

def buy_full(call, bot: TeleBot):
    gift_id = int(call.data.split("_")[2])
    gift = get_gift_details(gift_id)
    if not gift:
        bot.edit_message_text("Подарок не найден. Пожалуйста, выберите другой.", call.message.chat.id, call.message.id)
        return
    name, price, description, link = gift
    delete_gift(gift_id)
    bot.edit_message_text(f"🎁 Спасибо! Ваш подарок *{name}* был выбран и отправлен на адрес: Туркестан 32/1 (МША).\n\nВот ссылка на товар: [Товар]({link})",
                          call.message.chat.id, call.message.id, parse_mode="Markdown")


def final_selection(call, bot: TeleBot):
    bot.edit_message_text("🎁 Спасибо! Ваш подарок выбран. Мы свяжемся с вами в ближайшее время!",
                          call.message.chat.id, call.message.id)
