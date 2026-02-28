import pygame
from .base_state import BaseState 
from game.target import Target
from ui.hud import HUD

class PlayingState(BaseState):
    def enter(self):
        self.miss_click_penalty = 15
        self.duration = self.game.settings["duration"]
        self.time_left = self.duration

        self.font = pygame.font.SysFont(None, 36)

        # Stats
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.reaction_times = []

        # Target
        radius = int(30 * self.game.settings["size_multiplier"])
        ttl = 1.5 * self.game.settings["ttl_multiplier"]
        target_color = self.game.settings["target_color"]
        self.target = Target(self.game, radius=radius, ttl=ttl, color=target_color)
        self.spawn_time = pygame.time.get_ticks() / 1000.0
        self.hud = HUD(self.game)

    # ------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from game.states import PauseState
                self.game.state_machine.push(PauseState(self.game))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.hud.pause.checkForInput(mouse_pos):
                    from game.states import PauseState
                    self.game.state_machine.push(PauseState(self.game))
                    return

                if self.target.is_hit(event.pos):
                    self.register_hit()
                else:
                    self.register_miss(is_miss_click=True)

    # ------------------------------------------
    def update(self, dt):
        self.time_left -= dt

        if self.time_left <= 0:
            from game.states import ResultState

            results_data = {
                "score": self.score,
                "combo": self.max_combo,
                "hits": self.hits,
                "misses": self.misses,
                "reaction_times": self.reaction_times
            }

            self.game.update_persistent_stats(self.score, self.max_combo)
            self.game.state_machine.change(ResultState(self.game, results_data))
            return

        self.target.update(dt)

        if self.target.is_expired():
            self.register_miss(is_miss_click=False)
        
        mouse_pos = pygame.mouse.get_pos()
        self.hud.pause.changeColor(mouse_pos)

    # ------------------------------------------
    def register_hit(self):
        current_time = pygame.time.get_ticks() / 1000.0
        reaction = current_time - self.spawn_time

        self.hits += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self.reaction_times.append(reaction)

        # Combo multiplier increases with consecutive hits and caps at x3.
        base_points = 100
        bonus_cap = 50
        ttl = self.target.ttl
        combo_multiplier = min(1.0 + (self.combo - 1) * 0.2, 3.0)

        bonus = max(0, ttl - reaction) / ttl * bonus_cap
        self.score += int((base_points + bonus) * combo_multiplier)

        self.target.spawn()
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    # ------------------------------------------
    def register_miss(self, is_miss_click=False):
        self.misses += 1
        self.combo = 0

        if is_miss_click:
            self.score = max(0, self.score - self.miss_click_penalty)

        self.target.spawn()
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    # ------------------------------------------
    def draw(self, screen):
        screen.fill((245,238,205))

        # Draw target
        self.target.draw(screen)

        # HUD
        self.hud.draw(screen, self.time_left, self.score, self.hits, self.misses, self.combo)
