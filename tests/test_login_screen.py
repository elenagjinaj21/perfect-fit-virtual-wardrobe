import unittest
from types import SimpleNamespace

import pygame

from screens.login_screen import LoginScreen
from screens.outfit_creator import OutfitCreatorScreen


class LoginScreenTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = LoginScreen()

    def test_text_input_updates_active_field(self):
        self.screen.active_field = "username"
        self.screen.handle_event(pygame.event.Event(pygame.TEXTINPUT, {"text": "a"}), object())
        self.assertEqual(self.screen.username, "a")

        self.screen.active_field = "password"
        self.screen.handle_event(pygame.event.Event(pygame.TEXTINPUT, {"text": "b"}), object())
        self.assertEqual(self.screen.password, "b")

    def test_wrong_outfit_shows_loss_message(self):
        screen = OutfitCreatorScreen()
        app = SimpleNamespace(screen_name="creator")
        screen.option_rects = [
            pygame.Rect(0, 0, 10, 10),
            pygame.Rect(0, 20, 10, 10),
            pygame.Rect(0, 40, 10, 10),
            pygame.Rect(0, 60, 10, 10),
        ]

        screen.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (5, 25), "button": 1}), app)
        screen.confirm_choice()

        self.assertEqual(screen.feedback_message, "You Lost! Try Again.")
        self.assertFalse(screen.smiling)

    def test_correct_outfit_shows_win_message(self):
        screen = OutfitCreatorScreen()
        app = SimpleNamespace(screen_name="creator")
        screen.option_rects = [pygame.Rect(0, 0, 10, 10)]

        screen.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (5, 5), "button": 1}), app)
        screen.confirm_choice()

        self.assertEqual(screen.feedback_message, "You Won!")
        self.assertTrue(screen.smiling)


if __name__ == "__main__":
    unittest.main()
