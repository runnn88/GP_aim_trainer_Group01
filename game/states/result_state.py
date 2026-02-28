import pygame
from .base_state import BaseState 

class ResultState(BaseState):
    def __init__(self, game, results_data):
        super().__init__(game)
        self.results = results_data

    def enter(self):
        self.font_large = pygame.font.Font('LuckiestGuy-Regular.ttf', 120)
        self.font_small = pygame.font.Font('LuckiestGuy-Regular.ttf', 60)

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
        screen.fill((129,2,31))

        center_x = self.game.width // 2
        y = 120

        # Title
        title = self.font_large.render("RESULTS", True, (245,238,205))
        screen.blit(title, title.get_rect(center=(center_x, y)))
        y += 120

        # Score
        score_text = self.font.render(
            f"Final Score: {self.results['score']}",
            True,
            (245,238,205)
        )
        screen.blit(score_text, score_text.get_rect(center=(center_x, y)))
        y += 70

        combo_text = self.font.render(
            f"Highest Combo: x{self.results.get('combo', 0)}",
            True,
            (245,238,205)
        )
        screen.blit(combo_text, combo_text.get_rect(center=(center_x, y)))
        y += 70

        # Hits / Misses
        hits_text = self.font.render(
            f"Hits: {self.results['hits']}  |  Misses: {self.results['misses']}",
            True,
            (245,238,205)
        )
        screen.blit(hits_text, hits_text.get_rect(center=(center_x, y)))
        y += 70

        # Accuracy
        accuracy_text = self.font.render(
            f"Accuracy: {self.accuracy:.1f}%",
            True,
            (245,238,205)
        )
        screen.blit(accuracy_text, accuracy_text.get_rect(center=(center_x, y)))
        y += 70

        # Reaction times
        avg_text = self.font.render(
            f"Average Reaction: {self.avg_reaction:.3f}s",
            True,
            (245,238,205)
        )
        screen.blit(avg_text, avg_text.get_rect(center=(center_x, y)))
        y += 70

        best_text = self.font.render(
            f"Best Reaction: {self.best_reaction:.3f}s",
            True,
            (245,238,205)
        )
        screen.blit(best_text, best_text.get_rect(center=(center_x, y)))
        y += 100

        # Instructions
        restart_text = self.font_small.render(
            "Press ENTER to Main Menu | ESC to Quit",
            True,
            (245,238,205)
        )
        screen.blit(restart_text, restart_text.get_rect(center=(center_x, y)))
