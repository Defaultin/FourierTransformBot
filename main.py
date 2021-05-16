from tools import DFT as dft
from tools import PSPNet as pspn
from tools import data_tools as data
from tools import languages
import telebot
import logging
import os


APPROX = 80
FRAMES = 250


pspn_model, class_colors = pspn.load_PSPNet()
user_language = {}
users_for_neuroproceccing = set()
TOKEN = '894784788:AAGnH46A1qWl5TTSXs-zsGlQzo0F-Dw-tSg'
bot = telebot.TeleBot(TOKEN)
hide_keyboard = telebot.types.ReplyKeyboardRemove()
lang_keyboard = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard_ru = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard_eng = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard_de = telebot.types.ReplyKeyboardMarkup(True, True, True)
neuro_keyboard_ru = telebot.types.ReplyKeyboardMarkup(True, True)
neuro_keyboard_eng = telebot.types.ReplyKeyboardMarkup(True, True)
neuro_keyboard_de = telebot.types.ReplyKeyboardMarkup(True, True)
lang_keyboard.row('Русский 🇷🇺', 'English 🇬🇧', 'Deutsch 🇩🇪')
keyboard_ru.row('№1 👍', '№2 👍', 'НИЧЕГО 👎')
keyboard_eng.row('№1 👍', '№2 👍', 'NOTHING 👎')
keyboard_de.row('№1 👍', '№2 👍', 'NICHTS 👎')
neuro_keyboard_ru.row('ДА 👍', 'НЕТ 👎')
neuro_keyboard_eng.row('YES 👍', 'NO 👎')
neuro_keyboard_de.row('JA 👍', 'NEIN 👎')


def send_start_info(chat_id):
    bot.send_message(chat_id, languages[user_language[chat_id]]['start_1'])
    video = open('media/start.mp4', 'rb')
    bot.send_video(chat_id, video)
    video.close()
    bot.send_message(chat_id, languages[user_language[chat_id]]['start_2'])


@bot.message_handler(commands=['start'])
def bot_start(message):
    user_language.update(data.load_dataset())
    if message.chat.id not in user_language:
        user_language[message.chat.id] = 1
        data.save_dataset(user_language)
    bot.send_message(
        message.chat.id, languages[user_language[message.chat.id]]['language'], reply_markup=lang_keyboard)


@bot.message_handler(commands=['help'])
def bot_help(message):
    user_language.update(data.load_dataset())
    send_start_info(message.chat.id)


@bot.message_handler(commands=['commands'])
def bot_commands(message):
    user_language.update(data.load_dataset())
    bot.send_message(
        message.chat.id, languages[user_language[message.chat.id]]['commands'])


@bot.message_handler(commands=['language'])
def bot_language(message):
    user_language.update(data.load_dataset())
    bot.send_message(
        message.chat.id, languages[user_language[message.chat.id]]['language'], reply_markup=lang_keyboard)


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
    for ex in examples:
        ex.close()


@bot.message_handler(commands=['about'])
def bot_about(message):
    user_language.update(data.load_dataset())
    bot.send_message(
        message.chat.id, languages[user_language[message.chat.id]]['about'])
    formula = open('media/formula.jpg', 'rb')
    bot.send_photo(message.chat.id, formula)
    formula.close()


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
    bot.send_message(
        message.chat.id, languages[user_language[message.chat.id]]['photo_1'])
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    new_file = open(f'{message.chat.id}_befor1.jpg', 'wb')
    new_file.write(downloaded_file)
    new_file.close()
    try:
        dft.get_contours(f'{message.chat.id}_befor1.jpg', ID=message.chat.id)
        processed_image = open(f'{message.chat.id}_after.jpg', 'rb')
        bot.send_photo(message.chat.id, processed_image)
        processed_image.close()
        if user_language[message.chat.id] == 0:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['photo_2'], reply_markup=keyboard_ru)
        elif user_language[message.chat.id] == 1:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['photo_2'], reply_markup=keyboard_eng)
        elif user_language[message.chat.id] == 2:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['photo_2'], reply_markup=keyboard_de)
    except Exception as e:
        bot.send_message(
            message.chat.id, languages[user_language[message.chat.id]]['error'], reply_markup=hide_keyboard)
        logging.error(e)
        os.remove(f'{message.chat.id}_befor1.jpg')
        os.remove(f'{message.chat.id}_befor2.jpg')


@bot.message_handler(content_types=['text'])
def bot_get_text(message):
    user_language.update(data.load_dataset())
    if message.text == "№1 👍":
        if message.chat.id in users_for_neuroproceccing:
            users_for_neuroproceccing.remove(message.chat.id)
        bot.send_message(
            message.chat.id, languages[user_language[message.chat.id]]['text_1'], reply_markup=hide_keyboard)
        try:
            dft.get_ani(f'{message.chat.id}_befor1.jpg',
                        ID=message.chat.id, approx_level=APPROX, frames=FRAMES)
            result_video = open(f'{message.chat.id}_Fourier.mp4', 'rb')
            bot.send_video(message.chat.id, result_video)
            result_video.close()
            os.remove(f'{message.chat.id}_Fourier.mp4')
        except Exception as e:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['error'], reply_markup=hide_keyboard)
            logging.error(e)
        finally:
            os.remove(f'{message.chat.id}_befor1.jpg')
            os.remove(f'{message.chat.id}_befor2.jpg')
            os.remove(f'{message.chat.id}_after.jpg')
    elif message.text == "№2 👍":
        if message.chat.id in users_for_neuroproceccing:
            users_for_neuroproceccing.remove(message.chat.id)
        bot.send_message(
            message.chat.id, languages[user_language[message.chat.id]]['text_1'], reply_markup=hide_keyboard)
        try:
            dft.get_ani(f'{message.chat.id}_befor2.jpg',
                        ID=message.chat.id, approx_level=APPROX, frames=FRAMES)
            result_video = open(f'{message.chat.id}' + '_Fourier.mp4', 'rb')
            bot.send_video(message.chat.id, result_video)
            result_video.close()
            os.remove(f'{message.chat.id}_Fourier.mp4')
        except Exception as e:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['error'], reply_markup=hide_keyboard)
            logging.error(e)
        finally:
            os.remove(f'{message.chat.id}_befor1.jpg')
            os.remove(f'{message.chat.id}_befor2.jpg')
            os.remove(f'{message.chat.id}_after.jpg')
    elif message.text == "НИЧЕГО 👎" or message.text == "NOTHING 👎" or message.text == "NICHTS 👎":
        if message.chat.id not in users_for_neuroproceccing:
            if user_language[message.chat.id] == 0:
                bot.send_message(
                    message.chat.id, languages[user_language[message.chat.id]]['text_4'], reply_markup=neuro_keyboard_ru)
            elif user_language[message.chat.id] == 1:
                bot.send_message(
                    message.chat.id, languages[user_language[message.chat.id]]['text_4'], reply_markup=neuro_keyboard_eng)
            elif user_language[message.chat.id] == 2:
                bot.send_message(
                    message.chat.id, languages[user_language[message.chat.id]]['text_4'], reply_markup=neuro_keyboard_de)
        else:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['text_2'], reply_markup=hide_keyboard)
            os.remove(f'{message.chat.id}_befor1.jpg')
            os.remove(f'{message.chat.id}_befor2.jpg')
            os.remove(f'{message.chat.id}_after.jpg')
            users_for_neuroproceccing.remove(message.chat.id)
    elif message.text == "ДА 👍" or message.text == "YES 👍" or message.text == "JA 👍":
        bot.send_message(
            message.chat.id, languages[user_language[message.chat.id]]['text_5'], reply_markup=hide_keyboard)
        try:
            pspn.start_neuro_segmentation(f'{message.chat.id}_befor1.jpg', pspn_model, class_colors, ID=message.chat.id)
            dft.color_correction(f'{message.chat.id}_befor1.jpg', ID=message.chat.id, reverse=True, out_name='befor1')
            dft.get_contours(f'{message.chat.id}_befor1.jpg', ID=message.chat.id)
            processed_image = open(f'{message.chat.id}_after.jpg', 'rb')
            bot.send_photo(message.chat.id, processed_image)
            processed_image.close()
            users_for_neuroproceccing.add(message.chat.id)
            if user_language[message.chat.id] == 0:
                bot.send_message(
                    message.chat.id, languages[user_language[message.chat.id]]['photo_2'], reply_markup=keyboard_ru)
            elif user_language[message.chat.id] == 1:
                bot.send_message(
                    message.chat.id, languages[user_language[message.chat.id]]['photo_2'], reply_markup=keyboard_eng)
            elif user_language[message.chat.id] == 2:
                bot.send_message(
                    message.chat.id, languages[user_language[message.chat.id]]['photo_2'], reply_markup=keyboard_de)
        except Exception as e:
            bot.send_message(
                message.chat.id, languages[user_language[message.chat.id]]['error'], reply_markup=hide_keyboard)
            logging.error(e)
            os.remove(f'{message.chat.id}_befor1.jpg')
            os.remove(f'{message.chat.id}_befor2.jpg')
            os.remove(f'{message.chat.id}_after.jpg')
    elif message.text == "НЕТ 👎" or message.text == "NO 👎" or message.text == "NEIN 👎":
        bot.send_message(
            message.chat.id, languages[user_language[message.chat.id]]['text_2'], reply_markup=hide_keyboard)
        os.remove(f'{message.chat.id}_befor1.jpg')
        os.remove(f'{message.chat.id}_befor2.jpg')
        os.remove(f'{message.chat.id}_after.jpg')
    elif message.text == "Русский 🇷🇺":
        user_language[message.chat.id] = 0
        data.save_dataset(user_language)
        bot.send_message(
            message.chat.id, "Установлен русский язык.", reply_markup=hide_keyboard)
        send_start_info(message.chat.id)
    elif message.text == "English 🇬🇧":
        user_language[message.chat.id] = 1
        data.save_dataset(user_language)
        bot.send_message(
            message.chat.id, "English language is installed.", reply_markup=hide_keyboard)
        send_start_info(message.chat.id)
    elif message.text == "Deutsch 🇩🇪":
        user_language[message.chat.id] = 2
        data.save_dataset(user_language)
        bot.send_message(
            message.chat.id, "Deutsche Sprache ausgewählt.", reply_markup=hide_keyboard)
        send_start_info(message.chat.id)
    elif message.text.lower().startswith('thank') or message.text.lower().startswith('спасиб') or message.text.lower().startswith('dank'):
        bot.send_message(
            message.chat.id, languages[user_language[message.chat.id]]['text_3'])
    else:
        bot.reply_to(
            message, languages[user_language[message.chat.id]]['other'])


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