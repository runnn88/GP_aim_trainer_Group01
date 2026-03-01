import pygame
import random
import math


class Target:
    def __init__(self, game, radius=30, ttl=1.5, color=(129, 2, 31)):
        self.game = game
        self.radius = radius
        self.ttl = ttl  # seconds
        self.color = color
        self.fruit_type = "apple"
        self.texture_points = []
        
        self.x = 0
        self.y = 0

        self.time_alive = 0  # how long target has existed

        self.spawn()

    # ------------------------------------------
    # Spawn at random valid position
    # ------------------------------------------
    def spawn(self):
        width = self.game.width
        height = self.game.height

        self.x = random.randint(self.radius, width - self.radius)
        self.y = random.randint(80 + self.radius, height - self.radius)
        self.fruit_type = random.choice(
            ["orange", "apple", "watermelon", "coconut", "peach", "plum", "lemon", "kiwi", "grape"]
        )
        self.texture_points = []
        if self.fruit_type == "orange":
            for _ in range(max(8, self.radius // 2)):
                angle = random.random() * math.tau
                dist = random.randint(0, max(1, self.radius - 3))
                self.texture_points.append((angle, dist))

        self.time_alive = 0

    # ------------------------------------------
    # Update lifetime
    # ------------------------------------------
    def update(self, dt):
        self.time_alive += dt

    # ------------------------------------------
    # Check if expired
    # ------------------------------------------
    def is_expired(self):
        return self.time_alive >= self.ttl

    # ------------------------------------------
    # Check if clicked
    # ------------------------------------------
    def is_hit(self, mouse_pos):
        mx, my = mouse_pos
        distance = math.sqrt((mx - self.x) ** 2 + (my - self.y) ** 2)
        return distance <= self.radius

    # ------------------------------------------
    # Draw target
    # ------------------------------------------
    def draw(self, screen):
        if self.fruit_type == "orange":
            self._draw_orange(screen)
        elif self.fruit_type == "watermelon":
            self._draw_watermelon(screen)
        elif self.fruit_type == "coconut":
            self._draw_coconut(screen)
        elif self.fruit_type == "peach":
            self._draw_peach(screen)
        elif self.fruit_type == "plum":
            self._draw_plum(screen)
        elif self.fruit_type == "lemon":
            self._draw_lemon(screen)
        elif self.fruit_type == "kiwi":
            self._draw_kiwi(screen)
        elif self.fruit_type == "grape":
            self._draw_grape(screen)
        else:
            self._draw_apple(screen)

    def get_splash_colors(self):
        palette = {
            "orange": [(245, 155, 45), (255, 190, 90), (235, 120, 25)],
            "apple": [(210, 35, 55), (235, 85, 100), (160, 25, 40)],
            "watermelon": [(220, 70, 90), (245, 120, 140), (180, 45, 65)],
            "coconut": [(140, 95, 58), (175, 130, 90), (100, 65, 38)],
            "peach": [(245, 165, 120), (255, 195, 145), (230, 120, 95)],
            "plum": [(125, 55, 165), (175, 120, 205), (85, 35, 115)],
            "lemon": [(250, 220, 80), (255, 240, 135), (215, 185, 40)],
            "kiwi": [(145, 200, 70), (200, 230, 120), (110, 160, 55)],
            "grape": [(105, 58, 150), (155, 105, 190), (70, 38, 105)],
        }
        return palette.get(self.fruit_type, [(200, 30, 45), (245, 120, 130)])

    def _draw_apple(self, screen):
        body_color = (200, 30, 45)
        highlight = (240, 130, 140)
        stem_color = (80, 45, 25)
        leaf_color = (65, 150, 70)

        pygame.draw.circle(screen, body_color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (140, 15, 30), (self.x, self.y), self.radius, 2)
        pygame.draw.circle(
            screen,
            highlight,
            (self.x - self.radius // 3, self.y - self.radius // 3),
            max(3, self.radius // 5),
        )

        stem_w = max(2, self.radius // 6)
        stem_h = max(6, self.radius // 2)
        stem_rect = pygame.Rect(0, 0, stem_w, stem_h)
        stem_rect.center = (self.x, self.y - self.radius - stem_h // 4)
        pygame.draw.rect(screen, stem_color, stem_rect, border_radius=2)

        leaf_rect = pygame.Rect(0, 0, max(8, self.radius // 2), max(5, self.radius // 3))
        leaf_rect.center = (self.x + self.radius // 3, self.y - self.radius + 2)
        pygame.draw.ellipse(screen, leaf_color, leaf_rect)

    def _draw_orange(self, screen):
        base = (240, 145, 35)
        shade = (220, 110, 20)
        speck = (250, 180, 90)

        pygame.draw.circle(screen, base, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, shade, (self.x, self.y), self.radius, 2)

        for angle, dist in self.texture_points:
            px = int(self.x + math.cos(angle) * dist)
            py = int(self.y + math.sin(angle) * dist)
            pygame.draw.circle(screen, speck, (px, py), 1)

        leaf_rect = pygame.Rect(0, 0, max(8, self.radius // 2), max(5, self.radius // 3))
        leaf_rect.center = (self.x + self.radius // 4, self.y - self.radius + 2)
        pygame.draw.ellipse(screen, (70, 160, 80), leaf_rect)

    def _draw_watermelon(self, screen):
        rind = (35, 125, 55)
        flesh = (215, 55, 70)
        inner_rind = (170, 220, 120)
        seed = (30, 20, 20)

        pygame.draw.circle(screen, rind, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, inner_rind, (self.x, self.y), max(3, int(self.radius * 0.88)))
        pygame.draw.circle(screen, flesh, (self.x, self.y), max(3, int(self.radius * 0.76)))

        seed_count = max(5, self.radius // 4)
        for i in range(seed_count):
            angle = (2 * math.pi * i / seed_count) + 0.2
            dist = self.radius * 0.45
            sx = int(self.x + math.cos(angle) * dist)
            sy = int(self.y + math.sin(angle) * dist)
            pygame.draw.ellipse(
                screen,
                seed,
                pygame.Rect(sx - 2, sy - 4, 4, 8),
            )

    def _draw_coconut(self, screen):
        shell = (116, 78, 47)
        shell_dark = (82, 53, 31)
        fiber = (150, 110, 72)

        pygame.draw.circle(screen, shell, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, shell_dark, (self.x, self.y), self.radius, 2)

        for i in range(4):
            y = self.y - self.radius // 2 + i * max(3, self.radius // 3)
            pygame.draw.line(
                screen,
                fiber,
                (self.x - self.radius + 4, y),
                (self.x + self.radius - 4, y + 2),
                2,
            )

        eye_r = max(2, self.radius // 8)
        pygame.draw.circle(screen, shell_dark, (self.x - self.radius // 4, self.y), eye_r)
        pygame.draw.circle(screen, shell_dark, (self.x + self.radius // 4, self.y), eye_r)
        pygame.draw.circle(screen, shell_dark, (self.x, self.y + self.radius // 4), eye_r)

    def _draw_peach(self, screen):
        body = (242, 150, 110)
        shade = (220, 105, 90)
        crease = (190, 80, 70)

        pygame.draw.circle(screen, body, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, shade, (self.x, self.y), self.radius, 2)
        pygame.draw.line(
            screen,
            crease,
            (self.x + self.radius // 7, self.y - self.radius + 5),
            (self.x + self.radius // 7, self.y + self.radius - 5),
            2,
        )

    def _draw_plum(self, screen):
        body = (116, 45, 155)
        shade = (78, 28, 106)
        bloom = (186, 145, 210)

        pygame.draw.circle(screen, body, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, shade, (self.x, self.y), self.radius, 2)
        pygame.draw.circle(
            screen,
            bloom,
            (self.x - self.radius // 4, self.y - self.radius // 4),
            max(3, self.radius // 4),
        )

    def _draw_lemon(self, screen):
        body = (245, 217, 72)
        shade = (220, 190, 40)
        edge = (195, 165, 28)

        lemon_rect = pygame.Rect(0, 0, self.radius * 2, int(self.radius * 1.7))
        lemon_rect.center = (self.x, self.y)
        pygame.draw.ellipse(screen, body, lemon_rect)
        pygame.draw.ellipse(screen, edge, lemon_rect, 2)
        pygame.draw.ellipse(
            screen,
            shade,
            pygame.Rect(self.x - self.radius // 2, self.y - self.radius // 2, self.radius, self.radius // 2),
        )

    def _draw_kiwi(self, screen):
        skin = (140, 90, 45)
        flesh = (137, 191, 64)
        core = (238, 235, 198)
        seed = (28, 22, 15)

        pygame.draw.circle(screen, skin, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, flesh, (self.x, self.y), max(3, int(self.radius * 0.82)))
        pygame.draw.circle(screen, core, (self.x, self.y), max(2, int(self.radius * 0.22)))

        seed_count = max(8, self.radius // 2)
        for i in range(seed_count):
            angle = (2 * math.pi * i / seed_count) + 0.1
            dist = self.radius * 0.48
            sx = int(self.x + math.cos(angle) * dist)
            sy = int(self.y + math.sin(angle) * dist)
            pygame.draw.ellipse(screen, seed, pygame.Rect(sx - 1, sy - 2, 2, 4))

    def _draw_grape(self, screen):
        body = (92, 48, 135)
        shade = (62, 29, 93)
        highlight = (145, 100, 186)

        pygame.draw.circle(screen, body, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, shade, (self.x, self.y), self.radius, 2)
        pygame.draw.circle(
            screen,
            highlight,
            (self.x - self.radius // 3, self.y - self.radius // 3),
            max(3, self.radius // 5),
        )
