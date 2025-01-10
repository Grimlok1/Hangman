import random
from words import mylist
    
def get_word():
    word = random.choice(mylist)
    return word

def find_all(original_list, value):
    # Find all indices of a specific value (e.g., 2)
    indices = [index for index, element in enumerate(original_list) if element == value]
    return indices