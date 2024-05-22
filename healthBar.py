# Mohamed Elzeni / msmohame
# 15-112 Term Project

import pygame


class HealthBar(pygame.sprite.Sprite):
    # self.rect is the red bg
    # self.healthRect is green
    def __init__(self, game, sprite):
        super().__init__()
        self.game = game

        # the sprite that the health bar is associated with
        self.sprite = sprite

        self.width = abs(
            self.sprite.rect.topleft[0] - self.sprite.rect.topright[0])
        self.height = 10

        self.xcord = self.sprite.rect.topleft[0]
        self.ycord = self.sprite.rect.topleft[1] - self.height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.game.red)
        self.rect = self.image.get_rect()
        self.updateHealthFill()

    def update(self):
        if self.sprite.alive():
            self.updateHealthFill()
            if self.sprite in self.game.towerGroup.sprites():
                self.rect.x = self.xcord
                self.rect.y = self.sprite.rect.topleft[1] - self.height
            else:
                self.rect.x = self.sprite.rect.topleft[0]
                self.rect.y = self.sprite.rect.topleft[1] - self.height
        else:
            self.kill()

    def updateHealthFill(self):
        self.healthPercent = self.sprite.health / self.sprite.originalHealth
        self.healthWidth = int(self.healthPercent * self.width)
        if self.sprite in self.game.towerGroup.sprites():
            self.healthRect = pygame.Rect(
                self.xcord, self.sprite.rect.topleft[1] - self.height, self.healthWidth, self.height)
        else:
            self.healthRect = pygame.Rect(
                self.sprite.rect.topleft[0], self.sprite.rect.topleft[1] - self.height, self.healthWidth, self.height)
        pygame.draw.rect(self.game.win, self.game.green, self.healthRect)
