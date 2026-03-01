import pygame
from .base_state import BaseState 
from ui.button import Button

class StartState(BaseState):
    def enter(self):
        """Initialize creating the UI before enter the start state"""
        center_x = self.game.width // 2
        center_y = self.game.height // 2
        
        self.font_title = pygame.font.Font('LuckiestGuy-Regular.ttf', 130)
        self.font = pygame.font.Font('LuckiestGuy-Regular.ttf', 40)
        self.font_stats = pygame.font.Font('LuckiestGuy-Regular.ttf', 26)
        # self.font_title.set_bold(True)
        self.title_text1 = self.create_title_outline(self.font_title, "AIM", 20, (245,238,205), (129,2,31))
        self.title_text2 = self.create_title_outline(self.font_title, "TRAINER", 20, (245,238,205), (129,2,31))
        
        self.title_rect1 = self.title_text1.get_rect(center=(center_x, 130))
        self.title_rect2 = self.title_text2.get_rect(center=(center_x, 240))

        
        button_start_y = center_y + 70
        button_gap = 60

        self.start_button = Button(image=None, pos=(center_x, button_start_y), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Start"            
        )
        self.setting_button = Button(image=None, pos=(center_x, button_start_y + button_gap), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Settings"            
        )
        self.instruction_button = Button(image=None, pos=(center_x, button_start_y + button_gap * 2), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Instruction"            
        )
        self.stat_button = Button(image=None, pos=(center_x, button_start_y + button_gap * 3), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="History Statistic"            
        )
        self.exit_button = Button(image=None, pos=(center_x, button_start_y + button_gap * 4), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Exit"            
        )

        best_score, highest_combo = self.game.db.get_absolute_best_score()
        self.best_score_text = self.font_stats.render(
            f"Best Score: {best_score}", True, (245, 238, 205)
        )
        self.best_combo_text = self.font_stats.render(
            f"Highest Combo: x{highest_combo}", True, (245, 238, 205)
        )
        
    def create_title_outline(self, font, text, thickness, outline_color, text_color):
        base_title = font.render(text, True, text_color)
        outline_text = font.render(text, True, outline_color)
        
        weight, height = base_title.get_size()
        surface = pygame.Surface((weight + thickness*2, height + thickness*2), pygame.SRCALPHA)
        
        for x in range(-thickness, thickness + 1):
            for y in range(-thickness, thickness + 1):
                if x**2 + y**2 <= thickness**2:
                    surface.blit(outline_text, (x + thickness, y + thickness))
        surface.blit(base_title, (thickness, thickness))
        return surface
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.start_button.checkForInput(mouse_pos):
                    from game.states import PlayingState
                    self.game.state_machine.change(PlayingState(self.game))

                if self.setting_button.checkForInput(mouse_pos):
                    from game.states import SettingsState
                    self.game.state_machine.change(SettingsState(self.game))
                    
                if self.instruction_button.checkForInput(mouse_pos):
                    from game.states import InstructionState
                    self.game.state_machine.change(InstructionState(self.game))

                if self.stat_button.checkForInput(mouse_pos):
                    from game.states import StatState
                    self.game.state_machine.change(StatState(self.game))

                if self.exit_button.checkForInput(mouse_pos):
                    self.game.running = False

    def update(self, dt):
        """Change color for hovering"""
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.changeColor(mouse_pos)
        self.setting_button.changeColor(mouse_pos)
        self.instruction_button.changeColor(mouse_pos)
        self.stat_button.changeColor(mouse_pos)
        self.exit_button.changeColor(mouse_pos)
    
    def draw(self, screen):
        center_x = self.game.width // 2
        center_y = self.game.height // 2
        
        screen.fill( (129,2,31)) 
        
        rect3 = pygame.Rect(0,0, 1218, 897)
        rect3.center = (center_x, center_y)
        pygame.draw.ellipse(screen, (245,238,205), rect3)
        rect2 = pygame.Rect(0,0, 1070, 788)
        rect2.center = (center_x, center_y)
        pygame.draw.ellipse(screen, (92,145,163), rect2)
        rect1 = pygame.Rect(0,0, 940, 692)
        rect1.center = (center_x, center_y)
        pygame.draw.ellipse(screen, (20,71,88), rect1)
        
        screen.blit(self.title_text2, self.title_rect2)
        screen.blit(self.title_text1, self.title_rect1)
        screen.blit(self.best_score_text, self.best_score_text.get_rect(center=(center_x, center_y - 20 )))
        screen.blit(self.best_combo_text, self.best_combo_text.get_rect(center=(center_x, center_y + 15)))

        self.start_button.update(screen)
        self.setting_button.update(screen)
        self.instruction_button.update(screen)
        self.stat_button.update(screen)
        self.exit_button.update(screen)