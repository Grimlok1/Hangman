import sys

import pygame
from engine import StateMachine
from game_states import *

pygame.init()
screen = pygame.display.set_mode((800, 600)) # 800, 400 old
running = True

state_machine = Game(screen)
states = {
        "play": Play(state_machine),
        "main_menu" : MainMenu(state_machine),
        "credits" : Credits(state_machine),
        "high_score" : HighScore(state_machine),
        "game_over" : Game_over(state_machine),
        "settings" : Settings(state_machine)
        }
state_machine.states = states
state_machine.state = states["Main menu"] #set starting state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #press x to quit
            running = False 
        state_machine.handle_events(event)
        
    state_machine.process()
    state_machine.draw()
    pygame.display.update()
    pygame.time.Clock().tick(60)
pygame.quit()
sys.exit()