import dearpygui.dearpygui as dpg
import os
import random

DATA_FILE = "data/en_frequent_words.txt"


def main():

    dpg.create_context()
    # add a font registry
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        font_text = dpg.add_font("assets/fonts/Roboto_Condensed/RobotoCondensed-Regular.ttf", 32)
        font_text_large = dpg.add_font("assets/fonts/Roboto_Condensed/RobotoCondensed-Medium.ttf", 64)

    dpg.create_viewport(title='Smart Frequent Vocabulary Card Creator', width=1000, height=600)

    with dpg.window(label="Example Window", tag="Primary Window"):
        dpg.bind_font(font_text)

        word = get_random_new_word()
        dpg.add_text("Find the translation of this word in your target language:")
        word_label = dpg.add_text(word)
        dpg.bind_item_font(word_label, font_text_large)



    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()



# return a random word (line) from data/en_frquent_words
def get_random_new_word():
    with open(DATA_FILE, 'r') as f:
        data = f.read()

    words = data.split("\n")
    return random.choice(words)



if __name__ == '__main__':
    main()
