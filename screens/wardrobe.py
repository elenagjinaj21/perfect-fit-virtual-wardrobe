import pygame

from utils.colors import GRAY, GREEN, WHITE


class WardrobeScreen:
    def __init__(self):
        self.search_text = ""
        self.season = "all"

    def handle_event(self, event, app):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.search_text = self.search_text[:-1]
            elif event.unicode and event.unicode.isalnum():
                self.search_text += event.unicode
            elif event.key == pygame.K_RETURN:
                app.screen_name = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                app.screen_name = "menu"
            elif self.add_rect.collidepoint(event.pos):
                app.db.add_clothing("New Item", "accessory", 30, self.season)
                app.message = "Added a new outfit piece"

    def update(self, app):
        season = self.season if self.season != "all" else None
        self.clothes = app.db.get_clothes(season=season, search=self.search_text or None)

    def draw(self, surface, app):
        title = app.title_font.render("Wardrobe", True, WHITE)
        surface.blit(title, (60, 60))
        subtitle = app.font.render("Search clothing and filter by season", True, GRAY)
        surface.blit(subtitle, (60, 110))

        pygame.draw.rect(surface, (35, 40, 50), (60, 150, 400, 42), border_radius=8)
        surface.blit(app.font.render(self.search_text or "Search", True, WHITE), (80, 162))

        self.back_rect = pygame.Rect(60, 620, 120, 40)
        self.add_rect = pygame.Rect(210, 620, 180, 40)
        pygame.draw.rect(surface, GRAY, self.back_rect, border_radius=8)
        pygame.draw.rect(surface, GREEN, self.add_rect, border_radius=8)
        surface.blit(app.font.render("Back", True, WHITE), (92, 630))
        surface.blit(app.font.render("Add sample item", True, WHITE), (232, 630))

        y = 220
        for item in self.clothes[:6]:
            rect = pygame.Rect(60, y, 420, 48)
            pygame.draw.rect(surface, (45, 52, 65), rect, border_radius=8)
            surface.blit(app.font.render(item["name"], True, WHITE), (80, y + 10))
            surface.blit(app.font.render(f"{item['price']} coins", True, GRAY), (300, y + 10))
            y += 60
