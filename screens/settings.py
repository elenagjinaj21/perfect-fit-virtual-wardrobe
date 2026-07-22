import pygame

from utils.colors import BLUE, GREEN, GRAY, WHITE


class SettingsScreen:
    def __init__(self):
        self.sound_on = True

    def handle_event(self, event, app):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                app.screen_name = "menu"
            elif self.export_rect.collidepoint(event.pos):
                from pathlib import Path
                target = Path("exports") / "outfit.png"
                try:
                    app.image_manager.save_outfit_image(str(target), app.current_outfit)
                    app.message = "Exported outfit to exports/outfit.png"
                except FileNotFoundError as error:
                    app.message = str(error)

    def update(self, app):
        return None

    def draw(self, surface, app):
        title = app.title_font.render("Settings", True, WHITE)
        surface.blit(title, (60, 60))
        surface.blit(app.font.render("Sound and export preferences", True, GRAY), (60, 110))

        self.back_rect = pygame.Rect(60, 620, 120, 40)
        self.export_rect = pygame.Rect(220, 620, 220, 40)
        pygame.draw.rect(surface, BLUE, self.back_rect, border_radius=8)
        pygame.draw.rect(surface, GREEN, self.export_rect, border_radius=8)
        surface.blit(app.font.render("Back", True, WHITE), (92, 630))
        surface.blit(app.font.render("Export current outfit", True, WHITE), (250, 630))
