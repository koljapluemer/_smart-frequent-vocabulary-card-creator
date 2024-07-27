from pony.orm import *

def define_entities(db):
    class Vocab(db.Entity):
        native = Required(str)
        target = Required(str)
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

    class AudioFile(db.Entity):
        path = Required(str)
        vocab = Required('Vocab')

    class ImageFile(db.Entity):
        path = Required(str)
        vocab = Required('Vocab')
    
    class DrawingFile(db.Entity):
        path = Required(str)
        vocab = Required('Vocab')
    
    class LearnNote(db.Entity):
        based_on = Set('Vocab')
        # possible type is defined at front end
        note_type = Required(str)
        title = Required(str)
        content = Required(str)
        batch = Required('Batch')

    class Batch(db.Entity):
        # numbering conveniently done by pony :)
        notes = Set('LearnNote')

    db.generate_mapping(create_tables=True)
    

def main():
    # init database
    db = Database()
    db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
    define_entities(db)


if __name__ == '__main__':
    main()