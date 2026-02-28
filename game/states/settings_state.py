import pygame
from .base_state import BaseState
from ui.button import Button


class SettingsState(BaseState):
    def enter(self):
        center_x = self.game.width // 2

        self.font_title = pygame.font.Font("LuckiestGuy-Regular.ttf", 80)
        self.font_section = pygame.font.Font("LuckiestGuy-Regular.ttf", 34)
        self.font_option = pygame.font.Font("LuckiestGuy-Regular.ttf", 26)

        self.duration_options = [
            ("60s", 60),
            ("30s", 30),
            ("90s", 90),
        ]
        self.size_options = [
            ("Default", 1.0),
            ("Easy", 1.2),
            ("Hard", 0.5),
        ]
        self.difficulty_options = [
            ("Default", 1.0),
            ("Easy", 2.0),
            ("Hard", 0.5),
        ]
        self.color_options = [
            ("Default", (129, 2, 31)),
            ("Blue", (52, 132, 235)),
            ("Yellow", (240, 200, 40)),
        ]
        self.delay_options = [
            ("None (Default)", 0.0),
            ("100ms", 0.1),
            ("250ms", 0.25),
        ]
        self.duration_buttons = self._build_option_buttons(center_x, 145, self.duration_options)
        self.size_buttons = self._build_option_buttons(center_x, 225, self.size_options)
        self.difficulty_buttons = self._build_option_buttons(center_x, 305, self.difficulty_options)
        self.color_buttons = self._build_option_buttons(center_x, 385, self.color_options)
        self.delay_buttons = self._build_option_buttons(center_x, 465, self.delay_options)

        self.back_button = Button(
            image=None,
            pos=(center_x, 560),
            font=self.font_option,
            base_color=(129, 2, 31),
            hovering_color=(20, 71, 88),
            text_input="Back",
        )

    def _build_option_buttons(self, center_x, y, options):
        spacing = 320
        start_x = center_x - spacing
        buttons = []
        for i, (label, _) in enumerate(options):
            buttons.append(
                Button(
                    image=None,
                    pos=(start_x + i * spacing, y),
                    font=self.font_option,
                    base_color=(129, 2, 31),
                    hovering_color=(20, 71, 88),
                    text_input=label,
                )
            )
        return buttons

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game.states import StartState
            self.game.state_machine.change(StartState(self.game))
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(self.duration_buttons):
            if button.checkForInput(mouse_pos):
                self.game.settings["duration"] = self.duration_options[i][1]
                return

        for i, button in enumerate(self.size_buttons):
            if button.checkForInput(mouse_pos):
                self.game.settings["size_multiplier"] = self.size_options[i][1]
                return

        for i, button in enumerate(self.difficulty_buttons):
            if button.checkForInput(mouse_pos):
                self.game.settings["ttl_multiplier"] = self.difficulty_options[i][1]
                return

        for i, button in enumerate(self.color_buttons):
            if button.checkForInput(mouse_pos):
                self.game.settings["target_color"] = self.color_options[i][1]
                return

        for i, button in enumerate(self.delay_buttons):
            if button.checkForInput(mouse_pos):
                self.game.settings["spawn_delay"] = self.delay_options[i][1]
                return

        if self.back_button.checkForInput(mouse_pos):
            from game.states import StartState
            self.game.state_machine.change(StartState(self.game))

    def _set_group_button_style(self, buttons, options, selected_value):
        for i, button in enumerate(buttons):
            option_value = options[i][1]
            if option_value == selected_value:
                button.base_color = (0, 0, 0)
                button.hovering_color = (0, 0, 0)
            else:
                button.base_color = (129, 2, 31)
                button.hovering_color = (20, 71, 88)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()

        self._set_group_button_style(
            self.duration_buttons, self.duration_options, self.game.settings["duration"]
        )
        self._set_group_button_style(
            self.size_buttons, self.size_options, self.game.settings["size_multiplier"]
        )
        self._set_group_button_style(
            self.difficulty_buttons, self.difficulty_options, self.game.settings["ttl_multiplier"]
        )
        self._set_group_button_style(
            self.color_buttons, self.color_options, self.game.settings["target_color"]
        )
        self._set_group_button_style(
            self.delay_buttons, self.delay_options, self.game.settings["spawn_delay"]
        )

        for button in self.duration_buttons:
            button.changeColor(mouse_pos)
        for button in self.size_buttons:
            button.changeColor(mouse_pos)
        for button in self.difficulty_buttons:
            button.changeColor(mouse_pos)
        for button in self.color_buttons:
            button.changeColor(mouse_pos)
        for button in self.delay_buttons:
            button.changeColor(mouse_pos)
        self.back_button.changeColor(mouse_pos)

    def draw(self, screen):
        screen.fill((245, 238, 205))

        center_x = self.game.width // 2

        title_text = self.font_title.render("Settings", True, (129, 2, 31))
        screen.blit(title_text, title_text.get_rect(center=(center_x, 60)))

        duration_text = self.font_section.render("Game Duration", True, (20, 71, 88))
        size_text = self.font_section.render("Target Size", True, (20, 71, 88))
        difficulty_text = self.font_section.render("Difficulty", True, (20, 71, 88))
        color_text = self.font_section.render("Target Color", True, (20, 71, 88))
        delay_text = self.font_section.render("Delay", True, (20, 71, 88))

        screen.blit(duration_text, duration_text.get_rect(center=(center_x, 105)))
        screen.blit(size_text, size_text.get_rect(center=(center_x, 185)))
        screen.blit(difficulty_text, difficulty_text.get_rect(center=(center_x, 265)))
        screen.blit(color_text, color_text.get_rect(center=(center_x, 345)))
        screen.blit(delay_text, delay_text.get_rect(center=(center_x, 425)))

        for button in self.duration_buttons:
            button.update(screen)
        for button in self.size_buttons:
            button.update(screen)
        for button in self.difficulty_buttons:
            button.update(screen)
        for button in self.color_buttons:
            button.update(screen)
        for button in self.delay_buttons:
            button.update(screen)
        self.back_button.update(screen)
