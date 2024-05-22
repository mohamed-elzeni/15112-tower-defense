# Mohamed Elzeni / msmohame
# 15-112 Term Project

import random
import pygame
import math
import os


class Bullet(pygame.sprite.Sprite):
    # this is the default bullet for the default cannon
    def __init__(self, game, selfX, selfY, enemyX, enemyY):
        super().__init__()
        self.originalImage = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'Bullet_Cannon.png')), (12, 6))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (selfX, selfY)
        self.game = game

        self.speed = 20
        self.angle = math.atan2(enemyY-selfY, enemyX-selfX)
        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed
        self.x = selfX
        self.y = selfY

        self.enemyX = enemyX
        self.enemyY = enemyY

        self.damage = 20

    def rotate(self):
        enemyX = self.enemyX
        enemyY = self.enemyY
        relativeX = enemyX - self.rect.center[0]
        relativeY = enemyY - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.image = pygame.transform.rotate(self.originalImage, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.checkIfOutOfBounds()
        self.x += self.dx
        self.y += self.dy
        self.rotate()
        self.rect.center = int(self.x), int(self.y)
        self.checkCollisionWithEnemies()

    def checkIfOutOfBounds(self):
        if self.rect.center[0] > 800 or self.rect.center[1] > 800:
            self.kill()

    def checkCollisionWithEnemies(self):
        for enemy in self.game.enemiesGroup.sprites():
            if pygame.sprite.collide_rect(self, enemy):
                enemy.health -= self.damage
                self.kill()


class MG1Bullet(Bullet):
    def __init__(self, game, selfX, selfY, enemyX, enemyY):
        super().__init__(game, selfX, selfY, enemyX, enemyY)
        self.originalImage = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'Bullet_MG.png')), (18, 5))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (selfX, selfY)
        self.game = game

        self.speed = 20
        self.angle = math.atan2(enemyY-selfY, enemyX-selfX)
        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed
        self.x = selfX
        self.y = selfY

        self.enemyX = enemyX
        self.enemyY = enemyY

        self.damage = 5


class ML1Bullet(Bullet):
    def __init__(self, game, selfX, selfY, enemyX, enemyY, targetEnemy, tower):
        super().__init__(game, selfX, selfY, enemyX, enemyY)
        self.targetEnemy = targetEnemy
        self.tower = tower
        self.originalImage = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'Missile.png')), (20, 11))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (selfX, selfY)
        self.game = game

        self.enemyX = self.targetEnemy.rect.center[0]
        self.enemyY = self.targetEnemy.rect.center[1]

        self.x = selfX
        self.y = selfY

        self.speed = 2
        self.damage = 100

        self.reachedEnemy = False
        self.uniqueThing = random.randint(1, 100)

    def rotate(self):
        self.enemyX = self.targetEnemy.rect.center[0]
        self.enemyY = self.targetEnemy.rect.center[1]
        relativeX = self.enemyX - self.rect.center[0]
        relativeY = self.enemyY - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.image = pygame.transform.rotate(self.originalImage, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.checkIfOutOfBounds()
        if not self.targetEnemy.alive():
            self.angle = math.atan2(self.enemyY-self.y, self.enemyX-self.x)
            self.dx = self.dx
            self.dy = self.dy
            self.x += self.dx
            self.y += self.dy
            self.rect.center = int(self.x), int(self.y)
            self.checkCollisionWithEnemies()
        else:
            self.rotate()
            self.angle = math.atan2(self.enemyY-self.y, self.enemyX-self.x)
            self.dx = math.cos(self.angle)*self.speed
            self.dy = math.sin(self.angle)*self.speed
            self.x += self.dx
            self.y += self.dy
            self.rect.center = int(self.x), int(self.y)
            self.checkCollisionWithEnemies()


class BigCannonBullet(Bullet):
    def __init__(self, game, selfX, selfY, enemyX, enemyY):
        super().__init__(game, selfX, selfY, enemyX, enemyY)
        self.originalImage = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'Bullet_Cannon.png')), (18, 9))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (selfX, selfY)
        self.game = game

        self.speed = 15
        self.angle = math.atan2(enemyY-selfY, enemyX-selfX)
        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed
        self.x = selfX
        self.y = selfY

        self.enemyX = enemyX
        self.enemyY = enemyY

        self.damage = 150


class MG2Bullet(Bullet):
    def __init__(self, game, selfX, selfY, enemyX, enemyY):
        super().__init__(game, selfX, selfY, enemyX, enemyY)
        self.originalImage = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'Bullet_MG.png')), (24, 7))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (selfX, selfY)
        self.game = game

        self.speed = 20
        self.angle = math.atan2(enemyY-selfY, enemyX-selfX)
        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed
        self.x = selfX
        self.y = selfY

        self.enemyX = enemyX
        self.enemyY = enemyY

        self.damage = 10


class ML2Bullet(Bullet):
    def __init__(self, game, selfX, selfY, enemyX, enemyY, targetEnemy, tower):
        super().__init__(game, selfX, selfY, enemyX, enemyY)
        self.targetEnemy = targetEnemy
        self.tower = tower
        self.originalImage = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'Missile.png')), (40, 22))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (selfX, selfY)
        self.game = game

        self.enemyX = self.targetEnemy.rect.center[0]
        self.enemyY = self.targetEnemy.rect.center[1]

        self.x = selfX
        self.y = selfY

        self.speed = 10
        self.damage = 500

        self.reachedEnemy = False
        self.uniqueThing = random.randint(1, 100)

    def rotate(self):
        self.enemyX = self.targetEnemy.rect.center[0]
        self.enemyY = self.targetEnemy.rect.center[1]
        relativeX = self.enemyX - self.rect.center[0]
        relativeY = self.enemyY - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.image = pygame.transform.rotate(self.originalImage, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.checkIfOutOfBounds()
        if not self.targetEnemy.alive():
            if len(self.tower.enemiesInRange) >= 1:
                self.targetEnemy = self.tower.enemiesInRange[0]
            else:
                self.angle = math.atan2(self.enemyY-self.y, self.enemyX-self.x)
                self.dx = self.dx
                self.dy = self.dy
                self.x += self.dx
                self.y += self.dy
                self.rect.center = int(self.x), int(self.y)
                self.checkCollisionWithEnemies()
        else:
            self.rotate()
            self.angle = math.atan2(self.enemyY-self.y, self.enemyX-self.x)
            self.dx = math.cos(self.angle)*self.speed
            self.dy = math.sin(self.angle)*self.speed
            self.x += self.dx
            self.y += self.dy
            self.rect.center = int(self.x), int(self.y)
            self.checkCollisionWithEnemies()
