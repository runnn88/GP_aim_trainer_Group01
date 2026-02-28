import pygame

class HUD:
    def __init__(self, game):
        self.game = game
        self.width = game.width
        self.height = game.height 
        
        self.bar_height = 80 
        self.font = pygame.font.Font('LuckiestGuy-Regular.ttf', 40)
        self.top_bar = pygame.Rect(0,0, self.width, self.bar_height)
        
    def draw(self, screen, time_left, score, hit, miss):
        pygame.draw.rect(screen, (20,71,88), self.top_bar)
        
        time_text = self.font.render(f"{max(0, time_left):.1f}", True, (245,238,205))
        hit_text = self.font.render(f"Hit: {hit}", True, (245,238,205))
        miss_text = self.font.render(f"Missed: {miss}", True, (245,238,205)) # rgb(245,238,205)
        score_text = self.font.render(f"Score: {score}", True, (245,238,205))
        combo = self.font.render(f"Combo x0", True, (245,238,205))
        pause = self.font.render("||", True, (245,238,205))
        
        screen.blit(time_text, time_text.get_rect(topleft=(26, 27)))
        screen.blit(hit_text, hit_text.get_rect(topleft=(190, 27)))
        screen.blit(miss_text, miss_text.get_rect(topleft=(400, 27)))
        screen.blit(score_text, score_text.get_rect(topleft=(650, 27)))
        screen.blit(combo, combo.get_rect(topleft=(946, 27)))
        screen.blit(pause, pause.get_rect(topright=(self.width - 27, 27)))