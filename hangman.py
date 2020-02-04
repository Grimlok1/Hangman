#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      milo
#
# Created:     18/01/2020
# Copyright:   (c) milo 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def read_from_file():
    with open("fruit_alphabets.txt") as file:
        data = file.readlines()
        return data

def main():
     import string
     data = read_from_file()
     import random
     secret_word = random.choice(data)
     secret_word = secret_word.rstrip("\n")
     print(secret_word)

     name = input("Hello, what is your name?")
     print("Hello %s, Time to play some hangman, i hope you dont leave me hanging, Hahaha! kill me! "%name)
     print("Ok for real, start guessing")
     guesses = ""
     turns = 6
     while turns > 0:
        failed = 0
        for char in secret_word:
            if char in guesses:
                print(char, end = "")
            else:
                print("_ ", end = "")
                failed += 1
        if failed == 0:
            print("\nHeh, i knew i could count on you, You Win!")
            break
        guess = input("guess a character")
        guesses += guess
        if guess not in secret_word:
            turns -= 1
            print("ouch, Wrong!")
            print("you have %s guesses left, make em count!"%turns)
            if turns == 0:
                print("My wish has come true, you lost i die the end")











if __name__ == '__main__':
    main()
