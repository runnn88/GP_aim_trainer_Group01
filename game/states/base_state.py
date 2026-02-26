import pygame
from game.target import Target

# ==================================================
# Base State (All states inherit from this)
# ==================================================
class BaseState:
    def __init__(self, game):
        self.game = game  # Reference to main Game object        
        self.font = pygame.font.Font('PressStart2P.ttf', 50)

    def enter(self):
        """Called when state becomes active."""
        pass

    def exit(self):
        """Called when state is replaced."""
        pass

    def handle_event(self, event):
        """Handle input events."""
        pass

    def update(self, dt):
        """Update logic."""
        pass

    def draw(self, screen):
        """Draw everything for this state."""
        pass
