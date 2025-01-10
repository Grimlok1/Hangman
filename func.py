from random_word import Wordnik

def get_word():
    # return one random word 
    wordnik_service = Wordnik()
    word = wordnik_service.get_random_word(hasDictionaryDef="true",
    includePartOfSpeech="noun", maxLength=10)
    return word 

def find_all(original_list, value):
    # Find all indices of a specific value (e.g., 2)
    indices = [index for index, element in enumerate(original_list) if element == value]
    return indices
