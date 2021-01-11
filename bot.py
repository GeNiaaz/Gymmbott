import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import os
from os import environ
from datetime import datetime
from pytz import timezone
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

logger = logging.getLogger(__name__)

# PORT = int(os.environ.get('PORT', '8443'))
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

# list creation
list_of_timings = [["Bishan ", "Century ", "JCube  ",
                    "Keat   ", "Kebun  ", "Bedok  ", "Canberra "]]
# url to crawl
LINK = "https://smartentry.org/status/gymmboxx"

# token and app name
TOKEN = "1451957453:AAH4MqtpohxSjJfKJPE1ufjXcaB6jgM2tPY"
# APP_NAME = os.environ.get("APP_NAME")

START_MESSAGE = "*I can send you current gymmboxx capacities!!*\n" + \
                "_I am in no way affliated to gymmboxx, just a fan  :)_\n\n" + \
                "Get capacity for\n" + \
                "/all : all gymmboxx\n" + \
                "/bishan : Bishan gymmboxx\n" + \
                "/century : Century Square gymmboxx\n" + \
                "/jcube : Jcube gymmboxx\n" + \
                "/keat : Keat Hong gymmboxx\n" + \
                "/kebun : Kebun Baru gymmboxx\n" + \
                "/bedok : Bedok Point gymmboxx\n" + \
                "/canberra : Canberra gymmboxx"

# Variable creation for scheduler
Days, Hour, Gym = range(3)

Days_str = ''
Hour_str = ''
Gym_str  = ''
schedule_status = False


# chromedriver setup
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
'''
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text=START_MESSAGE, parse_mode='Markdown')


def get_all_gyms(update, context):
    str = get_all_gyms_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_bishan_gym(update, context):
    str = get_bishan_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_century_gym(update, context):
    str = get_century_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_jcube_gym(update, context):
    str = get_jcube_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_keat_gym(update, context):
    str = get_keat_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_kebun_gym(update, context):
    str = get_kebun_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_bedok_gym(update, context):
    str = get_bedok_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


def get_cnbera_gym(update, context):
    str = get_cnbera_text()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=str, parse_mode='Markdown')


# Schedule functions
def schedule_handler(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="What days would you like to schedule the updates for?\n" + \
        "eg, `1 3 5` would be monday, wednesday and friday", 
        parse_mode='Markdown')
    return Days


def days(update, context):
    print("days: ", update.message.text)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Which hour of the day would you like to schedule the updates for?\n" + \
        "eg, `10` for 10am, or `14` for 2pm", 
        parse_mode='Markdown')
    return Hour


def hour(update, context):
    print("hour: ", update.message.text)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Which gym would you like to schedule the updates for?\n" + \
        "eg, `bishan` for bishan gym, or `all` for all gyms", 
        parse_mode='Markdown')
    return Gym


def gym(update, context):
    print("gym: ", update.message.text)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Okay, your schedule has been saved!", 
        parse_mode='Markdown')
    return ConversationHandler.END

def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="Scheduled message has been cancelled")
    return ConversationHandler.END


'''
Args: website_link = string; link of website to be crawled
        link_class = string; class name for job link on website
Returns: jobs_link = list; list of jobs
'''


def crawl(link):
    driver.get(link)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find_all('div', class_='box col-lg-4 col-md-6 col-sm-12')

    # list creation
    list_of_occupancies = []
    list_of_queuing = []

    # getting occupancy
    for gym in all_divs:
        occupancy = gym.find('span', class_='occupancy')
        occupancy_text = occupancy.text
        list_of_occupancies.append(occupancy_text)

    # getting queing
    for gym in all_divs:
        queuing = gym.find('span', class_='queue_length')
        queuing_text = queuing.text
        list_of_queuing.append(queuing_text)

    # creation of entire list
    list_of_timings.append(list_of_occupancies)
    list_of_timings.append(list_of_queuing)


def print_list(list, index):
    counter = 0
    final_str = []

    now_USA = datetime.now(timezone('US/Pacific'))
    now_SG = now_USA.astimezone(timezone('Asia/Singapore'))

    curr_time = now_SG.strftime("%d/%m/%Y %H:%M:%S")
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

    list_of_timings = [["Bishan ", "Century ", "JCube  ",
                        "Keat   ", "Kebun  ", "Bedok  ", "Canberra "]]

    if (index < 7):
        return curr_time_str + final_str[index]
    else:
        result_str = final_str[0] + final_str[1] + final_str[2] + \
            final_str[3] + final_str[4] + final_str[5] + final_str[6]
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

    # list_of_timings = [["Bishan ", "Century ", "JCube  ", "Keat   ", "Kebun  ", "Bedok  ", "Canberra "]]

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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("schedule", schedule_handler)],
        states={
            Days: [MessageHandler(filters=None, callback=days)],
            Hour: [MessageHandler(filters=None, callback=hour)],
            Gym : [MessageHandler(filters=None, callback=gym)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dispatcher.add_handler(conv_handler)

    # log all errors
    dispatcher.add_error_handler(error)


    # CODE TO RUN LOCALLY
    updater.start_polling()
    updater.idle()



    '''
    CODE FOR HEROKU
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
   '''

if __name__ == '__main__':
    main()
