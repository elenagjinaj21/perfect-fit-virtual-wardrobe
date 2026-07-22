import pygame

from utils.colors import GRAY, LIGHT_PINK, PINK, WHITE


class MenuScreen:
    def __init__(self):
        self.buttons = {}

    def handle_event(self, event, app):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    app.screen_name = name
                    break

    def update(self, app):
        return None

    def draw(self, surface, app):
        surface.fill(LIGHT_PINK)
        title = app.title_font.render("Perfect Fit", True, WHITE)
        surface.blit(title, (60, 60))
        subtitle = app.font.render("Try to make her smile", True, GRAY)
        surface.blit(subtitle, (60, 110))

        rect = pygame.Rect(60, 180, 360, 70)
        self.buttons = {"creator": rect}
        pygame.draw.rect(surface, PINK, rect, border_radius=24)
        surface.blit(app.font.render("Start styling", True, WHITE), (110, 202))

        info = app.font.render(app.message, True, GRAY)
        surface.blit(info, (60, 280))
