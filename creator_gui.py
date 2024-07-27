import tkinter as tk
from tkinter import ttk
from peewee import *
import random


db = SqliteDatabase('vocab.db')
class BaseModel(Model):
    class Meta:
        database = db



class Vocab(BaseModel):
    native = CharField()
    target = CharField(null=True)
    usage_note = TextField(null=True)
    transliteration = CharField(null=True)
    word_type = CharField(default='misc')
    # # PROPERTIES TO FILL ONE_BY_ONE
    take_emotional_judgement = CharField(null=True)
    take_last_seen = CharField(null=True)
    take_closest_occurrence = CharField(null=True)


class AudioFile(BaseModel):
    path = CharField()
    vocab = ForeignKeyField(Vocab, backref='audio_files')

class ImageFile(BaseModel):
    path = CharField()
    vocab = ForeignKeyField(Vocab, backref='image_files')

class DrawingFile(BaseModel):
    path = CharField()
    vocab = ForeignKeyField(Vocab, backref='drawing_files')

# yey, we have to do many2many manually :))))))
class VocabAntonym(BaseModel):
    vocab = ForeignKeyField(Vocab, backref='antonyms')
    antonym = ForeignKeyField(Vocab, backref='antonym_sibling')

class VocabSibling(BaseModel):
    vocab = ForeignKeyField(Vocab, backref='siblings')
    sibling = ForeignKeyField(Vocab, backref='sibling_vocab')

class VocabParent(BaseModel):
    vocab = ForeignKeyField(Vocab, backref='children')
    parent = ForeignKeyField(Vocab, backref='parent_vocab')

class VocabPronunciation(BaseModel):
    vocab = ForeignKeyField(Vocab, backref='pronunciations')
    audio = ForeignKeyField(AudioFile, backref='vocab')

class VocabImage(BaseModel):
    vocab = ForeignKeyField(Vocab, backref='images')
    image = ForeignKeyField(ImageFile, backref='vocab')

class LearnNote(BaseModel):
    title = CharField()
    content = TextField()

class VocabLearnNote(BaseModel):
    vocab = ForeignKeyField(Vocab, backref='learn_notes')
    learn_note = ForeignKeyField(LearnNote, backref='vocab')


db.connect()
db.create_tables([Vocab, AudioFile, ImageFile, DrawingFile])

# Application setup
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.create_demo_rows()
        self.render_screen()
    
    def render_screen(self):
        self.title("Language Learning App")
        
        # Set up the theme
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # You can choose a different theme if you like

        # Widgets
        self.native_label = ttk.Label(self, text="", font=("Helvetica", 24))
        self.native_label.pack(padx=20, pady=20)

        self.translation_label = ttk.Label(self, text="Translation:")
        self.translation_label.pack(padx=20, pady=5)

        self.translation_entry = ttk.Entry(self, font=("Helvetica", 18))
        self.translation_entry.pack(padx=20, pady=20)


        self.pronunciation_label = ttk.Label(self, text="Pronunciation:")
        self.pronunciation_label.pack(padx=20, pady=5)

        self.pronunciation_entry = ttk.Entry(self, font=("Helvetica", 18))
        self.pronunciation_entry.pack(padx=20, pady=20)

        # notes (bigger text field)
        self.notes_label = ttk.Label(self, text="Usage Notes:")
        self.notes_label.pack(padx=20, pady=5)

        self.notes_entry = tk.Text(self, font=("Helvetica", 18), height=5, width=40)
        self.notes_entry.pack(padx=20, pady=20)


        # type of word
        self.word_type = tk.StringVar(None, "misc")
        self.r1 = ttk.Radiobutton(self, text='Noun', value='noun', variable=self.word_type)
        self.r2 = ttk.Radiobutton(self, text='Verb', value='verb', variable=self.word_type)
        self.r3 = ttk.Radiobutton(self, text='Adjective/Adverb', value='ad', variable=self.word_type)
        self.r4 = ttk.Radiobutton(self, text='Other', value='misc', variable=self.word_type)

        self.r1.pack()
        self.r2.pack()
        self.r3.pack()
        self.r4.pack()


        # Buttons
        self.save_button = ttk.Button(self, text="Save and Next", command=self.save_and_next)
        self.save_button.pack(padx=20, pady=20)
        
        self.current_record = None
        self.load_next_record()

    
    def load_next_record(self):
        records = Vocab.select()
        record = self.get_random_record_missing_base_info()
        if record:
            self.current_record = record
            # fill in values from record or delete
            self.native_label.config(text=self.current_record.native)
            self.translation_entry.delete(0, tk.END)
            self.translation_entry.insert(0, self.current_record.target or "")
            self.pronunciation_entry.delete(0, tk.END)
            self.pronunciation_entry.insert(0, self.current_record.transliteration or "")
            self.notes_entry.delete("1.0", tk.END)
            self.notes_entry.insert("1.0", self.current_record.usage_note or "")
            self.word_type.set(self.current_record.word_type or "misc")
        else:
            self.native_label.config(text="No records found")
            self.current_record = None

    def get_random_record_missing_base_info(self):
        # get a record where target prop is unset or ""
        return Vocab.select().where((Vocab.target == "") | (Vocab.target == None)).order_by(fn.Random()).first()
    
    def save_and_next(self):
        if self.current_record:
            self.current_record.target = self.translation_entry.get()
            self.current_record.transliteration = self.pronunciation_entry.get()
            self.current_record.usage_note = self.notes_entry.get("1.0", tk.END)
            self.current_record.word_type = self.word_type.get()
            self.current_record.save()

            self.load_next_record()

    def create_demo_rows(self):
        native_words = ['be', 'and', 'of', 'their', 'she', 'year', 'time', 'take', 'people', 'see', 'red', 'kind', 'politicial']
        # if not exist!!!!!, create db obj for each
        for word in native_words:
            if not Vocab.select().where(Vocab.native == word):
                Vocab.create(native=word)

if __name__ == "__main__":
    app = App()
    app.mainloop()
