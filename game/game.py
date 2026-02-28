import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FULLSCREEN, TITLE
from game.state_machine import StateMachine
from game.states import StartState


class Game:
    def __init__(self):
        # --- Core Settings ---
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.fps = FPS
        self.fullscreen = FULLSCREEN
        self.title = TITLE

        # --- Runtime Control ---
        self.running = True

        # --- Pygame Initialization ---
        pygame.init()
        pygame.display.set_caption(self.title)

        self._create_display()

        self.clock = pygame.time.Clock()        
        self.font = pygame.font.Font('LuckiestGuy-Regular.ttf', 50)
        self.settings = {
            "duration": 60,
            "size_multiplier": 1.0,
            "ttl_multiplier": 1.0,
            "target_color": (129, 2, 31),
        }

        # --- State Machine ---
        self.state_machine = StateMachine()
        self.state_machine.change(StartState(self))

    # --------------------------------------------------
    # Display Management (Allows Future Customization)
    # --------------------------------------------------
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
            dt = self.clock.tick(self.fps) / 1000.0  # ms → seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    # --------------------------------------------------
    # Event Handling
    # --------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.state_machine.handle_event(event)

    # --------------------------------------------------
    # Update
    # --------------------------------------------------
    def update(self, dt):
        self.state_machine.update(dt)

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.state_machine.draw(self.screen)
        pygame.display.flip()

    # --------------------------------------------------
    # Quit
    # --------------------------------------------------
    def quit(self):
        pygame.quit()
