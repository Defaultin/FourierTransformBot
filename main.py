from tools import DFT as dft
from tools import PSPNet as pspn
from tools import data_tools as data
from tools import languages
import telebot
import logging
import os


APPROX = 80
FRAMES = 250

users_for_neuroproceccing = set()
user_language = data.load_dataset()
pspn_model, class_colors = pspn.load_PSPNet()
bot = telebot.TeleBot('894784788:AAGnH46A1qWl5TTSXs-zsGlQzo0F-Dw-tSg')

hide_keyboard = telebot.types.ReplyKeyboardRemove()
lang_keyboard = telebot.types.ReplyKeyboardMarkup(True, True, True)
lang_keyboard.row('Русский 🇷🇺', 'English 🇬🇧', 'Deutsch 🇩🇪')

keyboards = [telebot.types.ReplyKeyboardMarkup(True, True, True)] * 3
keyboards[0].row('№1 👍', '№2 👍', 'НИЧЕГО 👎')
keyboards[1].row('№1 👍', '№2 👍', 'NOTHING 👎')
keyboards[2].row('№1 👍', '№2 👍', 'NICHTS 👎')

neuro_keyboards = [telebot.types.ReplyKeyboardMarkup(True, True)] * 3
neuro_keyboards[0].row('ДА 👍', 'НЕТ 👎')
neuro_keyboards[1].row('YES 👍', 'NO 👎')
neuro_keyboards[2].row('JA 👍', 'NEIN 👎')


def send_start_info(chat_id):
    bot.send_message(chat_id, languages[user_language[chat_id]]['start_1'])
    with open('media/start.mp4', 'rb') as video:
        bot.send_video(chat_id, video)
    bot.send_message(chat_id, languages[user_language[chat_id]]['start_2'])


@bot.message_handler(commands=['start'])
def bot_start(message):
    user_language.update(data.load_dataset())
    if message.chat.id not in user_language:
        user_language[message.chat.id] = 1
        data.save_dataset(user_language)
    bot.send_message(message.chat.id, languages[user_language[message.chat.id]]['language'], reply_markup=lang_keyboard)


@bot.message_handler(commands=['help'])
def bot_help(message):
    user_language.update(data.load_dataset())
    send_start_info(message.chat.id)


@bot.message_handler(commands=['commands'])
def bot_commands(message):
    user_language.update(data.load_dataset())
    bot.send_message(message.chat.id, languages[user_language[message.chat.id]]['commands'])


@bot.message_handler(commands=['language'])
def bot_language(message):
    user_language.update(data.load_dataset())
    bot.send_message(message.chat.id, languages[user_language[message.chat.id]]['language'], reply_markup=lang_keyboard)


@bot.message_handler(commands=['examples'])
def bot_examples(message):
    user_language.update(data.load_dataset())
    examples = [
        open('media/001.jpg', 'rb'),
        open('media/002.jpg', 'rb'),
        open('media/003.jpg', 'rb'),
        open('media/004.jpg', 'rb'),
        open('media/005.jpg', 'rb'),
        open('media/006.jpg', 'rb'),
        open('media/007.jpg', 'rb'),
        open('media/008.jpg', 'rb'),
        open('media/009.jpg', 'rb'),
        open('media/010.jpg', 'rb')
    ]
    medias = [telebot.types.InputMediaPhoto(ex, f"Example №{i}") for i, ex in enumerate(examples)]
    bot.send_media_group(message.chat.id, medias)
    for example in examples:
        example.close()


@bot.message_handler(commands=['about'])
def bot_about(message):
    user_language.update(data.load_dataset())
    bot.send_message(message.chat.id, languages[user_language[message.chat.id]]['about'])
    with open('media/formula.jpg', 'rb') as formula:
        bot.send_photo(message.chat.id, formula)


@bot.message_handler(commands=['approx'])
def bot_about(message):
    global APPROX
    approx = message.text.replace('/approx', '').strip()
    APPROX = int(approx) if approx else APPROX
    bot.send_message(message.chat.id, f'approx = {APPROX}')


@bot.message_handler(commands=['frames'])
def bot_about(message):
    global FRAMES
    frames = message.text.replace('/frames', '').strip()
    FRAMES = int(frames) if frames else FRAMES
    bot.send_message(message.chat.id, f'frames = {FRAMES}')


@bot.message_handler(content_types=['photo'])
def bot_get_photo(message):
    user_language.update(data.load_dataset())
    chat_id = message.chat.id
    language = user_language[chat_id]
    bot.send_message(chat_id, languages[language]['photo_1'])
    
    with open(f'{chat_id}_befor1.jpg', 'wb') as new_file:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        new_file.write(downloaded_file)

    try:
        dft.get_contours(f'{chat_id}_befor1.jpg', ID=chat_id)
        with open(f'{chat_id}_after.jpg', 'rb') as processed_image:
            bot.send_photo(chat_id, processed_image)
        bot.send_message(chat_id, languages[language]['photo_2'], reply_markup=keyboards[language])

    except Exception as e:
        bot.send_message(chat_id, languages[language]['error'], reply_markup=hide_keyboard)
        logging.error(e)
        os.remove(f'{chat_id}_befor1.jpg')
        os.remove(f'{chat_id}_befor2.jpg')


@bot.message_handler(content_types=['text'])
def bot_get_text(message):
    user_language.update(data.load_dataset())
    chat_id = message.chat.id
    language = user_language[chat_id]

    if message.text == "№1 👍":
        if chat_id in users_for_neuroproceccing:
            users_for_neuroproceccing.remove(chat_id)
        bot.send_message(chat_id, languages[language]['text_1'], reply_markup=hide_keyboard)
        try:
            dft.get_ani(f'{chat_id}_befor1.jpg', ID=chat_id, approx_level=APPROX, frames=FRAMES)
            with open(f'{chat_id}_Fourier.mp4', 'rb') as result_video:
                bot.send_video(chat_id, result_video)
            os.remove(f'{chat_id}_Fourier.mp4')
        except Exception as e:
            bot.send_message(chat_id, languages[language]['error'], reply_markup=hide_keyboard)
            logging.error(e)
        finally:
            os.remove(f'{chat_id}_befor1.jpg')
            os.remove(f'{chat_id}_befor2.jpg')
            os.remove(f'{chat_id}_after.jpg')

    elif message.text == "№2 👍":
        if chat_id in users_for_neuroproceccing:
            users_for_neuroproceccing.remove(chat_id)
        bot.send_message(chat_id, languages[language]['text_1'], reply_markup=hide_keyboard)
        try:
            dft.get_ani(f'{chat_id}_befor2.jpg', ID=chat_id, approx_level=APPROX, frames=FRAMES)
            with open(f'{chat_id}' + '_Fourier.mp4', 'rb') as result_video:
                bot.send_video(chat_id, result_video)
            os.remove(f'{chat_id}_Fourier.mp4')
        except Exception as e:
            bot.send_message(chat_id, languages[language]['error'], reply_markup=hide_keyboard)
            logging.error(e)
        finally:
            os.remove(f'{chat_id}_befor1.jpg')
            os.remove(f'{chat_id}_befor2.jpg')
            os.remove(f'{chat_id}_after.jpg')

    elif message.text == "НИЧЕГО 👎" or message.text == "NOTHING 👎" or message.text == "NICHTS 👎":
        if chat_id not in users_for_neuroproceccing:
            bot.send_message(chat_id, languages[language]['text_4'], reply_markup=neuro_keyboards[language])
        else:
            bot.send_message(chat_id, languages[language]['text_2'], reply_markup=hide_keyboard)
            os.remove(f'{chat_id}_befor1.jpg')
            os.remove(f'{chat_id}_befor2.jpg')
            os.remove(f'{chat_id}_after.jpg')
            users_for_neuroproceccing.remove(chat_id)

    elif message.text == "ДА 👍" or message.text == "YES 👍" or message.text == "JA 👍":
        bot.send_message(chat_id, languages[language]['text_5'], reply_markup=hide_keyboard)
        try:
            pspn.start_neuro_segmentation(f'{chat_id}_befor1.jpg', pspn_model, class_colors, ID=chat_id)
            dft.color_correction(f'{chat_id}_befor1.jpg', ID=chat_id, reverse=True, out_name='befor1')
            dft.get_contours(f'{chat_id}_befor1.jpg', ID=chat_id)
            with open(f'{chat_id}_after.jpg', 'rb') as processed_image:
                bot.send_photo(chat_id, processed_image)
            users_for_neuroproceccing.add(chat_id)
            bot.send_message(chat_id, languages[language]['photo_2'], reply_markup=keyboards[language])
        except Exception as e:
            bot.send_message(chat_id, languages[language]['error'], reply_markup=hide_keyboard)
            logging.error(e)
            os.remove(f'{chat_id}_befor1.jpg')
            os.remove(f'{chat_id}_befor2.jpg')
            os.remove(f'{chat_id}_after.jpg')

    elif message.text == "НЕТ 👎" or message.text == "NO 👎" or message.text == "NEIN 👎":
        bot.send_message(chat_id, languages[language]['text_2'], reply_markup=hide_keyboard)
        os.remove(f'{chat_id}_befor1.jpg')
        os.remove(f'{chat_id}_befor2.jpg')
        os.remove(f'{chat_id}_after.jpg')

    elif message.text == "Русский 🇷🇺":
        user_language[chat_id] = 0
        data.save_dataset(user_language)
        bot.send_message(chat_id, "Установлен русский язык.", reply_markup=hide_keyboard)
        send_start_info(chat_id)

    elif message.text == "English 🇬🇧":
        user_language[chat_id] = 1
        data.save_dataset(user_language)
        bot.send_message(chat_id, "English language is installed.", reply_markup=hide_keyboard)
        send_start_info(chat_id)

    elif message.text == "Deutsch 🇩🇪":
        user_language[chat_id] = 2
        data.save_dataset(user_language)
        bot.send_message(chat_id, "Deutsche Sprache ausgewählt.", reply_markup=hide_keyboard)
        send_start_info(chat_id)

    elif message.text.lower().startswith('thank') or message.text.lower().startswith('спасиб') or message.text.lower().startswith('dank'):
        bot.send_message(chat_id, languages[language]['text_3'])

    else:
        bot.reply_to(message, languages[language]['other'])


@bot.message_handler(func=lambda message: True, content_types=['document', 'audio', 'sticker', 'voice'])
def bot_get_other(message):
    user_language.update(data.load_dataset())
    bot.reply_to(message, languages[user_language[message.chat.id]]['other'])


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
    finally:
        exit()