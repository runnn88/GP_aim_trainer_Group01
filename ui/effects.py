import random
import pygame


class JuiceSplashEffect:
    def __init__(self, x, y, radius, colors):
        self.particles = []
        self.life = 0.45
        self.max_life = self.life

        particle_count = max(14, radius // 2)
        for _ in range(particle_count):
            angle = random.uniform(0, 360)
            speed = random.uniform(130, 330) * max(0.75, radius / 30)
            velocity = pygame.math.Vector2(1, 0).rotate(angle) * speed
            size = random.uniform(2.0, 5.5)
            color = random.choice(colors)
            self.particles.append(
                {
                    "pos": pygame.math.Vector2(x, y),
                    "vel": velocity,
                    "size": size,
                    "color": color,
                }
            )

    def update(self, dt):
        self.life -= dt
        gravity = pygame.math.Vector2(0, 520)
        drag = 0.95

        for p in self.particles:
            p["vel"] += gravity * dt
            p["vel"] *= drag
            p["pos"] += p["vel"] * dt
            p["size"] = max(0.5, p["size"] - dt * 5.5)

    def is_done(self):
        return self.life <= 0

    def draw(self, screen):
        alpha_ratio = max(0.0, self.life / self.max_life)
        for p in self.particles:
            radius = int(max(1, p["size"]))
            c = p["color"]
            color = (
                int(c[0] * alpha_ratio),
                int(c[1] * alpha_ratio),
                int(c[2] * alpha_ratio),
            )
            pygame.draw.circle(screen, color, (int(p["pos"].x), int(p["pos"].y)), radius)
