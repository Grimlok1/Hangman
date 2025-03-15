import pygame
import widgets
from engine import *


class Game(StateMachine):
    def __init__(self, screen):
        super().__init__(screen)
        self.score = 100
        self.resource_manager = ResourceManager()
#MAINMENU STATE
class MainMenu(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        #BUTTON SURFACES
        main_menu_surfaces = self.state_machine.resource_manager.text_surfaces["main_menu_button"]
        #-----------------------------------------------------------------
        #BUTTON FUNCTIONS
        #--------------------------------------------------------------------
        def play():
            self.state_machine.transition_state("play")
        def credits():
            self.state_machine.transition_state("credits")
        def quit_game():
            pygame.quit()
            exit()
        def high_score():
            self.state_machine.transition_state("high_score")
        #---------------------------------------------------------------------
        #BUTTONS
        #---------------------------------------------------------------------
        txt_btn1 = TextButton((400, 200), "PLAY", main_menu_surfaces, "center", play)
        txt_btn2 = TextButton((400, 300), "CREDITS", main_menu_surfaces, "center", credits)
        txt_btn3 = TextButton((400, 400), "HIGHSCORE", main_menu_surfaces, "center", high_score)
        txt_btn4 = TextButton((400, 500), "QUIT", main_menu_surfaces, "center", quit_game)

        #Store buttons in a list
        self.buttons = {txt_btn1, txt_btn2, txt_btn3, txt_btn4}

    #update all the buttons
    def update(self):
        for btn in self.buttons:
            btn.update()

    #draw everything                 
    def draw(self):
        self.screen.fill("pink") #Placeholder background
        for btn in self.buttons:
            btn.draw(self.screen)

#NEEDS TO REFACTOR THIS STATE
class HighScore(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.font = pygame.font.Font(size=35)
        self.font2 = pygame.font.Font(size=60)
        self.screen = self.state_machine.screen

        self.hs_list = [400, 300, 200, 200, 100, 100, 50, 0, 0, 0] #test list, is in order
        self.render_hs = []
        self.numbers = []

        self.rect = pygame.Rect(0, 0, 300, 400)
        self.rect.midtop = (400, 50)

        self.new_score = None #updated when you get a new high score
        self.timer = widgets.Timer(10, self.stop) #timer for how long the text will blink
        self.timer2 = widgets.Timer(0.5, self.blink) #timer for how fast the text will blinking.

        #render shit
        self.title = widgets.Text("HIGH SCORE", self.font2, "white", (400, 5), "midtop")
        self.render_hs.append(widgets.Text(f"{self.hs_list[0]}", self.font, "white", self.rect.topright, "topright")) #starting score, used to put the rest.
        self.numbers.append(widgets.Text("1.", self.font, "white", self.rect.topleft, "topleft"))

        for score in self.hs_list[1:]: #skip first
            prev_rect = self.render_hs[-1].rect
            self.render_hs.append(widgets.Text(f"{score}", self.font, "white", (prev_rect.right, prev_rect.bottom + 5), "topright"))

        for i in range(2, 11): # 2 - 10
            prev_rect = self.numbers[-1].rect
            self.numbers.append(widgets.Text(f"{i}.", self.font, "white", (prev_rect.centerx, prev_rect.bottom + 5), "midtop"))

    #render highscore        
    def render_all(self):
        for i, text in enumerate(self.render_hs):
            text.text = f"{self.hs_list[i]}"
            text.render()

    #handle inputs here
    def handle_event(self, event):           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")

            elif event.key == pygame.K_RETURN: #change state to main_menu
                self.add_score(350)
                self.start_timer()

    #function for adding the score
    def add_score(self, new_score): #too tired to work on this you must re-render all score after adding a new one
        for i, text in enumerate(self.render_hs):
            if int(new_score) > int(text.text): #compare scores, if score is bigger than old one -->
                self.new_score = text
                self.hs_list.insert(i, new_score) #add new score
                self.hs_list.pop() #remove last score
                text.color = "black" #paint new score as black
                self.render_all() #render scores
                break
    #function that executes when the timer stops
    def stop(self):
        self.new_score.color = "white"
        self.new_score.render()

    #function for handling text blinking
    def blink(self):
        if self.new_score.color == "white":
            self.new_score.color = "black"
        else:
            self.new_score.color = "white"
        self.new_score.render()
        self.timer2.start() #restart timer

    #function for starting the timer. set when you get new highscore
    def start_timer(self):
        self.timer.start() #first timer set how long the text will blink
        self.timer2.start() #second sets how fast the text will blink

    #update the timer every frame
    def process(self):
        self.timer.update()
        if self.timer.running:
            self.timer2.update()

    #draw everything here!
    def draw(self):
        self.screen.fill("pink") #bg
        self.title.blit(self.screen)
        for hs in self.render_hs:
            hs.blit(self.screen)
        for num in self.numbers:
            num.blit(self.screen)
            #self.numbers[i].blit(self.screen)

class Credits(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        font = pygame.font.Font(None, 30)
        self.line = widgets.MultilineText(self.screen, "Game made\nBy\nMilo Komulainen", font, "white", (400, 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")
            
    def draw(self):
        pygame.Surface.fill(self.screen, "pink")
        self.line.blit()

#PLAY STATE
class Play(State): #pass callback functions to Objects!
    def __init__(self, state_machine):
        super().__init__(state_machine)
#TEXTURES AND FONTS AND SURFACES
        self.background = self.state_machine.resource_manager.textures["bg_play"]
        alphabet_button_textures = self.state_machine.resource_manager.button_textures["alphabet_button"]
        alphabet_button_text_surfaces = self.state_machine.resource_manager.button_text_surfaces["alphabet_button"]
        score_font = self.state_machine.resource_manager.fonts["score_font"]
#UI OBJECTS
        self.hidden_word = widgets.HiddenWord(30, 30, (400, 100))
        self.alphabet = widgets.Alphabet((400, 400, alphabet_button_textures, alphabet_button_text_surfaces, self.guess_letter)) ###
        self.score = widgets.Score(score_font, (10, 10), "topleft")
        self.hangman = widgets.Hangman((400, 300))
        #TIMER
        self.timer = Timer()
#FUNCTIONS
    def game_over(self):
        self.state_machine.transition_state("Game over")
        print(self.state_machine.score)

    def new_word(self):
        self.hangman.reset_lines()
        self.hidden_word.new_word()
        self.alphabet.reset_buttons()

    def set_timer(self, duration, callback):
        self.timer.set_callback(duration, callback)
        self.timer.start()

    def guess_letter(self, guess): #callback
        num_of_correct_letters, fully_revealed = self.hidden_word.guess_letter(guess)
        if num_of_correct_letters < 1:
            game_over = self.hangman.add_line() #wrong_aswer
            if game_over:
                self.set_timer(2, self.game_over)
                return
        self.score.score_guess(num_of_correct_letters)
        if fully_revealed:
            self.set_timer(3, self.game_over())

#STATE FUNCTIONS
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Settings")


    def update(self): #handle buttons
        self.timer.update() #delay timer after the player has guessed the correct word
        self.alphabet.update()

    def draw(self):
        self.screen.blit(self.background, (0,0)) #background
        self.hidden_word.draw(self.screen)
        self.alphabet.draw(self.screen)
        self.score.draw(self.screen)
        self.hangman.draw(self.screen)

#GAMEOVER STATE
class GameOver(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        #FONTS
        game_over_font = self.state_machine.resource_manager.fonts["game_over_font"]
        score_font = self.state_machine.resource_manager.fonts["score_font"]
        #TEXT OBJECTS
        self.gameOverTxt = widgets.Text1("GAME OVER", game_over_font, "white")
        self.score = widgets.Text1(f"Score: {self.state_machine.score}", score_font, "white")
        #Reposition Text objects
        self.gameOverTxt.rect.center = (400, 300)
        self.score.rect.midtop = (self.gameOverTxt.rect.centerx, self.gameOverTxt.rect.bottom + 10)

    def draw(self):
        self.screen.fill("black")
        self.screen.blit(self.gameOverTxt.surf, self.gameOverTxt.rect)
        self.screen.blit(self.score.surf, self.score.rect)

    def transition_state(self):
        self.score.text = f"Score: {self.state_machine.score}"
        self.score.render_text()

#SETTINGS STATE
class Settings(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)

        # BUTTON FONTS/TEXTS
        font = pygame.font.Font(size=32)
        font2 = pygame.font.Font(size=20)

        text_on = widgets.TextAttr(font, "black")
        text_off = widgets.TextAttr(font, "gray")
        text_hover = widgets.TextAttr(font, "white")


        self.settings = widgets.Settings(self, (400, 200), btnTexts, "midtop")
        self.paused_txt = widgets.Text1("PAUSED", font2, "black")
        self.paused_txt.rect.topleft = (5, 5)

    #FUNCTIONS
    def close_menu(self):
        self.state_machine.transition_state("Play")

    def main_menu(self):
        self.state_machine.transition_state("Main menu")

    def process(self):
        self.settings.update()

    #STATE FUNCTIONS
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_menu()# change state to main_menu

    def draw(self):
        self.settings.draw(self.state_machine.screen)