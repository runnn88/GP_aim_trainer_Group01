import pygame
import json
from pathlib import Path
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FULLSCREEN, TITLE
from game.state_machine import StateMachine
from game.states import StartState
from game.database import Database


class Game:
    def __init__(self):
        # --- Core Settings ---
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.fps = FPS
        self.fullscreen = FULLSCREEN
        self.title = TITLE

        self.running = True

        pygame.init()
        pygame.display.set_caption(self.title)

        self._create_display()

        self.clock = pygame.time.Clock()        
        self.font = pygame.font.Font('LuckiestGuy-Regular.ttf', 50)
        self.settings = {
            "duration": 60,
            "size_multiplier": 1.0,
            "ttl_multiplier": 1.0,
            "spawn_delay": 0.0,
            "progression_enabled": False,
            "target_color": (129, 2, 31),
        }
        # self.stats_file = Path(__file__).resolve().parent.parent / "player_stats.json"
        # self.persistent_stats = self._load_persistent_stats()
        
        self.db = Database()

        self.state_machine = StateMachine()
        self.state_machine.change(StartState(self))

    def _create_display(self):
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode((self.width, self.height), flags)

    def set_resolution(self, width, height):
        """Change resolution at runtime."""
        self.width = width
        self.height = height
        self._create_display()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
        self._create_display()

    def set_fps(self, fps):
        """Change FPS cap dynamically."""
        self.fps = fps

    # --------------------------------------------------
    # Main Loop
    # --------------------------------------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  

            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.state_machine.handle_event(event)

    def update(self, dt):
        self.state_machine.update(dt)
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.state_machine.draw(self.screen)
        pygame.display.flip()
    
    def quit(self):
        pygame.quit()

    # def _load_persistent_stats(self):
    #     default_stats = {"best_score": 0, "highest_combo": 0}
    #     if not self.stats_file.exists():
    #         return default_stats

    #     try:
    #         data = json.loads(self.stats_file.read_text(encoding="utf-8"))
    #         return {
    #             "best_score": max(0, int(data.get("best_score", 0))),
    #             "highest_combo": max(0, int(data.get("highest_combo", 0))),
    #         }
    #     except Exception:
    #         return default_stats

    # def _save_persistent_stats(self):
    #     self.stats_file.write_text(
    #         json.dumps(self.persistent_stats, indent=2), encoding="utf-8"
    #     )

    # def update_persistent_stats(self, score, highest_combo):
    #     updated = False

    #     if score > self.persistent_stats["best_score"]:
    #         self.persistent_stats["best_score"] = score
    #         updated = True

    #     if highest_combo > self.persistent_stats["highest_combo"]:
    #         self.persistent_stats["highest_combo"] = highest_combo
    #         updated = True

    #     if updated:
    #         self._save_persistent_stats()
