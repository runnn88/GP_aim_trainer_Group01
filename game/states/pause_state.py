import pygame
from .base_state import BaseState 
from ui.button import Button

class PauseState(BaseState):
    def enter(self):
        center_x = self.game.width // 2
        center_y = self.game.height // 2
        
        self.font_title = pygame.font.Font('LuckiestGuy-Regular.ttf', 120)
        self.title_text = self.font_title.render("Paused", True, (133,4,34))
        self.title_rect = self.title_text.get_rect(center=(center_x, center_y - 200))
        
        self.cont_button = Button(image=None, pos=(center_x, center_y),
                                  font=self.font, base_color=(129,2,31), #rgb(129,2,31)
                                  hovering_color=(245,238,205), #rgb(245,238,205)
                                  text_input="Continue"
                                  ) 
        self.menu_button = Button(image=None, pos=(center_x, center_y + 100),
                                  font=self.font, base_color=(129,2,31), 
                                  hovering_color=(245,238,205), #rgb(2245,238,205)
                                  text_input="Main menu"
                                  ) 
                                
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.game.state_machine.pop()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.cont_button.checkForInput(mouse_pos): 
                    self.game.state_machine.pop()
                    
                if self.menu_button.checkForInput(mouse_pos):
                    from game.states import StartState
                    self.game.state_machine.change(StartState(self.game))
                
    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.cont_button.changeColor(mouse_pos)
        self.menu_button.changeColor(mouse_pos)

    def draw(self, screen):
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.set_alpha(100)
        overlay.fill((128,128,128))
        screen.blit(overlay, (0,0))
        
        screen.blit(self.title_text, self.title_rect)
        self.cont_button.update(screen)
        self.menu_button.update(screen)