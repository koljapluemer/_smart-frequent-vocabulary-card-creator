import dearpygui.dearpygui as dpg
import os
import random
from pathlib import Path

from PIL import ImageGrab
import PIL
import uuid
import numpy


DATA_FILE = "data/en_frequent_words.txt"

def save_translation(sender, app_data, user_data):
    print("Save button clicked")
    print("Translation: ", dpg.get_value(translation_input))

    # create path user/words if not existing:
    Path("user/words").mkdir(parents=True, exist_ok=True)
    # append "translation: $translation" to file with name of $word
    with open(f"user/words/{word}.txt", "a") as f:
        f.write(f"translation: {dpg.get_value(translation_input)}\n")


# return a random word (line) from data/en_frquent_words
def get_random_new_word():
    with open(DATA_FILE, 'r') as f:
        data = f.read()

    words = data.split("\n")
    return random.choice(words)

def paint_image(img_path):
    width, height, channels, data = dpg.load_image(img_path)
    with dpg.texture_registry(show=True):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
        dpg.add_image("texture_tag")

def grab_translation_image_from_clipboard():
    try:
        im = ImageGrab.grabclipboard()
        Path("user/images").mkdir(parents=True, exist_ok=True)
        img_path = f'user/images/{word}-{uuid.uuid4()}.png'
        im.save(img_path)
        paint_image(img_path)
    except Exception as e:
        print('Grabbing Image from Clipboard Failed:', e)


# DPG STUFF
# seems to hate main functions

dpg.create_context()
# add a font registry
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    font_text = dpg.add_font("assets/fonts/Roboto_Condensed/RobotoCondensed-Regular.ttf", 32)
    font_text_huge = dpg.add_font("assets/fonts/Roboto_Condensed/RobotoCondensed-Medium.ttf", 64)
    font_text_large = dpg.add_font("assets/fonts/Roboto_Condensed/RobotoCondensed-Medium.ttf", 48)


dpg.create_viewport(title='Smart Frequent Vocabulary Card Creator', width=1000, height=600)

with dpg.window(label="Example Window", tag="Primary Window"):
    dpg.bind_font(font_text)

    word = get_random_new_word()
    dpg.add_text("Find the translation of this word in your target language:")
    word_label = dpg.add_text(word + ":")
    dpg.bind_item_font(word_label, font_text_huge)

    # translation input
    translation_input = dpg.add_input_text(label="", default_value="")
    dpg.bind_item_font(translation_input, font_text_large)

    translation_button = dpg.add_button(label="Save", callback=save_translation)
    dpg.bind_item_font(translation_button, font_text_large)

    dpg.bind_font(font_text)

    btn_grab_translation_image_from_clipboard = dpg.add_button(label="Grab translation image from clipboard", callback=grab_translation_image_from_clipboard)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()



