import pygame
from .base_state import BaseState
from ui.button import Button


class InstructionState(BaseState):
    def enter(self):
        self.game.play_music("menu")
        center_x = self.game.width // 2
        center_y = self.game.height // 2

        self.font_title = pygame.font.Font("LuckiestGuy-Regular.ttf", 80)
        self.font_body = pygame.font.Font("LuckiestGuy-Regular.ttf", 34)
        self.font_hint = pygame.font.Font("LuckiestGuy-Regular.ttf", 26)

        self.message_lines = [
            "Welcome to Aim Trainer!",
            "Try to hit the target as fast as possible for maximum score.",
        ]

        self.back_button = Button(
            image=None,
            pos=(center_x, center_y + 230),
            font=self.font_body,
            base_color=(129, 2, 31),
            hovering_color=(252,154,154),
            text_input="Back",
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game.states import StartState
            self.game.state_machine.change(StartState(self.game))
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button.checkForInput(mouse_pos):
                from game.states import StartState
                self.game.state_machine.change(StartState(self.game))

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.changeColor(mouse_pos)

    def draw(self, screen):
        screen.fill((245, 238, 205))

        center_x = self.game.width // 2
        y = 120

        title = self.font_title.render("Instruction", True, (129, 2, 31))
        screen.blit(title, title.get_rect(center=(center_x, y)))
        y += 120

        for line in self.message_lines:
            text = self.font_body.render(line, True, (20, 71, 88))
            screen.blit(text, text.get_rect(center=(center_x, y)))
            y += 70

#        hint = self.font_hint.render("Press ESC or click Back", True, (129, 2, 31))
#        screen.blit(hint, hint.get_rect(center=(center_x, y + 30)))

        self.back_button.update(screen)
