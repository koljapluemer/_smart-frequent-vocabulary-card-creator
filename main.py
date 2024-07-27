import dearpygui.dearpygui as dpg
import os
import random

DATA_FILE = "data/en_frequent_words.txt"


def main():

    dpg.create_context()
    dpg.create_viewport(title='Smart Frequent Vocabulary Card Creator', width=600, height=300)

    with dpg.window(label="Example Window", tag="Primary Window"):
        word = get_random_new_word()
        dpg.add_text("Find the translation of this word in your target language:")
        dpg.add_text(word)


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
