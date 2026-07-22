import pygame

from utils.colors import BLUE, GRAY, GREEN, WHITE


class ProfileScreen:
    def __init__(self):
        self.message = ""

    def handle_event(self, event, app):
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_rect.collidepoint(event.pos):
            app.screen_name = "menu"

    def update(self, app):
        if app.current_user:
            self.message = f"Coins: {app.current_user['coins']} | XP: {app.current_user['xp']}"

    def draw(self, surface, app):
        title = app.title_font.render("Profile", True, WHITE)
        surface.blit(title, (60, 60))
        if app.current_user:
            surface.blit(app.font.render(f"User: {app.current_user['username']}", True, WHITE), (60, 130))
            surface.blit(app.font.render(f"Level: {app.current_user['level']}", True, GRAY), (60, 170))
            surface.blit(app.font.render(self.message, True, GREEN), (60, 210))

        self.back_rect = pygame.Rect(60, 620, 120, 40)
        pygame.draw.rect(surface, BLUE, self.back_rect, border_radius=8)
        surface.blit(app.font.render("Back", True, WHITE), (92, 630))
