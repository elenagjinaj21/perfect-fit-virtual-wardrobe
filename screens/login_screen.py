from sqlite3 import IntegrityError

import pygame

from utils.colors import GRAY, LIGHT_PINK, PINK, WHITE
from utils.security import needs_rehash, verify_password
from utils.validation import is_valid_password, is_valid_username

INPUT_TEXT = (220, 70, 145)
PLACEHOLDER_TEXT = (210, 130, 170)


class LoginScreen:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.active_field = "username"
        self.message = "Create an account or sign in"
        self.login_rect = pygame.Rect(0, 0, 0, 0)
        self.create_rect = pygame.Rect(0, 0, 0, 0)
        self.username_rect = pygame.Rect(0, 0, 0, 0)
        self.password_rect = pygame.Rect(0, 0, 0, 0)
        pygame.key.start_text_input()
        self.avatar_img = None
        self.animation_frame = 0
        # No default avatar is displayed on the login screen.

    def _render_clipped(self, surface, font, text, color, rect, padding: int = 14):
        """Render text clipped to fit inside rect with ellipsis if needed."""
        max_width = rect.width - padding * 2
        display = text
        if font.size(display)[0] > max_width:
            # shorten and add ellipsis
            ellipsis = "..."
            # Reserve width for ellipsis
            ellips_w = font.size(ellipsis)[0]
            # start trimming until it fits
            while display and font.size(display)[0] + ellips_w > max_width:
                display = display[:-1]
            display = display + ellipsis if display else ellipsis

        text_surf = font.render(display, True, color)
        surface.blit(text_surf, (rect.x + padding, rect.y + (rect.height - text_surf.get_height()) // 2))

    def handle_event(self, event, app):
        if event.type == pygame.TEXTINPUT:
            self._append_text(event.text)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_field = "password" if self.active_field == "username" else "username"
            elif event.key == pygame.K_BACKSPACE:
                self._remove_char()
            elif event.key == pygame.K_RETURN:
                self.login(app)
            elif event.key == pygame.K_ESCAPE:
                self.username = ""
                self.password = ""
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_rect.collidepoint(event.pos):
                self.active_field = "username"
            elif self.password_rect.collidepoint(event.pos):
                self.active_field = "password"
            elif self.login_rect.collidepoint(event.pos):
                self.login(app)
            elif self.create_rect.collidepoint(event.pos):
                self.create_account(app)

    def _append_text(self, text: str):
        if not text:
            return
        if self.active_field == "username":
            self.username += text
        else:
            self.password += text

    def _remove_char(self):
        if self.active_field == "username":
            self.username = self.username[:-1]
        else:
            self.password = self.password[:-1]

    def login(self, app):
        self.username = self.username.strip()
        if not is_valid_username(self.username) or not is_valid_password(self.password):
            self.message = "Use a username and password of at least 3/4 characters"
            return
        user = app.db.get_user(self.username)
        if user and verify_password(self.password, user["password"]):
            if needs_rehash(user["password"]):
                app.db.update_password(user["id"], self.password)
            app.current_user = user
            app.message = f"Welcome back, {self.username}!"
            app.screen_name = "creator"
        else:
            self.message = "Account not found. Try creating one."

    def create_account(self, app):
        self.username = self.username.strip()
        if not is_valid_username(self.username) or not is_valid_password(self.password):
            self.message = "Use a username and password of at least 3/4 characters"
            return
        existing = app.db.get_user(self.username)
        if existing:
            self.message = "That account already exists"
            return
        try:
            user_id = app.db.add_user(self.username, self.password)
        except IntegrityError:
            self.message = "That account already exists"
            return
        app.current_user = {"id": user_id, "username": self.username, "coins": 100, "xp": 0, "level": 1}
        app.message = f"Account created for {self.username}"
        app.screen_name = "creator"

    def update(self, app):
        # update animation frame
        self.animation_frame = (self.animation_frame + 1) % 120
        return None

    def draw(self, surface, app):
        surface.fill(LIGHT_PINK)

        # Small decorative accents keep the screen playful without relying on
        # an external image asset.
        pygame.draw.circle(surface, (255, 202, 230), (70, 80), 22)
        pygame.draw.circle(surface, (255, 202, 230), (surface.get_width() - 75, 120), 30)
        pygame.draw.circle(surface, (255, 214, 236), (surface.get_width() - 120, surface.get_height() - 80), 18)

        panel_width, panel_height = 680, 550
        panel_rect = pygame.Rect(
            (surface.get_width() - panel_width) // 2,
            (surface.get_height() - panel_height) // 2,
            panel_width,
            panel_height,
        )
        shadow_rect = panel_rect.move(0, 8)
        pygame.draw.rect(surface, (235, 170, 205), shadow_rect, border_radius=30)
        pygame.draw.rect(surface, WHITE, panel_rect, border_radius=30)
        pygame.draw.rect(surface, (255, 150, 205), panel_rect, 3, border_radius=30)

        # Centered pink logo and game name.
        pygame.draw.circle(surface, (255, 196, 225), (panel_rect.centerx, panel_rect.top + 54), 29)
        pygame.draw.circle(surface, PINK, (panel_rect.centerx, panel_rect.top + 54), 29, 3)
        logo_font = pygame.font.SysFont("arial", 27, bold=True)
        logo = logo_font.render("P", True, WHITE)
        surface.blit(logo, logo.get_rect(center=(panel_rect.centerx, panel_rect.top + 54)))
        title = app.title_font.render("Perfect Fit", True, PINK)
        title_rect = title.get_rect(center=(panel_rect.centerx, panel_rect.top + 100))
        surface.blit(title, title_rect)
        subtitle = app.font.render("Log in and help her smile", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(panel_rect.centerx, panel_rect.top + 133))
        surface.blit(subtitle, subtitle_rect)

        # input boxes
        input_width = panel_rect.width - 160
        input_left = panel_rect.left + 60
        username_label = app.font.render("Username", True, (140, 80, 120))
        surface.blit(username_label, (input_left, panel_rect.top + 155))
        self.username_rect = pygame.Rect(input_left, panel_rect.top + 180, input_width, 54)
        password_label = app.font.render("Password", True, (140, 80, 120))
        surface.blit(password_label, (input_left, panel_rect.top + 248))
        self.password_rect = pygame.Rect(input_left, panel_rect.top + 273, input_width, 54)
        box_fill = WHITE
        pygame.draw.rect(surface, box_fill, self.username_rect, border_radius=12)
        username_border = PINK if self.active_field == "username" else (230, 190, 210)
        pygame.draw.rect(surface, username_border, self.username_rect, 2, border_radius=12)
        username_text = self.username if self.username else "Username"
        username_color = INPUT_TEXT if self.username else PLACEHOLDER_TEXT
        self._render_clipped(surface, app.font, username_text, username_color, self.username_rect, padding=18)

        pygame.draw.rect(surface, box_fill, self.password_rect, border_radius=12)
        password_border = PINK if self.active_field == "password" else (230, 190, 210)
        pygame.draw.rect(surface, password_border, self.password_rect, 2, border_radius=12)
        password_text = "*" * len(self.password) if self.password else "Password"
        password_color = INPUT_TEXT if self.password else PLACEHOLDER_TEXT
        self._render_clipped(surface, app.font, password_text, password_color, self.password_rect, padding=18)

        # action buttons
        hint = pygame.font.SysFont("arial", 16).render("Use 8+ characters with upper, lower, and a number.", True, GRAY)
        surface.blit(hint, (input_left, panel_rect.top + 338))
        buttons_top = panel_rect.top + 375
        self.login_rect = pygame.Rect(input_left, buttons_top, 220, 52)
        self.create_rect = pygame.Rect(input_left + 240, buttons_top, 220, 52)
        pygame.draw.rect(surface, (255, 185, 220), self.login_rect, border_radius=14)
        pygame.draw.rect(surface, (255, 200, 232), self.create_rect, border_radius=14)
        pygame.draw.rect(surface, PINK, self.login_rect, 2, border_radius=14)
        pygame.draw.rect(surface, (255, 160, 195), self.create_rect, 2, border_radius=14)
        login_text = app.font.render("Log in", True, (90, 40, 70))
        surface.blit(login_text, login_text.get_rect(center=self.login_rect.center))
        surface.blit(
            app.font.render("Create account", True, (90, 40, 70)),
            (self.create_rect.centerx - 74, self.create_rect.y + 15),
        )

        # message
        message = app.font.render(self.message, True, (140, 80, 120))
        message_rect = message.get_rect(center=(panel_rect.centerx, panel_rect.top + 455))
        surface.blit(message, message_rect)
