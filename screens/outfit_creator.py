import math
from pathlib import Path

import pygame

from utils.colors import BLUE, GOLD, GRAY, GREEN, LIGHT_PINK, PINK, WHITE

OUTFIT_KEYS = ("pink", "blue", "green", "gold")
TRANSITION_FRAMES = 18
OUTFIT_SOURCE_REGIONS = (
    (0.02, 0.12, 0.24, 0.96),
    (0.30, 0.12, 0.47, 0.96),
    (0.53, 0.13, 0.71, 0.96),
    (0.78, 0.13, 0.96, 0.97),
)
WRONG_CHOICE_REGIONS = (
    (0.04, 0.08, 0.32, 0.96),
    (0.36, 0.08, 0.66, 0.96),
    (0.71, 0.08, 0.96, 0.96),
)
FUNNY_CAPTIONS = (
    "Royal frosting mode activated.",
    "Denim said, 'I woke up practical.'",
    "Lime drama with extra twirl.",
    "Cat hoodie chaos has entered the chat.",
)


class OutfitCreatorScreen:
    def __init__(self):
        self.smiling = False
        self.animation_frame = 0
        self.cheer_rect = pygame.Rect(0, 0, 0, 0)
        self.back_rect = pygame.Rect(0, 0, 0, 0)
        self.clothes_img = None
        self.choices_img = None
        self.outfit_images = []
        self.avatar_outfit_images = []
        self.wrong_choice_images = []
        self.winning_outfit_img = None
        self.winning_outfit_img_scaled = None
        self.option_rects = []
        self.confirm_rect = pygame.Rect(0, 0, 0, 0)
        self.character_img = None
        self.character_img_scaled = None
        self.current_outfit = "pink"
        self.selected_outfit_index = None
        self.visible_outfit_index = None
        self.pending_outfit_index = None
        self.transition_frame = 0
        self.feedback_message = "Pick the outfit that makes her smile."
        self.correct_outfit = "pink"
        self.status_message = "She is waiting to smile..."
        self.result_state = None
        self.outfit_options = [
            ("Pink Dress", PINK, "pink"),
            ("Blue Jacket", BLUE, "blue"),
            ("Green Skirt", GREEN, "green"),
            ("Golden Coat", GOLD, "gold"),
        ]
        self._load_character_image()
        self._load_clothes_image()
        self._load_choices_image()
        self._load_winning_outfit_image()

    def _load_character_image(self):
        character_path = Path(__file__).parent.parent / "assets" / "images" / "character.png"
        if not character_path.exists():
            return
        try:
            self.character_img = pygame.image.load(str(character_path)).convert_alpha()
            max_width, max_height = 320, 440
            scale = min(max_width / self.character_img.get_width(), max_height / self.character_img.get_height(), 1.0)
            width = int(self.character_img.get_width() * scale)
            height = int(self.character_img.get_height() * scale)
            self.character_img_scaled = pygame.transform.smoothscale(self.character_img, (width, height))
        except Exception:
            self.character_img = None
            self.character_img_scaled = None

    def _load_clothes_image(self):
        asset_path = Path(__file__).parent.parent / "assets" / "images" / "clothes.png"
        downloads_path = Path.home() / "Downloads" / "clothes.png"
        spaced_downloads_path = Path.home() / "Downloads" / "clothes .png"
        image_path = self._first_existing_path(asset_path, downloads_path, spaced_downloads_path)
        if not image_path.exists():
            return

        try:
            self.clothes_img = pygame.image.load(str(image_path)).convert_alpha()
            self.clothes_img = self._scale_for_processing(self.clothes_img, 600)
            self.clothes_img = self._make_background_transparent(self.clothes_img)
            self.outfit_images = self._split_outfit_sheet(self.clothes_img, (110, 112))
            self.avatar_outfit_images = self._split_outfit_sheet(self.clothes_img, (230, 350))
        except Exception:
            self.clothes_img = None
            self.outfit_images = []
            self.avatar_outfit_images = []

    def _load_choices_image(self):
        asset_path = Path(__file__).parent.parent / "assets" / "images" / "choices.png"
        downloads_path = Path.home() / "Downloads" / "choices.png"
        image_path = self._first_existing_path(asset_path, downloads_path)
        if not image_path.exists():
            return

        try:
            self.choices_img = pygame.image.load(str(image_path)).convert_alpha()
            self.choices_img = self._scale_for_processing(self.choices_img, 600)
            self.choices_img = self._make_background_transparent(self.choices_img)
            self.wrong_choice_images = self._split_choice_sheet(self.choices_img, (320, 500))
        except Exception:
            self.choices_img = None
            self.wrong_choice_images = []

    def _load_winning_outfit_image(self):
        asset_path = Path(__file__).parent.parent / "assets" / "images" / "pinkdress.png"
        downloads_path = Path.home() / "Downloads" / "pinkdress.png"
        image_path = self._first_existing_path(asset_path, downloads_path)
        if not image_path.exists():
            return

        try:
            self.winning_outfit_img = pygame.image.load(str(image_path)).convert_alpha()
            self.winning_outfit_img = self._scale_for_processing(self.winning_outfit_img, 600)
            self.winning_outfit_img = self._make_background_transparent(self.winning_outfit_img)
            self.winning_outfit_img_scaled = self._scale_to_fit(self.winning_outfit_img, (390, 500))
        except Exception:
            self.winning_outfit_img = None
            self.winning_outfit_img_scaled = None

    def _first_existing_path(self, *paths):
        for path in paths:
            if path.exists():
                return path
        return paths[0]

    def _scale_for_processing(self, image, max_dimension):
        largest_dimension = max(image.get_width(), image.get_height())
        if largest_dimension <= max_dimension:
            return image
        scale = max_dimension / largest_dimension
        size = (max(1, int(image.get_width() * scale)), max(1, int(image.get_height() * scale)))
        return pygame.transform.smoothscale(image, size)

    def _make_background_transparent(self, image):
        cleaned = image.copy()
        for x in range(cleaned.get_width()):
            for y in range(cleaned.get_height()):
                color = cleaned.get_at((x, y))
                is_white = color.r > 240 and color.g > 240 and color.b > 240
                is_neutral = max(color.r, color.g, color.b) - min(color.r, color.g, color.b) < 12
                if is_white and is_neutral:
                    cleaned.set_at((x, y), (255, 255, 255, 0))
        return cleaned

    def _split_outfit_sheet(self, sheet, max_size):
        outfits = []
        for area in self._source_regions(sheet):
            outfit = sheet.subsurface(area).copy()
            outfit.set_colorkey((0, 0, 0))
            outfit = self._trim_visible_pixels(outfit)
            outfits.append(self._scale_to_fit(outfit, max_size))
        return outfits

    def _source_regions(self, sheet):
        areas = []
        for left, top, right, bottom in OUTFIT_SOURCE_REGIONS:
            x = int(sheet.get_width() * left)
            y = int(sheet.get_height() * top)
            width = int(sheet.get_width() * right) - x
            height = int(sheet.get_height() * bottom) - y
            areas.append(pygame.Rect(x, y, width, height))
        return areas

    def _split_choice_sheet(self, sheet, max_size):
        choices = []
        for left, top, right, bottom in WRONG_CHOICE_REGIONS:
            x = int(sheet.get_width() * left)
            y = int(sheet.get_height() * top)
            width = int(sheet.get_width() * right) - x
            height = int(sheet.get_height() * bottom) - y
            character = sheet.subsurface(pygame.Rect(x, y, width, height)).copy()
            character = self._trim_visible_pixels(character)
            choices.append(self._scale_to_fit(character, max_size))
        return choices

    def _trim_visible_pixels(self, image):
        image = self._remove_small_artifacts(image)
        left = image.get_width()
        top = image.get_height()
        right = 0
        bottom = 0
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                if self._is_visible_outfit_pixel(image.get_at((x, y))):
                    left = min(left, x)
                    top = min(top, y)
                    right = max(right, x)
                    bottom = max(bottom, y)

        if left > right or top > bottom:
            return image

        padding = 6
        rect = pygame.Rect(
            max(0, left - padding),
            max(0, top - padding),
            min(image.get_width(), right + padding) - max(0, left - padding),
            min(image.get_height(), bottom + padding) - max(0, top - padding),
        )
        trimmed = image.subsurface(rect).copy()
        trimmed.set_colorkey((0, 0, 0))
        return trimmed

    def _remove_small_artifacts(self, image):
        visited: set[tuple[int, int]] = set()
        components = []
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                if (x, y) in visited or not self._is_visible_outfit_pixel(image.get_at((x, y))):
                    continue
                component = self._collect_component(image, x, y, visited)
                components.append(component)

        cleaned = image.copy()
        for component in components:
            if len(component) < 450:
                for x, y in component:
                    cleaned.set_at((x, y), (0, 0, 0, 0))
        cleaned.set_colorkey((0, 0, 0))
        return cleaned

    def _collect_component(self, image, start_x, start_y, visited):
        component = []
        stack = [(start_x, start_y)]
        visited.add((start_x, start_y))
        while stack:
            x, y = stack.pop()
            component.append((x, y))
            for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if (
                    next_x < 0
                    or next_y < 0
                    or next_x >= image.get_width()
                    or next_y >= image.get_height()
                    or (next_x, next_y) in visited
                    or not self._is_visible_outfit_pixel(image.get_at((next_x, next_y)))
                ):
                    continue
                visited.add((next_x, next_y))
                stack.append((next_x, next_y))
        return component

    def _is_visible_outfit_pixel(self, color):
        return color.a > 10 and (color.r > 12 or color.g > 12 or color.b > 12)

    def _scale_to_fit(self, image, max_size):
        max_width, max_height = max_size
        scale = min(max_width / image.get_width(), max_height / image.get_height(), 1.0)
        width = max(1, int(image.get_width() * scale))
        height = max(1, int(image.get_height() * scale))
        return pygame.transform.smoothscale(image, (width, height))

    def _remove_base_hands(self, image):
        """Remove base hands because outfit artwork includes its own hands."""
        cleaned = image.copy()
        width, height = cleaned.get_size()
        hand_regions = (
            pygame.Rect(int(width * 0.17), int(height * 0.41), int(width * 0.17), int(height * 0.13)),
            pygame.Rect(int(width * 0.66), int(height * 0.41), int(width * 0.17), int(height * 0.13)),
        )
        for region in hand_regions:
            pygame.draw.rect(cleaned, (0, 0, 0, 0), region)
        return cleaned

    def handle_event(self, event, app):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                app.screen_name = "login" if self.result_state == "win" else "menu"
                if self.result_state == "win":
                    app.current_user = None
                    app.message = "You won! Sign in to play again."
                    login_screen = app.screens.get("login")
                    if login_screen is not None:
                        login_screen.username = ""
                        login_screen.password = ""
                        login_screen.active_field = "username"
                self.smiling = False
                self.feedback_message = "Pick the outfit that makes her smile."
                self.status_message = "She is waiting to smile..."
                self.current_outfit = "pink"
                self.selected_outfit_index = None
                self.visible_outfit_index = None
                self.pending_outfit_index = None
                self.transition_frame = 0
                self.result_state = None
                return

            if (
                self.confirm_rect.collidepoint(event.pos)
                and self.selected_outfit_index is not None
                and self.result_state is None
            ):
                self.confirm_choice()
                return

            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.select_outfit(index)
                    break

    def select_outfit(self, index):
        if index == self.selected_outfit_index and self.pending_outfit_index is None:
            return

        self.selected_outfit_index = index
        self.current_outfit = OUTFIT_KEYS[index]
        self.pending_outfit_index = index
        self.transition_frame = TRANSITION_FRAMES
        self.result_state = None
        self.smiling = False
        self.feedback_message = FUNNY_CAPTIONS[index]
        self.status_message = FUNNY_CAPTIONS[index]

    def confirm_choice(self):
        if self.current_outfit == self.correct_outfit:
            self.smiling = True
            self.result_state = "win"
            self.feedback_message = "You Won!"
            self.status_message = "You Won!"
        else:
            self.smiling = False
            self.result_state = "lose"
            self.feedback_message = "You Lost! Try Again."
            self.status_message = "You Lost! Try Again."

    def update(self, app):
        self.animation_frame += 1
        if self.animation_frame > 9999:
            self.animation_frame = 0
        if self.transition_frame > 0:
            self.transition_frame -= 1
            if self.pending_outfit_index is not None and self.transition_frame <= TRANSITION_FRAMES // 2:
                self.visible_outfit_index = self.pending_outfit_index
                self.pending_outfit_index = None

    def draw_character(self, surface, center_x, center_y):
        bob = math.sin(self.animation_frame * 0.08) * 8
        transition = self.transition_frame / TRANSITION_FRAMES if self.transition_frame else 0
        bounce = -math.sin((1 - transition) * math.pi) * 22 if transition else 0
        tilt = math.sin((1 - transition) * math.pi * 2) * 6 if transition else 0
        avatar_center = (center_x, int(center_y + bob + bounce))

        avatar_layer = pygame.Surface((330, 455), pygame.SRCALPHA)
        layer_center = (avatar_layer.get_width() // 2, avatar_layer.get_height() // 2)

        if self.avatar_outfit_images and self.visible_outfit_index is not None:
            if self.character_img_scaled:
                base_character = self._remove_base_hands(self.character_img_scaled)
                img_rect = base_character.get_rect(center=(layer_center[0], layer_center[1] + 12))
                avatar_layer.blit(base_character, img_rect)

            outfit = self.avatar_outfit_images[self.visible_outfit_index]
            outfit_rect = outfit.get_rect(center=(layer_center[0], layer_center[1] + 44))
            avatar_layer.blit(outfit, outfit_rect)
        elif self.character_img_scaled:
            img_rect = self.character_img_scaled.get_rect(center=(layer_center[0], layer_center[1] + 12))
            avatar_layer.blit(self.character_img_scaled, img_rect)

        if tilt:
            avatar_layer = pygame.transform.rotozoom(avatar_layer, tilt, 1.0)

        avatar_rect = avatar_layer.get_rect(center=avatar_center)
        surface.blit(avatar_layer, avatar_rect)

    def draw(self, surface, app):
        if self.result_state == "win":
            surface.fill(LIGHT_PINK)

            title = app.title_font.render("Perfect Fit", True, PINK)
            surface.blit(title, (50, 40))
            win_text = app.title_font.render("You Won!", True, (140, 20, 90))
            surface.blit(win_text, (50, 110))

            if self.winning_outfit_img_scaled:
                outfit_rect = self.winning_outfit_img_scaled.get_rect(
                    center=(surface.get_width() // 2, surface.get_height() // 2 + 20)
                )
                surface.blit(self.winning_outfit_img_scaled, outfit_rect)

            self.back_rect = pygame.Rect(surface.get_width() // 2 - 90, surface.get_height() - 90, 180, 48)
            pygame.draw.rect(surface, (255, 190, 220), self.back_rect, border_radius=14)
            pygame.draw.rect(surface, PINK, self.back_rect, 2, border_radius=14)
            surface.blit(
                app.font.render("Back to account", True, (90, 40, 70)),
                (self.back_rect.x + 22, self.back_rect.y + 14),
            )
            return

        if self.result_state == "lose":
            surface.fill(LIGHT_PINK)

            title = app.title_font.render("Perfect Fit", True, PINK)
            surface.blit(title, (50, 40))
            lose_text = app.title_font.render("You Lost! Try Again.", True, (140, 20, 90))
            surface.blit(lose_text, (50, 110))
            caption = app.font.render("You know you can do better than that.......", True, (110, 20, 70))
            surface.blit(caption, (50, 158))

            wrong_index = max(0, self.selected_outfit_index - 1) if self.selected_outfit_index is not None else 0
            if wrong_index < len(self.wrong_choice_images):
                character = self.wrong_choice_images[wrong_index]
                character_rect = character.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 25))
                surface.blit(character, character_rect)
            else:
                self.draw_character(surface, surface.get_width() // 2, surface.get_height() // 2 + 40)

            self.back_rect = pygame.Rect(surface.get_width() // 2 - 90, surface.get_height() - 90, 180, 48)
            pygame.draw.rect(surface, (255, 190, 220), self.back_rect, border_radius=14)
            pygame.draw.rect(surface, PINK, self.back_rect, 2, border_radius=14)
            surface.blit(app.font.render("Back", True, (90, 40, 70)), (self.back_rect.x + 60, self.back_rect.y + 14))
            return

        surface.fill(LIGHT_PINK)

        title = app.title_font.render("Perfect Fit", True, PINK)
        surface.blit(title, (50, 40))
        subtitle = app.font.render("Choose the outfit that makes her smile.", True, GRAY)
        surface.blit(subtitle, (50, 90))

        panel = pygame.Rect(40, 130, 720, 420)
        pygame.draw.rect(surface, WHITE, panel, border_radius=30)
        pygame.draw.rect(surface, PINK, panel, 4, border_radius=30)

        self.draw_character(surface, 545, 345)

        question = "Which outfit makes her smile?"
        question_surf = app.font.render(question, True, (120, 30, 90))
        surface.blit(question_surf, (60, 158))

        status = self.status_message
        status_surf = app.font.render(status, True, (110, 20, 70))
        surface.blit(status_surf, (60, 190))

        self.option_rects = []
        for index, (label, color, outfit_key) in enumerate(self.outfit_options):
            row = index // 2
            column = index % 2
            rect = pygame.Rect(60 + column * 140, 225 + row * 155, 125, 140)
            self.option_rects.append(rect)
            is_selected = self.selected_outfit_index == index
            fill_color = (255, 246, 250) if not is_selected else (255, 214, 234)
            border_color = PINK if not is_selected else (255, 92, 166)
            border_width = 3 if not is_selected else 5
            pygame.draw.rect(surface, fill_color, rect, border_radius=14)
            pygame.draw.rect(surface, border_color, rect, border_width, border_radius=14)

            if index < len(self.outfit_images):
                outfit = self.outfit_images[index]
                outfit_rect = outfit.get_rect(center=(rect.centerx, rect.centery - 10))
                surface.blit(outfit, outfit_rect)
            else:
                label_surf = app.font.render(label, True, color)
                label_rect = label_surf.get_rect(center=rect.center)
                surface.blit(label_surf, label_rect)

            if is_selected:
                selected_text = app.font.render("Selected", True, (120, 30, 90))
                text_rect = selected_text.get_rect(center=(rect.centerx, rect.bottom - 15))
                surface.blit(selected_text, text_rect)

        if self.selected_outfit_index is not None:
            self.confirm_rect = pygame.Rect(510, 560, 210, 48)
            pygame.draw.rect(surface, (255, 190, 220), self.confirm_rect, border_radius=14)
            pygame.draw.rect(surface, PINK, self.confirm_rect, 2, border_radius=14)
            surface.blit(
                app.font.render("OK this choice", True, (90, 40, 70)),
                (self.confirm_rect.x + 30, self.confirm_rect.y + 14),
            )
        else:
            self.confirm_rect = pygame.Rect(0, 0, 0, 0)

        self.back_rect = pygame.Rect(300, 560, 180, 48)
        pygame.draw.rect(surface, (255, 190, 220), self.back_rect, border_radius=14)
        pygame.draw.rect(surface, PINK, self.back_rect, 2, border_radius=14)
        surface.blit(app.font.render("Back", True, (90, 40, 70)), (self.back_rect.x + 60, self.back_rect.y + 14))
