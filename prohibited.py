import pygame


class ProhibitedArea(pygame.sprite.Sprite):
    # x, y are topleft
    # x2, y2 are bottomright
    def __init__(self, x, y, x2, y2):
        super().__init__()
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.width = self.x2 - self.x
        self.height = self.y2 - self.y
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.rect.topleft = (self.x, self.y)
