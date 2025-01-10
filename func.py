from random_word import RandomWords

def get_word():
    # return one random word 
    r = RandomWords()
    return r.get_random_word()

def find_all(original_list, value):
    # Find all indices of a specific value (e.g., 2)
    indices = [index for index, element in enumerate(original_list) if element == value]
    return indices
