class StateMachine:
    def __init__(self):
        self.current_state = None

    # ------------------------------------------
    # Change State
    # ------------------------------------------
    def change(self, new_state):
        if self.current_state is not None:
            self.current_state.exit()

        self.current_state = new_state

        if self.current_state is not None:
            self.current_state.enter()

    # ------------------------------------------
    # Event Handling
    # ------------------------------------------
    def handle_event(self, event):
        if self.current_state is not None:
            self.current_state.handle_event(event)

    # ------------------------------------------
    # Update
    # ------------------------------------------
    def update(self, dt):
        if self.current_state is not None:
            self.current_state.update(dt)

    # ------------------------------------------
    # Draw
    # ------------------------------------------
    def draw(self, screen):
        if self.current_state is not None:
            self.current_state.draw(screen)