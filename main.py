import argparse
from typing import Any, Dict, List, Optional, Protocol

import pygame

from config import DB_PATH, FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from managers.database_manager import DatabaseManager
from managers.image_manager import ImageManager
from screens.login_screen import LoginScreen
from screens.menu import MenuScreen
from screens.wardrobe import WardrobeScreen
from screens.outfit_creator import OutfitCreatorScreen
from screens.profile import ProfileScreen
from screens.shop import ShopScreen
from screens.settings import SettingsScreen


class Screen(Protocol):
    def handle_event(self, event: pygame.event.Event, app: "StyleStudioApp") -> None:
        ...

    def update(self, app: "StyleStudioApp") -> None:
        ...

    def draw(self, surface: pygame.Surface, app: "StyleStudioApp") -> None:
        ...


class StyleStudioApp:
    def __init__(self, db_path: Optional[str] = None):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Perfect Fit")
        self.clock = pygame.time.Clock()
        self.db = DatabaseManager(str(db_path or DB_PATH))
        self.db.create_tables()
        self.db.seed_demo_clothes()
        self.running = True
        self.screen_name = "login"
        self.current_user = None
        self.current_outfit: List[Any] = []
        self.message = "Welcome to Perfect Fit"
        self.font = pygame.font.SysFont("arial", 24)
        self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        self.image_manager = ImageManager()
        self.screens: Dict[str, Screen] = {
            "login": LoginScreen(),
            "menu": MenuScreen(),
            "wardrobe": WardrobeScreen(),
            "profile": ProfileScreen(),
            "shop": ShopScreen(),
            "settings": SettingsScreen(),
        }
        self.creator_screen: Optional[Screen] = None

    def get_current_screen(self) -> Screen:
        if self.screen_name == "creator":
            if self.creator_screen is None:
                self.creator_screen = OutfitCreatorScreen()
            return self.creator_screen
        return self.screens[self.screen_name]

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.get_current_screen().handle_event(event, self)

            self.get_current_screen().update(self)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def draw(self):
        self.screen.fill((255, 235, 245))
        self.get_current_screen().draw(self.screen, self)
        pygame.display.update()


def parse_args():
    parser = argparse.ArgumentParser(description="Style Studio virtual wardrobe")
    parser.add_argument("--db-path", default=str(DB_PATH), help="Path to the SQLite database")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app = StyleStudioApp(args.db_path)
    app.run()
