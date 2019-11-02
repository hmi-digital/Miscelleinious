from spellchecker import SpellChecker

def init():
    global spell
    spell= SpellChecker()  # loads default word frequency list
    spell.word_frequency.load_text_file('./data/dictionary.txt')

def spellCorrect(utterance):
    words = []
    for word in utterance.split():
        words.append(spell.correction(word.lower()))
    return " ".join(words)