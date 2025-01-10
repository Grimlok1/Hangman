import pygame
import func
import states as st

pygame.init()
screen = pygame.display.set_mode((800, 400))
running = True

state_machine = st.Game(screen)
states = {
        "Play": st.Play(state_machine),
        "Main menu" : st.MainMenu(state_machine),
        "Credits" : st.Credits(state_machine),
        "High score" : st.HighScore(state_machine)
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