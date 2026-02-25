class StateMachine:
    def __init__(self):
        self.states = []
    
    def change(self, new_state):
        if new_state is None:
            print("Error: Trying to move to a None state")
            return 
        self.pop()
        self.push(new_state)

    def push(self, new_state):
        if new_state is None:
            return 
        
        self.states.append(new_state)
        self.states[-1].enter()
        
    def pop(self):
        if len(self.states) > 0:
            self.states[-1].exit()
            self.states.pop()
        
    def handle_event(self, event):
        if len(self.states) > 0:
            self.states[-1].handle_event(event)

    def update(self, dt):
        if len(self.states) > 0:
            self.states[-1].update(dt)

    def draw(self, screen):
        for state in self.states:
            state.draw(screen)