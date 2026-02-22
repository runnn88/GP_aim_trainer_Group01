import pygame
from .base_state import BaseState 

class StartState(BaseState):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from game.states import PlayingState
                self.game.state_machine.change(PlayingState(self.game))

            if event.key == pygame.K_ESCAPE:
                self.game.running = False

    def draw(self, screen):
        screen.fill((30, 30, 80))

        font = pygame.font.SysFont(None, 60)
        text = font.render("START SCREEN", True, (255, 255, 255))

        rect = text.get_rect(center=(
            self.game.width // 2,
            self.game.height // 2
        ))

        screen.blit(text, rect)