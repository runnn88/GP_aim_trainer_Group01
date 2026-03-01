import pygame
from .base_state import BaseState
from game.target import Target
from ui.hud import HUD


class PlayingState(BaseState):
    def enter(self):
        self.miss_click_penalty = 15
        self.spawn_delay = self.game.settings["spawn_delay"]
        self.progression_enabled = self.game.settings["progression_enabled"]
        self.spawn_delay_timer = 0.0
        self.target_active = True
        self.duration = self.game.settings["duration"]
        self.time_left = self.duration

        self.font = pygame.font.SysFont(None, 36)
        self.sound = pygame.mixer.Sound("pop.ogg")

        # Stats
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.reaction_times = []

        # Target
        self.base_radius = int(30 * self.game.settings["size_multiplier"])
        self.base_ttl = 1.5 * self.game.settings["ttl_multiplier"]
        target_color = self.game.settings["target_color"]
        self.target = Target(self.game, radius=self.base_radius, ttl=self.base_ttl, color=target_color)
        self._apply_progression_to_target()
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

                if not self.target_active:
                    return

                if self.target.is_hit(event.pos):
                    self.register_hit()
                else:
                    self.register_miss_click()

    # ------------------------------------------
    def update(self, dt):
        self.time_left -= dt

        if self.time_left <= 0:
            from game.states import ResultState
            total_clicks = self.hits + self.misses
            accuracy = round((self.hits / total_clicks * 100) if total_clicks > 0 else 0, 2)
            if self.reaction_times:
                avg_reaction = sum(self.reaction_times) / len(self.reaction_times)
                best_reaction = min(self.reaction_times)
            else: 
                avg_reaction = 0.0
                best_reaction = 0.0
            avg_reaction = round(avg_reaction,3)
            self.game.db.insert_result(self.score, accuracy, avg_reaction, 
                                       self.hits, self.misses, self.max_combo)
            
            results_data = {
                "score": self.score,
                "combo": self.max_combo,
                "hits": self.hits,
                "misses": self.misses,
                "accuracy": accuracy,
                "avg_reaction": avg_reaction,
                "best_reaction": best_reaction
            }
            
            # self.game.update_persistent_stats(self.score, self.max_combo)
            self.game.state_machine.change(ResultState(self.game, results_data))
            return

        if self.target_active:
            self.target.update(dt)

            if self.target.is_expired():
                self.register_timeout_miss()
        elif self.spawn_delay_timer > 0:
            self.spawn_delay_timer -= dt
            if self.spawn_delay_timer <= 0:
                self._apply_progression_to_target()
                self.target.spawn()
                self.spawn_time = pygame.time.get_ticks() / 1000.0
                self.target_active = True

        mouse_pos = pygame.mouse.get_pos()
        self.hud.pause.changeColor(mouse_pos)
        

    # ------------------------------------------
    def register_hit(self):
        self.sound.play()
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

        self.queue_next_target()

    # ------------------------------------------
    def register_miss_click(self):
        self.misses += 1
        self.combo = 0
        self.score = max(0, self.score - self.miss_click_penalty)

    def register_timeout_miss(self):
        self.misses += 1
        self.combo = 0
        self.score = max(0, self.score - self.miss_click_penalty)
        self.queue_next_target()

    def queue_next_target(self):
        if self.spawn_delay > 0:
            self.target_active = False
            self.spawn_delay_timer = self.spawn_delay
        else:
            self._apply_progression_to_target()
            self.target.spawn()
            self.spawn_time = pygame.time.get_ticks() / 1000.0
            self.target_active = True

    def _apply_progression_to_target(self):
        if not self.progression_enabled:
            self.target.radius = self.base_radius
            self.target.ttl = self.base_ttl
            return

        elapsed_time = self.duration - self.time_left
        stage = max(0, int(elapsed_time // 10))

        size_scale = max(0.4, 1.0 - 0.1 * stage)
        ttl_scale = max(0.2, 1.0 - 0.2 * stage)

        self.target.radius = max(8, int(self.base_radius * size_scale))
        self.target.ttl = max(0.2, self.base_ttl * ttl_scale)

    # ------------------------------------------
    def draw(self, screen):
        screen.fill((245, 238, 205))

        # Draw target
        if self.target_active:
            self.target.draw(screen)

        # HUD
        self.hud.draw(screen, self.time_left, self.score, self.hits, self.misses, self.combo)
