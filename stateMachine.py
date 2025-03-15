class StateMachine:
    def __init__(self, screen):
            self.states = None
            self.screen = screen
            self.state = None 
            
    def handle_events(self, event):
        self.state.handle_event(event)
        
    def process(self):
        self.state.process()
        
    def draw(self):
        self.state.draw()
        
    def transition_state(self, state):
        self.state = self.states[state]
        self.state.transition_state()

class State:
    def __init__(self, state_machine):
        self.state_machine = state_machine  # Store reference to the state machine
        
    def handle_event(self, event):
        pass

    def transition_state(self): #fired when you first transison to statet
        pass

    def update(self):
        pass
        
    def process(self):
        pass

    def draw(self, screen):
        pass