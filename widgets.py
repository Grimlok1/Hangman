import pygame
from engine import *
from func import get_word

class Score:
    def __init__(self, font, pos, alignment="center"):
        self.score = 0
        self.multiplier = 50
        self.font = font
        self.pos = pos
        self.alignment = alignment

        self.surf = None
        self.rect = None

        self.render() #render score

    def score_guess(self, num_of_correct_letters):
        self.score += num_of_correct_letters * self.multiplier
        self.render()

    def render(self):
        self.surf = self.font.render(f"SCORE: {self.score}", False, "black")
        self.rect = self.surf.get_rect()
        setattr(self.rect, self.alignment, self.pos) #set position

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Alphabet:
    def __init__(self, pos, textures, text_surfaces, callback, alignment="center"):
        self.callback = callback
        self.buttons = []
        self.alphabet = ["A","B","C","D","E","F","G","H",
        "I","J","K","L","M","N","O","P","Q","R","S",
        "T","U","V","W","X","Y","Z"]
        gap = 10
        width_inc = 30 + gap
        height_inc = 30 + gap

        x = 13 * width_inc - gap
        y = 2  * height_inc - gap
        self.rect = pygame.Rect(pos, (x, y)) #create a rectangle that can fit the entire Alphabet
        setattr(self.rect, alignment, pos)  # set rect position

        row = 0
        i = 0

        for letter in self.alphabet:
            if i == 13:
                row += 1 # 
                i = 0
            button = TextureButton((self.rect.x + width_inc * i, self.rect.y + height_inc * row), letter, textures, text_surfaces)
            self.buttons.append(button)
            i += 1
            
    def reset_buttons(self):
        for button in self.buttons:
            button.state = "normal"

    def update(self):
        for button in self.buttons:
            button.update()
            if button.state == "clicked":
                self.callback(button)
                break

    def draw(self, screen):
        #screen.fill("red", self.rect)
        for button in self.buttons:
            button.draw(screen)
      

class HiddenLetter:
    def __init__(self, x, y, char):
        font = pygame.font.Font(None, 20)
        self.char = char
        self.visible = False
        self.rect = pygame.rect.Rect(x, y, 30, 30)
        self.letter = Text1(char, font, "black")
        self.letter.rect.center = self.rect.center # center char

    def draw(self, screen):
        screen.fill("white", self.rect)
        if self.visible:
            screen.blit(self.letter.surf, self.letter.rect)


class HiddenWord:
    def __init__(self, w, h, pos, alignment="center"):
        self.counter = None
        self.hidden_letters = []
        self.word = None
        self.rect = None
        self.pos = pos
        self.alignment = alignment
        self.w = w
        self.h = h
        self.width_inc = self.w + 10
        self.new_word()
            
    def new_word(self):
        self.counter = 0 #clear counter
        self.word = get_word() #get new hidden word
        print(self.word)

        w = len(self.word) * self.width_inc - 10

        self.rect = pygame.Rect((0,0),(w, self.h)) #create a rectangle that can fit the entire word
        setattr(self.rect, self.alignment, self.pos) #set rect position

        for  i, letter in enumerate(self.word): #create hidden letters
            hidden_letter = HiddenLetter(self.rect.w + self.width_inc * i, self.rect.h, letter)
            self.hidden_letters.append(hidden_letter)
        
    def draw(self, screen):
        for hidden_letter in self.hidden_letters:
            hidden_letter.draw(screen)

    def guess_letter(self, guess):
        fully_revealed = False
        new_list = []
        guessed_letters = 0
        for hidden_letter in self.hidden_letters:
            if hidden_letter.char == guess:
                hidden_letter.visible = True
                guessed_letters += 1
            else: #function does need to iterate over letters that are visible
                new_list.append(hidden_letter)
            self.hidden_letters = new_list
        if not self.hidden_letters:
            fully_revealed = True
        return guessed_letters, fully_revealed

class Hangman:
    def __init__(self, pos, alignment="center"):
        self.rect = pygame.rect.Rect((0,0),(200, 200))
        self.pos = pos
        self.alignment = alignment
        self.current_line_index = 0
        setattr(self.rect, self.alignment, self.pos) #set position

        self.hangman_lines = [Line("black", self.rect.bottomleft, self.rect.topleft, 5),
        Line("black", (self.rect.x, self.rect.y + 150), (self.rect.x + 200, self.rect.y + 150), 5),
        Line("black", (self.rect.x + 200, self.rect.y + 150), (self.rect.x + 200, self.rect.y + 200), 5),
        Line("black", (self.rect.x, self.rect.y), (self.rect.x + 125, self.rect.y), 5),
        Line("black", (self.rect.x, self.rect.y + 50), (self.rect.x + 50, self.rect.y), 6),
        Line("black", (self.rect.x + 125, self.rect.y), (self.rect.x + 125, self.rect.y + 35), 5),
        Circle("black", (self.rect.x + 125, self.rect.y + 50), 15, 5),
        Line("black", (self.rect.x + 125, self.rect.y + 65), (self.rect.x + 125, self.rect.y + 100), 5),
        Line("black", (self.rect.x + 125, self.rect.y + 100), (self.rect.x + 110, self.rect.y + 125), 6),
        Line("black", (self.rect.x + 125, self.rect.y + 100), (self.rect.x + 140, self.rect.y + 125), 6),
        Line("black", (self.rect.x + 125, self.rect.y + 75), (self.rect.x + 105, self.rect.y + 90), 6),
        Line("black", (self.rect.x + 125, self.rect.y + 75), (self.rect.x + 145, self.rect.y + 90), 6),
        ]
        self.visible_lines = []

    def add_line(self):
        self.visible_lines.append(self.hangman_lines[self.current_line_index])
        self.current_line_index += 1
        if self.current_line_index == len(self.hangman_lines):
            game_over = True
            return game_over

    def reset_lines(self):
        self.current_line_index = 0
        self.visible_lines = []

    def draw(self, screen):
        for line in self.visible_lines:
            line.draw(screen)

#SETTINGS

class Settings(resource_manager):
    def __init__(self, state, pos, text_surfaces, alignment="topleft"):
        self.state = state

        super().__init__((300, 200), pos, alignment)
        btn1 = TextButton((self.rect.centerx, self.rect.y + 20), "Main Menu", text_surfaces, "center", self.state.main_menu)
        btn2 = TextButton((self.rect.centerx, self.rect.y + 80), "Continue", text_surfaces, "center", self.state.close_menu)
        self.buttons.append(btn1)
        self.buttons.append(btn2)