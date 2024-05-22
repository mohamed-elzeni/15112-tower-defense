# Mohamed Elzeni / msmohame
# 15-112 Term Project

import pygame
import os
import healthBar


class Household(pygame.sprite.Sprite):
    def __init__(self, game, health=200):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join('Assets', 'house.png'))
        self.rect = self.image.get_rect()
        self.game = game

        self.originalHealth = health
        self.health = self.originalHealth

        self.addHealthBar()

    def update(self):
        self.checkForDeath()
        self.rect.bottomright = self.game.levelDict["household pos"]

    def checkForDeath(self):
        if self.health <= 0:
            score = self.game.score
            self.game.reset()
            self.game.score = score
            self.game.gameActive = False
            self.game.winLoseMessage = "You Lost!"

    def addHealthBar(self):
        self.game.healthBarGroup.add(healthBar.HealthBar(self.game, self))
