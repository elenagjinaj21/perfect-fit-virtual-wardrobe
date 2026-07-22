class SoundManager:
    def __init__(self):
        self.enabled = True

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled
