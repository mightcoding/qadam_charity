from telebot import TeleBot
from db import initialize_database
from logic import start, price_menu, gift_menu, gift_details, partial_payment, final_selection, buy_full

with open("token.txt") as token_file:
    TOKEN = token_file.read().strip()

def main():
    initialize_database()
    bot = TeleBot(TOKEN)

    @bot.message_handler(commands=["start"])
    def handle_start(message):
        start(message, bot)

    @bot.callback_query_handler(func=lambda call: call.data == "choose_price")
    def handle_price_menu(call):
        price_menu(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("price_"))
    def handle_gift_menu(call):
        gift_menu(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("gift_"))
    def handle_gift_details(call):
        gift_details(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("partial_"))
    def handle_partial_payment(call):
        partial_payment(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("final_"))
    def handle_final_selection(call):
        final_selection(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("buy_full_"))
    def handle_buy_full(call):
        buy_full(call, bot)


    print("Бот запущен...")
    bot.polling()

if __name__ == "__main__":
    main()
