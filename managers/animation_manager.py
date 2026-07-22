class AnimationManager:
    def __init__(self):
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % 4
        return self.frame
