import pygame
from .base_state import BaseState
from ui.button import Button

class StatState(BaseState):
    def enter(self):
        self.game.play_music("menu")
        center_x = self.game.width // 2
        self.font_title = pygame.font.Font("LuckiestGuy-Regular.ttf", 80)
        self.font_header = self.font
        self.font_body = pygame.font.Font("LuckiestGuy-Regular.ttf", 30)
        
        self.top_records = self.game.db.get_best_record()
        
        self.back_button = Button(
            image=None,
            pos=(center_x, 620),
            font=self.font_header,
            base_color=(129, 2, 31),
            hovering_color=(252,154,154),
            text_input="Back",
        )
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game.states import StartState
            self.game.state_machine.change(StartState(self.game))
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            from game.states import StartState
            self.game.state_machine.change(StartState(self.game))
            
    def update(self, dt):
        self.back_button.changeColor(pygame.mouse.get_pos())
    
    def draw(self, screen):
        screen.fill((245, 238, 205)) 
        center_x = self.game.width // 2
        
        title_text = self.font_title.render("TOP 3 RECORDS", True, (129, 2, 31))
        screen.blit(title_text, title_text.get_rect(center=(center_x, 100)))
        
        headers = ["RANK", "DATE", "SCORE", "ACCURACY", "REACTION"]
        x_offsets = [-480, -280, -80, 170, 430] 
        
        for i, header_text in enumerate(headers):
            header_surf = self.font_header.render(header_text, True, (20, 71, 88))
            screen.blit(header_surf, header_surf.get_rect(center=(center_x + x_offsets[i], 180)))

        start_y = 250
        gap_y = 60
        if len(self.top_records) == 0:
            empty_msg = self.font_body.render("No records found. Play a game first!", True, (0, 0, 0))
            screen.blit(empty_msg, empty_msg.get_rect(center=(center_x, 350)))
        else:
            for i, record in enumerate(self.top_records):
                date, score, accuracy, reaction, _ = record
                
                short_date = date.split(" ")[0] if date else "N/A"
                
                row_data = [f"#{i+1}", short_date, str(score), f"{accuracy}%", f"{reaction}s"]
                
                for j, text in enumerate(row_data):
                    color = (129, 2, 31) if j == 2 else (0, 0, 0) 
                    data = self.font_body.render(text, True, color)
                    screen.blit(data, data.get_rect(center=(center_x + x_offsets[j], start_y + i * gap_y)))

        self.back_button.update(screen)
