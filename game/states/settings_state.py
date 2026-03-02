import pygame
from .base_state import BaseState
from ui.button import Button


class SettingsState(BaseState):
    def enter(self):
        self.game.play_music("menu")
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
        self.delay_options = [
            ("None (Default)", 0.0),
            ("100ms", 0.1),
            ("250ms", 0.25),
        ]
        self.progression_options = [
            ("Off (Default)", False),
            ("On", True),
        ]

        self.progression_buttons = self._build_option_buttons(center_x, 160, self.progression_options)
        self.duration_buttons = self._build_option_buttons(center_x, 240, self.duration_options)
        self.size_buttons = self._build_option_buttons(center_x, 320, self.size_options)
        self.difficulty_buttons = self._build_option_buttons(center_x, 400, self.difficulty_options)
        self.delay_buttons = self._build_option_buttons(center_x, 480, self.delay_options)
        self._init_volume_slider(center_x, 560)

        self.back_button = Button(
            image=None,
            pos=(center_x, 650),
            font=self.font_section,
            base_color=(129, 2, 31),
            hovering_color=(252, 154, 154),
            text_input="Back",
        )

    def _init_volume_slider(self, center_x, y):
        self.slider_rect = pygame.Rect(0, 0, 420, 10)
        self.slider_rect.center = (center_x, y)
        self.slider_knob_radius = 14
        self.dragging_volume = False
        self._update_volume_knob_from_setting()

    def _update_volume_knob_from_setting(self):
        volume = self.game.settings["master_volume"]
        self.slider_knob_x = int(self.slider_rect.left + volume * self.slider_rect.width)
        self.slider_knob_y = self.slider_rect.centery

    def _set_volume_from_mouse(self, mouse_x):
        clamped_x = max(self.slider_rect.left, min(mouse_x, self.slider_rect.right))
        volume = (clamped_x - self.slider_rect.left) / self.slider_rect.width
        self.game.set_master_volume(volume)
        self._update_volume_knob_from_setting()

    def _build_option_buttons(self, center_x, y, options):
        option_count = len(options)
        if option_count == 2:
            spacing = 360
            start_x = center_x - (spacing // 2)
        elif option_count == 3:
            spacing = 320
            start_x = center_x - spacing
        elif option_count == 4:
            spacing = 250
            start_x = center_x - int(spacing * 1.5)
        else:
            spacing = 200
            start_x = center_x - int(spacing * (option_count - 1) / 2)

        buttons = []
        for i, (label, _) in enumerate(options):
            buttons.append(
                Button(
                    image=None,
                    pos=(start_x + i * spacing, y),
                    font=self.font_option,
                    base_color=(129, 2, 31),
                    hovering_color=(252, 154, 154),
                    text_input=label,
                )
            )
        return buttons

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game.states import StartState

            self.game.state_machine.change(StartState(self.game))
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_volume = False
            return

        if event.type == pygame.MOUSEMOTION and self.dragging_volume:
            self._set_volume_from_mouse(event.pos[0])
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        mouse_pos = pygame.mouse.get_pos()

        if self.slider_rect.inflate(0, 24).collidepoint(mouse_pos):
            self.dragging_volume = True
            self._set_volume_from_mouse(mouse_pos[0])
            return

        for i, button in enumerate(self.progression_buttons):
            if button.checkForInput(mouse_pos):
                self.game.settings["progression_enabled"] = self.progression_options[i][1]
                return

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
                button.hovering_color = (207, 207, 207)
            else:
                button.base_color = (129, 2, 31)
                button.hovering_color = (252, 154, 154)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()

        self._set_group_button_style(
            self.progression_buttons, self.progression_options, self.game.settings["progression_enabled"]
        )
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
            self.delay_buttons, self.delay_options, self.game.settings["spawn_delay"]
        )
        if not self.dragging_volume:
            self._update_volume_knob_from_setting()

        for button in self.progression_buttons:
            button.changeColor(mouse_pos)
        for button in self.duration_buttons:
            button.changeColor(mouse_pos)
        for button in self.size_buttons:
            button.changeColor(mouse_pos)
        for button in self.difficulty_buttons:
            button.changeColor(mouse_pos)
        for button in self.delay_buttons:
            button.changeColor(mouse_pos)
        self.back_button.changeColor(mouse_pos)

    def draw(self, screen):
        screen.fill((245, 238, 205))

        center_x = self.game.width // 2

        title_text = self.font_title.render("Settings", True, (129, 2, 31))
        screen.blit(title_text, title_text.get_rect(center=(center_x, 65)))

        progression_text = self.font_section.render("Difficulty Progression", True, (20, 71, 88))
        duration_text = self.font_section.render("Game Duration", True, (20, 71, 88))
        size_text = self.font_section.render("Target Size", True, (20, 71, 88))
        difficulty_text = self.font_section.render("Difficulty", True, (20, 71, 88))
        delay_text = self.font_section.render("Delay", True, (20, 71, 88))
        volume_text = self.font_section.render("Volume", True, (20, 71, 88))

        screen.blit(progression_text, progression_text.get_rect(center=(center_x, 120)))
        screen.blit(duration_text, duration_text.get_rect(center=(center_x, 200)))
        screen.blit(size_text, size_text.get_rect(center=(center_x, 280)))
        screen.blit(difficulty_text, difficulty_text.get_rect(center=(center_x, 360)))
        screen.blit(delay_text, delay_text.get_rect(center=(center_x, 440)))
        screen.blit(volume_text, volume_text.get_rect(center=(center_x, 520)))

        pygame.draw.rect(screen, (180, 180, 180), self.slider_rect, border_radius=6)
        fill_rect = self.slider_rect.copy()
        fill_rect.width = max(1, self.slider_knob_x - self.slider_rect.left)
        pygame.draw.rect(screen, (20, 71, 88), fill_rect, border_radius=6)
        pygame.draw.circle(
            screen,
            (129, 2, 31),
            (self.slider_knob_x, self.slider_knob_y),
            self.slider_knob_radius,
        )
        pygame.draw.circle(
            screen,
            (245, 238, 205),
            (self.slider_knob_x, self.slider_knob_y),
            max(2, self.slider_knob_radius - 6),
        )
        volume_percent = int(self.game.settings["master_volume"] * 100)
        volume_value = self.font_option.render(f"{volume_percent}%", True, (129, 2, 31))
        screen.blit(volume_value, volume_value.get_rect(center=(center_x, 600)))

        for button in self.progression_buttons:
            button.update(screen)
        for button in self.duration_buttons:
            button.update(screen)
        for button in self.size_buttons:
            button.update(screen)
        for button in self.difficulty_buttons:
            button.update(screen)
        for button in self.delay_buttons:
            button.update(screen)
        self.back_button.update(screen)
