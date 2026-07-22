# Perfect Fit — Virtual Wardrobe

Perfect Fit is a pink-themed Python/Pygame desktop game by Elena Gjinaj. It
lets players create an account, browse a wardrobe, style a character, and
choose the outfit that makes her smile.

## Features
- Account creation and login
- Wardrobe inventory with search and season filters
- Drag-and-drop outfit composition
- Outfit saving and random outfit generation
- Achievement and coin progression
- Outfit export to PNG
- Animated outfit challenge with win and retry flows
- Password hashing and duplicate-account protection

## Installation
```bash
pip install -r requirements.txt
python main.py
```

## Portfolio highlights

This project demonstrates practical skills useful for a junior Python or
game-development role:

- Object-oriented Python application structure
- Pygame event handling, animation, compositing, and responsive layout
- SQLite persistence for users, clothing, outfits, inventory, and achievements
- Secure salted PBKDF2-SHA256 password storage
- Automated tests with pytest
- Static quality checks with Flake8 and mypy
- Cross-platform project commands through a Makefile

## Project structure
- `main.py` launches the application
- `database/` stores the SQLite database and creation script
- `screens/` contains the main UI screens
- `managers/` handles persistence, exports, and assets
- `models/` contains the game domain objects

## Development checks

```text
make check
```

This runs the tests, Flake8, and mypy. On Windows, use `mingw32-make` or run
the same commands with the Python environment directly.

Individual commands are `make test`, `make lint`, `make typecheck`, and
`make run`.

## Account security

Passwords are stored using salted, memory-hard scrypt hashes. New passwords
must contain at least eight characters, including uppercase, lowercase, and a
number. Usernames are matched case-insensitively, so the same account cannot
be created twice with different capitalization. Older PBKDF2 or legacy
plain-text accounts are upgraded after a successful login.

## License

See [LICENSE](LICENSE).

## GitHub

- Owner: [Elena Gjinaj](https://github.com/elenagjinaj21)
- Suggested repository name: `perfect-fit-virtual-wardrobe`
- Suggested description: `A pink-themed Python/Pygame virtual wardrobe game with account security, outfit styling, SQLite persistence, and an animated outfit challenge.`
