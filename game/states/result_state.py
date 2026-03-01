import pygame
from .base_state import BaseState 

class ResultState(BaseState):
    def __init__(self, game, results_data):
        super().__init__(game)
        self.results = results_data

    def enter(self):
        self.font_large = pygame.font.Font('LuckiestGuy-Regular.ttf', 120)
        self.font_small = pygame.font.Font('LuckiestGuy-Regular.ttf', 30)
        self.font_score = pygame.font.Font('LuckiestGuy-Regular.ttf', 80)

        hits = self.results["hits"]
        misses = self.results["misses"]

        # Accuracy
        self.accuracy = self.results["accuracy"]

        # Reaction metrics
        self.avg_reaction = self.results["avg_reaction"]
        self.best_reaction = self.results["best_reaction"]
            

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
        screen.fill((129,2,31))

        center_x = self.game.width // 2
        y = 80

        # Title
        title = self.font_large.render("RESULTS", True, (245,238,205))
        screen.blit(title, title.get_rect(center=(center_x, y)))
        y += 120

        # Score
        score_text = self.font.render(
            f"Final Score: {self.results['score']}",
            True,
            (129,2,31)
        )
        score_rect = score_text.get_rect(center=(center_x, y))
        border_rect = score_rect.inflate(52, 28)
        border_rect.y -= 8
        pygame.draw.rect(screen, (245,238,205), border_rect, border_radius=40)
        screen.blit(score_text, score_rect)
        y += 80

        combo_text = self.font.render(
            f"Highest Combo: x{self.results.get('combo', 0)}",
            True,
            (245,238,205)
        )
        screen.blit(combo_text, combo_text.get_rect(center=(center_x, y)))
        y += 70

        # Hits / Misses
        hits_text = self.font_small.render(
            f"Hits: {self.results['hits']}  |  Misses: {self.results['misses']}",
            True,
            (245,238,205)
        )
        screen.blit(hits_text, hits_text.get_rect(center=(center_x, y)))
        y += 80

        # Accuracy
        accuracy_text = self.font_small.render(
            f"Accuracy: {self.accuracy:.1f}%",
            True,
            (245,238,205)
        )
        screen.blit(accuracy_text, accuracy_text.get_rect(center=(center_x, y)))
        y += 80

        # Reaction times
        avg_text = self.font_small.render(
            f"Average Reaction: {self.avg_reaction:.3f}s",
            True,
            (245,238,205)
        )
        screen.blit(avg_text, avg_text.get_rect(center=(center_x, y)))
        y += 80

        best_text = self.font_small.render(
            f"Best Reaction: {self.best_reaction:.3f}s",
            True,
            (245,238,205)
        )
        screen.blit(best_text, best_text.get_rect(center=(center_x, y)))
        y += 80

        # Instructions
        restart_text = self.font.render(
            "Press ENTER to Restart | ESC to Quit",
            True,
            (245,238,205)
        )
        screen.blit(restart_text, restart_text.get_rect(center=(center_x, y)))
