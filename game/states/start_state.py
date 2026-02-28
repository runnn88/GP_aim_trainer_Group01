import pygame
from .base_state import BaseState 
from ui.button import Button

class StartState(BaseState):
    def enter(self):
        """Initialize creating the UI before enter the start state"""
        center_x = self.game.width // 2
        center_y = self.game.height // 2
        
        self.font_title = pygame.font.Font('LuckiestGuy-Regular.ttf', 185)
        self.font = pygame.font.Font('LuckiestGuy-Regular.ttf', 60)
        # self.font_title.set_bold(True)
        self.title_text1 = self.create_title_outline(self.font_title, "AIM", 33, (245,238,205), (129,2,31))
        self.title_text2 = self.create_title_outline(self.font_title, "TRAINER", 33, (245,238,205), (129,2,31))
        
        self.title_rect1 = self.title_text1.get_rect(topleft=(386- 35, 98 - 35))
        self.title_rect2 = self.title_text2.get_rect(topleft=(280 -35, 263 - 35))

        
        self.start_button = Button(image=None, pos=(center_x, center_y + 140), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Start"            
        )
        self.setting_button = Button(image=None, pos=(center_x, center_y + 220), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Setting"            
        )
        self.exit_button = Button(image=None, pos=(center_x, center_y + 300), 
                                   font=self.font, base_color= (245,238,205),
                                   hovering_color= (92,145,163), #rgb(92,145,163)
                                   text_input="Exit"            
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

                if self.exit_button.checkForInput(mouse_pos):
                    self.game.running = False

    def update(self, dt):
        """Change color for hovering"""
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.changeColor(mouse_pos)
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

        self.start_button.update(screen)
        self.setting_button.update(screen)
        self.exit_button.update(screen)
        
        