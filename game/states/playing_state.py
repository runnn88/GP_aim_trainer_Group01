import pygame
from .base_state import BaseState 
from game.target import Target

class PlayingState(BaseState):
    def enter(self):
        self.duration = 60
        self.time_left = self.duration

        self.font = pygame.font.SysFont(None, 36)

        # Stats
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.reaction_times = []

        # Target
        self.target = Target(self.game, radius=30, ttl=1.5)
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    # ------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from game.states import PauseState
                self.game.state_machine.push(PauseState(self.game))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.target.is_hit(event.pos):
                    self.register_hit()

    # ------------------------------------------
    def update(self, dt):
        self.time_left -= dt

        if self.time_left <= 0:
            from game.states import ResultState

            results_data = {
                "score": self.score,
                "hits": self.hits,
                "misses": self.misses,
                "reaction_times": self.reaction_times
            }

            self.game.state_machine.change(ResultState(self.game, results_data))
            return

        self.target.update(dt)

        if self.target.is_expired():
            self.register_miss()

    # ------------------------------------------
    def register_hit(self):
        current_time = pygame.time.get_ticks() / 1000.0
        reaction = current_time - self.spawn_time

        self.hits += 1
        self.reaction_times.append(reaction)

        # Score formula (simple version from spec)
        base_points = 100
        bonus_cap = 50
        ttl = self.target.ttl

        bonus = max(0, ttl - reaction) / ttl * bonus_cap
        self.score += int(base_points + bonus)

        self.target.spawn()
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    # ------------------------------------------
    def register_miss(self):
        self.misses += 1
        self.target.spawn()
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    # ------------------------------------------
    def draw(self, screen):
        screen.fill((20, 120, 20))

        # Draw target
        self.target.draw(screen)

        # HUD
        time_text = f"Time: {max(0, self.time_left):.1f}s"
        score_text = f"Score: {self.score}"
        hits_text = f"Hits: {self.hits}"
        miss_text = f"Misses: {self.misses}"

        screen.blit(self.font.render(time_text, True, (255, 255, 255)), (20, 20))
        screen.blit(self.font.render(score_text, True, (255, 255, 255)), (20, 60))
        screen.blit(self.font.render(hits_text, True, (255, 255, 255)), (20, 100))
        screen.blit(self.font.render(miss_text, True, (255, 255, 255)), (20, 140))