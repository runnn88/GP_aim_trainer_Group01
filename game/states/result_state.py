import pygame
from .base_state import BaseState 

class ResultState(BaseState):
    def __init__(self, game, results_data):
        super().__init__(game)
        self.results = results_data

    def enter(self):
        self.font_large = pygame.font.Font('PressStart2P.ttf', 60)
        self.font_small = pygame.font.Font('PressStart2P.ttf', 30)

        hits = self.results["hits"]
        misses = self.results["misses"]
        reactions = self.results["reaction_times"]

        total_attempts = hits + misses

        # Accuracy
        self.accuracy = (hits / total_attempts * 100) if total_attempts > 0 else 0

        # Reaction metrics
        if reactions:
            self.avg_reaction = sum(reactions) / len(reactions)
            self.best_reaction = min(reactions)
        else:
            self.avg_reaction = 0
            self.best_reaction = 0

    # ------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from game.states import StartState
                self.game.state_machine.change(StartState(self.game))

            if event.key == pygame.K_ESCAPE:
                self.game.running = False

    # ------------------------------------------
    def draw(self, screen):
        screen.fill((120, 20, 20))

        center_x = self.game.width // 2
        y = 120

        # Title
        title = self.font_large.render("RESULTS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(center_x, y)))
        y += 80

        # Score
        score_text = self.font_small.render(
            f"Final Score: {self.results['score']}",
            True,
            (255, 255, 255)
        )
        screen.blit(score_text, score_text.get_rect(center=(center_x, y)))
        y += 50

        # Hits / Misses
        hits_text = self.font_small.render(
            f"Hits: {self.results['hits']}  |  Misses: {self.results['misses']}",
            True,
            (255, 255, 255)
        )
        screen.blit(hits_text, hits_text.get_rect(center=(center_x, y)))
        y += 50

        # Accuracy
        accuracy_text = self.font_small.render(
            f"Accuracy: {self.accuracy:.1f}%",
            True,
            (255, 255, 255)
        )
        screen.blit(accuracy_text, accuracy_text.get_rect(center=(center_x, y)))
        y += 50

        # Reaction times
        avg_text = self.font_small.render(
            f"Average Reaction: {self.avg_reaction:.3f}s",
            True,
            (255, 255, 255)
        )
        screen.blit(avg_text, avg_text.get_rect(center=(center_x, y)))
        y += 40

        best_text = self.font_small.render(
            f"Best Reaction: {self.best_reaction:.3f}s",
            True,
            (255, 255, 255)
        )
        screen.blit(best_text, best_text.get_rect(center=(center_x, y)))
        y += 70

        # Instructions
        restart_text = self.font_small.render(
            "Press ENTER to Restart | ESC to Quit",
            True,
            (255, 255, 255)
        )
        screen.blit(restart_text, restart_text.get_rect(center=(center_x, y)))