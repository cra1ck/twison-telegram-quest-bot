import logging
import json
import os
import quest_macros

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove



# select quest function
def quest_selector(update, context):
    quest_list = os.listdir('./quests/')
    print(f'FILES ON DISK: {quest_list}\n')
    choice_button_column = []
    for i in range(len(quest_list)):
        choice_button_column.append(KeyboardButton(str
        (f'./quests/{quest_list[i]}')))
    choice_keyboard = ReplyKeyboardMarkup.from_column(choice_button_column, one_time_keyboard=True)
    send_keyboard(update, context, choice_keyboard)


def load_quest(update, context):
    story_init = ''
    if(check_id(update.message.from_user.id) == False):
        user_data = [update.message.from_user.id, 0, [], '', {}]
        users.append(user_data)
    input_file = update.message.text
    with open(input_file, "r") as read_file:
        users[find_index(update.message.from_user.id)][3] = json.load(read_file)
    context.bot.send_message(chat_id=update.effective_chat.id, text = str((f'Выбран квест: {users[find_index(update.message.from_user.id)][3]["name"]} \nЧтобы начать приключение используйте /start')))
    for i in range(len(users[find_index(update.message.from_user.id)][3]['passages'])):
        if(users[find_index(update.message.from_user.id)][3]['passages'][i]['name'] == 'StoryInit'):
            story_init = users[find_index(update.message.from_user.id)][3]['passages'][i]['text']
    var = users[find_index(update.message.from_user.id)][4] = quest_macros.macro_set(story_init)
    print(f'StoryInit: {var}')


def send_keyboard(update, context, kboard):
    context.bot.send_message(chat_id=update.effective_chat.id, text='...',reply_markup=kboard)

def quest_answer(update, context):
    if(check_id(update.message.from_user.id) == False):
        user_data = [update.message.from_user.id, 0, [], '', {}]
        users.append(user_data)

    print(f'\nUSER_DATA: {users}')

    data = users[find_index(update.message.from_user.id)][3]
    text = str(update.message.text)
    text = text.strip()
    print('NEW CHOICES:' + str(users[find_index(update.message.from_user.id)][2]))
    print(text)
    for i in range(len(users[find_index(update.message.from_user.id)][2])):
        if(users[find_index(update.message.from_user.id)][2][i].strip() == str(text)):
            users[find_index(update.message.from_user.id)][1]= int(data['passages'][users[find_index(update.message.from_user.id)][1]]['links'][i]['pid'])
            users[find_index(update.message.from_user.id)][1]=users[find_index(update.message.from_user.id)][1]- 1
            list.clear(users[find_index(update.message.from_user.id)][2])
            gameplay(update, context, data)


def check_id(user_id):
    global users
    for i in range(len(users)):
        if(user_id == users[i][0]):
            return True
    return False


def find_index(user_id):
    for i in range(len(users)):
        if(user_id == users[i][0]):
            return i
    return None


## /start command function
def start(update, context):
    if(check_id(update.message.from_user.id) == False):
        user_data = [update.message.from_user.id, 0, [], '', {}]
        users.append(user_data)
    else:
        users[find_index(update.message.from_user.id)][1] = 0
        list.clear(users[find_index(update.message.from_user.id)][2])

    data = users[find_index(update.message.from_user.id)][3]
    print(f'\nDATA: {data}\n')
    if(users[find_index(update.message.from_user.id)][3] == ''):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте, вы можете выбрать историю, которую хотите пережить, используйте /quest')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Квест: ' + str(data['name']) + '\n')
    global pid
    pid = 1
    users[find_index(update.message.from_user.id)][1] = pid - 1
    #users[find_index(update.message.from_user.id)][4] = quest_macros.macro_set(data['passages'][])
    gameplay(update, context, data)

# gameplay
def gameplay(update, context, data):
    global pid
    var = users[find_index(update.message.from_user.id)][4]
    if(users[find_index(update.message.from_user.id)][1]>= 0):
        message = str(data['passages'][users[find_index(update.message.from_user.id)][1]]['text'])
        ##text processing
        #
        #
        #
        local_var = quest_macros.macro_set(message)
        for key in local_var:
            var[key] = local_var[key]
        message = quest_macros.macro_print(message, var)
        print(f'\nlocal_vars = {local_var}')
        print(f'global vars = {var}\n')
        message = message.partition('[')[0]

        print(f'\nTEXT: {message}\n')
        if (not message):
            print('WARNING: empty string')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text = message)

        try:
            for n in range(len(data['passages'][users[find_index(update.message.from_user.id)][1]]['links'])):
                users[find_index(update.message.from_user.id)][2].append(str(data['passages'][users[find_index(update.message.from_user.id)][1]]['links'][n]['name']))
        except KeyError:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "История здесь обрывается, может вы хотите попробывать снова?      /start\nИли выбрать другую историю?     /quest")
            return 0

        choice_button_column = []
        for i in range(len(users[find_index(update.message.from_user.id)][2])):
            choice_button_column.append(KeyboardButton(users[find_index(update.message.from_user.id)][2][i]))

        choice_keyboard = ReplyKeyboardMarkup.from_column(choice_button_column, one_time_keyboard=True)
        send_keyboard(update, context, choice_keyboard)
        dispatcher.add_handler(message_handler)



###### Main program
#
#

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


## Need ./token file to start bot
with open('./.token', 'r') as token_file:
    bot_token = str(token_file.read())
bot_token = bot_token[0:-1]

updater = Updater(token=bot_token, use_context=True)

dispatcher = updater.dispatcher

# user identification
users = []

quest_selector_handler = CommandHandler('quest', quest_selector)
dispatcher.add_handler(quest_selector_handler)

load_quest_handler = MessageHandler(Filters.regex(r'.json'), load_quest)
dispatcher.add_handler(load_quest_handler)

pid = 0

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

message_handler = MessageHandler(Filters.text & (~Filters.command), quest_answer)
dispatcher.add_handler(message_handler)

updater.start_polling()
