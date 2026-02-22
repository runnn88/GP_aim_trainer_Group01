import pygame
from .base_state import BaseState 

class PauseState(BaseState):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from game.states import PlayingState
                self.game.state_machine.change(PlayingState(self.game))

    def draw(self, screen):
        screen.fill((100, 100, 100))

        font = pygame.font.SysFont(None, 50)
        text = font.render("PAUSED - Press ENTER", True, (0, 0, 0))

        rect = text.get_rect(center=(
            self.game.width // 2,
            self.game.height // 2
        ))

        screen.blit(text, rect)
