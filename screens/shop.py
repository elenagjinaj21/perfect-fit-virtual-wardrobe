import pygame

from utils.colors import BLUE, GRAY, GREEN, WHITE


class ShopScreen:
    def __init__(self):
        self.items = []

    def handle_event(self, event, app):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                app.screen_name = "menu"
            for idx, item in enumerate(self.items):
                rect = pygame.Rect(60, 220 + idx * 70, 420, 48)
                if rect.collidepoint(event.pos):
                    app.db.buy_clothing(app.current_user["id"], item["id"])
                    app.current_user["coins"] = app.current_user.get("coins", 100) - item["price"]
                    app.message = f"Bought {item['name']}"
                    break

    def update(self, app):
        self.items = app.db.get_clothes()

    def draw(self, surface, app):
        title = app.title_font.render("Shop", True, WHITE)
        surface.blit(title, (60, 60))
        surface.blit(app.font.render("Spend your coins on fresh wardrobe items", True, GRAY), (60, 110))

        y = 220
        for item in self.items[:5]:
            rect = pygame.Rect(60, y, 420, 48)
            pygame.draw.rect(surface, (45, 52, 65), rect, border_radius=8)
            surface.blit(app.font.render(item["name"], True, WHITE), (80, y + 10))
            surface.blit(app.font.render(f"{item['price']} coins", True, GREEN), (300, y + 10))
            y += 60

        self.back_rect = pygame.Rect(60, 620, 120, 40)
        pygame.draw.rect(surface, BLUE, self.back_rect, border_radius=8)
        surface.blit(app.font.render("Back", True, WHITE), (92, 630))
