from peewee import *

def main():
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

    # print all Vocab records
    for vocab in Vocab.select():
        print(vocab.native, vocab.target)

if __name__ == '__main__':
    main()