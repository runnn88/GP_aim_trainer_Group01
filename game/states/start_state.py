import pygame
from .base_state import BaseState 
from ui.button import Button

class StartState(BaseState):
    def enter(self):
        """Initialize creating the UI before enter the start state"""
        center_x = self.game.width // 2
        center_y = self.game.height // 2
        
        self.font_title = pygame.font.Font('PressStart2P.ttf', 80)
        self.title_text = self.font_title.render("AIM TRAINER", True, "white")
        self.title_rect = self.title_text.get_rect(center=(center_x, center_y - 100))
        
        self.start_button = Button(image=None, pos=(center_x, center_y + 70), 
                                   font=self.font, base_color="white",
                                   hovering_color= (255,200,200), #rgb(255,200,200)
                                   text_input="Start"            
        )
        self.exit_button = Button(image=None, pos=(center_x, center_y + 200), 
                                   font=self.font, base_color="white",
                                   hovering_color= (255,200,200), #rgb(255,200,200)
                                   text_input="Exit"            
        )
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
        screen.fill((117, 0, 0)) # rgb(148, 0, 0)
        
        screen.blit(self.title_text, self.title_rect)

        self.start_button.update(screen)
        self.exit_button.update(screen)
        
        