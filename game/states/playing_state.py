import pygame
from .base_state import BaseState 
from game.target import Target
from ui.hud import HUD

class PlayingState(BaseState):
    def enter(self):
        self.duration = 60
        self.time_left = self.duration

        self.font = pygame.font.SysFont(None, 36)
        self.sound = pygame.mixer.Sound("pop.ogg")

        # Stats
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.reaction_times = []

        # Target
        self.target = Target(self.game, radius=30, ttl=1.5)
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
                if self.target.is_hit(event.pos):
                    self.register_hit()
                mouse_pos = pygame.mouse.get_pos()
                if self.hud.pause.checkForInput(mouse_pos): 
                    from game.states import PauseState
                    self.game.state_machine.push(PauseState(self.game))

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
        
        mouse_pos = pygame.mouse.get_pos()
        self.hud.pause.changeColor(mouse_pos)

    # ------------------------------------------
    def register_hit(self):
        self.sound.play()
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
        screen.fill((245,238,205))

        # Draw target
        self.target.draw(screen)

        # HUD
        self.hud.draw(screen, self.time_left, self.score, self.hits, self.misses)