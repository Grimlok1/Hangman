import pygame
import widgets
import func
from stateMachine import *


class Game(StateMachine):
    def __init__(self, screen):
        super().__init__(screen)
        self.score = 0
    
class MainMenu(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen = self.state_machine.screen
        def play():
            self.state_machine.transition_state("Play")
        def credit():
            self.state_machine.transition_state("Credits")
        def quit_game():
            pygame.quit()
            exit()
        def high_score():
            self.state_machine.transition_state("High score")
            
        tb1 = widgets.TextButton(self.screen,"Play", 50, (400,200), play)
        tb2 = widgets.TextButton(self.screen,"Quit", 50, (400, 350), quit_game, "midbottom")
        tb3 = widgets.TextButton(self.screen,"High Score", 50, (400, tb1.rect.centery + 50), high_score)
        tb4 = widgets.TextButton(self.screen,"Credits", 50, (400, 20), credit, "midtop")
        
        self.buttons = {tb2, tb3, tb1, tb4}
        
    def process(self):
        for button in self.buttons:
            button.process()
            
                
    def draw(self):
        self.screen.fill("pink") #bg
        for btn in self.buttons:
            btn.blit()

class Settings(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen = self.state_machine.screen
        rect = pygame.rect.Rect(0, 0, 300, 350)
        rect.midtop = (400, 25)
        self.widgets.TextButton(self.screen, "Main menu")

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
        self.timer = widgets.Timer(10, self.stop)
        self.timer2 = widgets.Timer(0.5, self.blink)

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

    def render_all(self):
        for i, text in enumerate(self.render_hs):
            text.text = f"{self.hs_list[i]}"
            text.render()

    def handle_event(self, event):           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")

            elif event.key == pygame.K_RETURN: #change state to main_menu
                self.add_score(350)
                self.start_timer()

    def add_score(self, new_score): #too tired to work on this you must re-render all score after adding a new one
        for i, text in enumerate(self.render_hs):
            if int(new_score) > int(text.text): #compare scores, if score is bigger than old one -->
                self.new_score = text
                self.hs_list.insert(i, new_score) #add new score
                self.hs_list.pop() #remove last score
                text.color = "black" #paint new score as black
                self.render_all() #render scores
                break
    def stop(self):
        self.new_score.color = "white"
        self.new_score.render()

    def blink(self):
        if self.new_score.color == "white":
            self.new_score.color = "black"
        else:
            self.new_score.color = "white"
        self.new_score.render()
        self.timer2.start()

    def start_timer(self):
        self.timer.start()
        self.timer2.start()

    def process(self):
        self.timer.update()
        if self.timer.running == True:
            self.timer2.update()


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
        self.screen = self.state_machine.screen
        self.line = widgets.MultilineText(self.screen, "Game made\nBy\nMilo Komulainen", font, "white", (400, 50))
        #self, text, font, pos, color, alignment="left"
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")
            
    def draw(self):
        pygame.Surface.fill(self.screen, "pink")
        self.line.blit()
        
            
class Play(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)

        self.screen = self.state_machine.screen
        bg = pygame.image.load("tausta1.png")
        self.bg = bg.convert()

        basic_font = pygame.font.Font(None, 32)
        box = pygame.Rect(0,0, 30, 30)
        rect = pygame.Rect(0,0, 200,200)

        self.hidden_word = widgets.HiddenWord(box=box, font=basic_font, pos=(400, 25), anchor_point="midtop")
        self.alphabet = widgets.Alphabet(box=box, font=basic_font, pos=(400, 375), anchor_point="midbottom")
        self.score = widgets.Score(font=basic_font, pos=(700, 25), anchor_point="midtop")
        self.hangman = widgets.Hangman(rect=rect, surf=self.screen, pos=(400, self.hidden_word.rect.bottom + 25), anchor_point="midtop")
       

    def handle_event(self, event):           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #change state to main_menu
                self.state_machine.transition_state("Main menu")


    def process(self): #handle buttons
        for button in self.alphabet.buttons:
            if button.active == True:
                if button.is_pressed():
                    button.deactivate() # 
                    self.guess_letter(button)


    def guess_letter(self, button):
        indices = func.find_all(self.hidden_word.word.lower(), button.text.lower()) #find out if the letter you pressed occures in the word
        if indices: #right answer
            for i in indices:
                self.hidden_word.hidden_letters[i].visible = True
                self.score.add_score(50)
                self.hidden_word.counter += 1
                if self.hidden_word.counter == len(self.hidden_word.word): #entire word was revealed
                    self.new_word()
                    self.hangman.reset_lines()
        else: #wrong answer
            self.hangman.add_line()
   
    def new_word(self):
        timer = widgets.Timer()
        self.hidden_word.new_word()
        self.alphabet.reset_buttons()


    def draw(self):
        self.screen.blit(self.bg, (0,0)) #background
        self.hidden_word.blit(self.screen)
        self.alphabet.blit(self.screen)
        self.score.blit(self.screen)
        self.hangman.blit(self.screen)

class Game_over(State):
    def __init__(self, state_machine):
        super().__init__(state_machine)
        self.screen = state_machine.screen
        game_over = pygame.font.Font(None, 60)
        score = pygame.font.Font(None, 30)
        self.line = widgets.Text("GAME OVER",game_over, "white", (400, 200))
        self.score = widgets.Text(f"Score: {state_machine.score}", "white", (self.line.centerx, self.line.bottom + 30))

    def draw(self):
        self.screen.fill("black")


