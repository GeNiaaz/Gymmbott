import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import os
from os import environ
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


PORT = int(os.environ.get('PORT', '8443'))
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

# list creation
list_of_timings = [["Bishan ", "Century ", "JCube  ", "Keat   ", "Kebun  ", "Bedok  ", "Canberra "]]
# url to crawl
LINK = "https://smartentry.org/status/gymmboxx"

TOKEN = environ['TOKEN']
APP_NAME = environ['APP_NAME']

START_MESSAGE = "*I can send you current gymmboxx capacities!!*\n" + \
                "_I am in no way affliated to gymmboxx, just a fan :)_\n\n" + \
                "Get capacity for " + \
                "/all : all gymmboxx\n" + \
                "/bishan : Bishan gymmboxx\n" + \
                "/century : Century Square gymmboxx\n" + \
                "/jcube : Jcube gymmboxx\n" + \
                "/keat : Keat Hong gymmboxx\n" + \
                "/kebun : Kebun Baru gymmboxx\n" + \
                "/bedok : Bedok Point gymmboxx\n" + \
                "/canberra : Canberra gymmboxx"



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=START_MESSAGE, parse_mode= 'Markdown')

def get_all_gyms(update, context):
    str = get_all_gyms_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_bishan_gym(update, context):
    str = get_bishan_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_century_gym(update, context):
    str = get_century_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_jcube_gym(update, context):
    str = get_jcube_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_keat_gym(update, context):
    str = get_keat_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_kebun_gym(update, context):
    str = get_kebun_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_bedok_gym(update, context):
    str = get_bedok_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')

def get_cnbera_gym(update, context):
    str = get_cnbera_text()
    context.bot.send_message(chat_id=update.message.chat_id, text=str, parse_mode= 'Markdown')



'''
Args: website_link = string; link of website to be crawled
        link_class = string; class name for job link on website
Returns: jobs_link = list; list of jobs 
'''
def crawl(link):
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(2)

    html = driver.page_source 
    soup = BeautifulSoup(html, "html.parser") 
    all_divs = soup.find_all('div', class_ = 'box col-lg-4 col-md-6 col-sm-12') 

    # list creation 
    list_of_occupancies = []
    list_of_queuing = []

    # getting occupancy
    for gym in all_divs:
        occupancy = gym.find('span', class_ = 'occupancy')
        occupancy_text = occupancy.text
        list_of_occupancies.append(occupancy_text)

    # getting queing
    for gym in all_divs:
        queuing = gym.find('span', class_ = 'queue_length')
        queuing_text = queuing.text
        list_of_queuing.append(queuing_text)

    driver.close()

    # creation of entire list
    list_of_timings.append(list_of_occupancies)
    list_of_timings.append(list_of_queuing)
    
def print_list(list, index):
    counter = 0
    final_str = []

    now = datetime.now()
    curr_time = now.strftime("%d/%m/%Y %H:%M:%S")
    curr_time_str = "*Accurate as of: " + curr_time + "*\n\n"
 
    for gym in list[0]:
        gym_name = list[0][counter]
        capacity_level = '(' + list[1][counter] + ')'
        capacity_number = list[2][counter]
        cap_str = " with " + capacity_number + " queuing"
        if (capacity_number == '0'):
            cap_str = ''
        final_str.append(gym_name + capacity_level + cap_str + "\n") 
        counter += 1

    if (index < 7):
        return curr_time_str + final_str[index]
    else:
        result_str = final_str[0] + final_str[1] + final_str[2] + final_str[3] + final_str[4] + final_str[5] + final_str[6] 
        return curr_time_str + result_str

def get_all_gyms_text(): 
    crawl(LINK)
    return print_list(list_of_timings, 8)

def get_bishan_text():
    crawl(LINK)
    return print_list(list_of_timings, 0)

def get_century_text():
    crawl(LINK)
    return print_list(list_of_timings, 1)

def get_jcube_text():
    crawl(LINK)
    return print_list(list_of_timings, 2)

def get_keat_text():
    crawl(LINK)
    return print_list(list_of_timings, 3)

def get_kebun_text():
    crawl(LINK)
    return print_list(list_of_timings, 4)

def get_bedok_text():
    crawl(LINK)
    return print_list(list_of_timings, 5)

def get_cnbera_text():
    crawl(LINK)
    return print_list(list_of_timings, 6)

def main():
   # Create updater and pass in Bot's API token.
   updater = Updater(TOKEN, use_context=True)
   # Get dispatcher to register handlers
   dispatcher = updater.dispatcher

   # answer commands
   dispatcher.add_handler(CommandHandler('start', start))
   dispatcher.add_handler(CommandHandler('all', get_all_gyms))
   dispatcher.add_handler(CommandHandler('bishan', get_bishan_gym))
   dispatcher.add_handler(CommandHandler('century', get_century_gym))
   dispatcher.add_handler(CommandHandler('jcube', get_jcube_gym))
   dispatcher.add_handler(CommandHandler('keat', get_keat_gym))
   dispatcher.add_handler(CommandHandler('kebun', get_kebun_gym))
   dispatcher.add_handler(CommandHandler('bedok', get_bedok_gym))
   dispatcher.add_handler(CommandHandler('canberra', get_cnbera_gym))

    # Start the Bot
   updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
   updater.bot.set_webhook(APP_NAME + TOKEN)

   # Run the bot until you press Ctrl-C or the process receives SIGINT,
   # SIGTERM or SIGABRT. This should be used most of the time, since
   # start_polling() is non-blocking and will stop the bot gracefully.
   updater.idle()
   
if __name__ == '__main__':
   main()