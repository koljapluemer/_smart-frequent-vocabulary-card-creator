import tkinter as tk
from tkinter import ttk
from pony.orm import *
import random

# Application setup
class App(tk.Tk):
    def define_entities(self):
        class Vocab(self.db.Entity):
            native = Required(str)
            target = Optional(str)
            usage_note = Optional(str)
            transliteration = Optional(str)
            # PROPERTIES TO FILL ONE_BY_ONE
            # word_type is picked from a list at front_end
            word_type = Required(str, default='misc')
            antonyms = Set('Vocab', reverse='antonyms')
            synonyms = Set('Vocab', reverse='synonyms')
            siblings = Set('Vocab', reverse='siblings')
            parents = Set('Vocab', reverse='children')
            children = Set('Vocab', reverse='parents')
            take_emotional_judgement = Optional(str)
            take_last_seen = Optional(str)
            take_closest_occurrence = Optional(str)
            pronunciations = Set('AudioFile')
            images = Set('ImageFile')
            drawing = Optional('DrawingFile')
            # misc
            learn_notes = Set('LearnNote')

        class AudioFile(self.db.Entity):
            path = Required(str)
            vocab = Required('Vocab')

        class ImageFile(self.db.Entity):
            path = Required(str)
            vocab = Required('Vocab')

        class DrawingFile(self.db.Entity):
            path = Required(str)
            vocab = Required('Vocab')

        class LearnNote(self.db.Entity):
            based_on = Set('Vocab')
            # possible type is defined at front end
            note_type = Required(str)
            title = Required(str)
            content = Required(str)
            batch = Required('Batch')

        class Batch(self.db.Entity):
            # numbering conveniently done by pony :)
            notes = Set('LearnNote')

        self.db.generate_mapping(create_tables=True)


    def __init__(self):
        super().__init__()

        self.db = Database()
        self.db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
        self.define_entities()

        self.render_screen()



    @db_session
    def render_screen(self):
        self.title("Language Learning App")
        
        # Set up the theme
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # You can choose a different theme if you like

        # Widgets
        self.native_label = ttk.Label(self, text="", font=("Helvetica", 24))
        self.native_label.pack(padx=20, pady=20)

        self.translation_label = ttk.Label(self, text="Translation:")
        self.translation_label.pack(padx=20, pady=20)

        self.translation_entry = ttk.Entry(self, font=("Helvetica", 18))
        self.translation_entry.pack(padx=20, pady=20)

        self.save_button = ttk.Button(self, text="Save and Next", command=self.save_and_next)
        self.save_button.pack(padx=20, pady=20)
        
        self.current_record = None
        self.load_random_record()

    @db_session
    def load_random_record(self):
        self.records = select(v for v in self.db.Vocab)[:]
        if self.records:
            self.current_record = random.choice(self.records)
            self.native_label.config(text=self.current_record.native)
            self.translation_entry.delete(0, tk.END)
        else:
            self.native_label.config(text="No records found")
            self.current_record = None

    @db_session
    def save_and_next(self):
        if self.current_record:
            self.current_record.target = self.translation_entry.get()
            self.load_random_record()

if __name__ == "__main__":
    app = App()
    app.mainloop()
