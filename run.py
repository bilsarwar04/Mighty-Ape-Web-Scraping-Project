from bot.test import WebAutomator


item = input("What item are you after today?: ")
proceed = False
min_price = float(input("What is the minimum price range?: "))
max_price = float(input("What is the maximum price range?: "))

bot = WebAutomator()
bot.open_first_page()
bot.search_item(item)
bot.apply_price_filters(min_price, max_price)
bot.proceed_to_next_page(min_price, max_price)
bot.final_products_list()
bot.generate_table()



