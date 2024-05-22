# Mohamed Elzeni / msmohame
# 15-112 Term Project

import pygame
import bullet
import math
import os
import healthBar


class Tower(pygame.sprite.Sprite):
    # this is the normal cannon (cannon1)
    def __init__(self, game):
        super().__init__()
        self.originalImage = pygame.image.load(
            os.path.join('Assets', 'Tower', 'Cannon1.png'))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.isPlaced = False
        self.x = 0
        self.y = 0
        self.range = 150
        self.game = game
        self.enemiesInRange = []

        self.cost = 50
        self.originalHealth = 300
        self.health = self.originalHealth

        # time to wait after shooting a bullet (in milliseconds)
        self.coolDown = 1500
        self.lastShotTime = 0

    def addHealthBar(self):
        self.game.healthBarGroup.add(healthBar.HealthBar(self.game, self))

    def update(self):
        if self.health > 0:
            self.detectEnemiesInRange()
            if not self.isPlaced:
                self.rect.center = pygame.mouse.get_pos()
                if self.game.canAddTower(self):
                    pygame.draw.circle(self.game.win, (0, 255, 0), [
                        self.rect.center[0], self.rect.center[1]], self.range, 5)
                else:
                    pygame.draw.circle(self.game.win, (255, 0, 0), [
                        self.rect.center[0], self.rect.center[1]], self.range, 5)
            else:
                if len(self.enemiesInRange) >= 1:
                    self.rotate()
                self.rect.center = [self.x, self.y]
                if len(self.enemiesInRange) > 0 and (self.game.currentTime - self.lastShotTime > self.coolDown):
                    self.shoot()
                    self.lastShotTime = self.game.currentTime
        else:
            self.kill()

    def getDistance(self, x1, y1, x2, y2):
        return ((x2-x1)**2 + (y2-y1)**2)**(1/2)

    def inRange(self, enemy):
        enemyBorderPoints = [(enemy.rect.topleft[0],
                              enemy.rect.topleft[1]),
                             (enemy.rect.topright[0],
                             enemy.rect.topright[1]),
                             (enemy.rect.bottomleft[0],
                              enemy.rect.bottomleft[1]),
                             (enemy.rect.bottomright[0],
                             enemy.rect.bottomright[1])]
        towerCenter = self.rect.center

        for point in enemyBorderPoints:
            if self.getDistance(point[0], point[1], towerCenter[0], towerCenter[1]) <= self.range:
                return True

    def detectEnemiesInRange(self):
        self.enemiesInRange.clear()
        for enemy in self.game.enemiesGroup.sprites():
            if self.inRange(enemy):
                if enemy not in self.enemiesInRange:
                    self.enemiesInRange += [enemy]
            elif enemy in self.enemiesInRange:
                self.enemiesInRange.remove(enemy)

    def rotate(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        relativeX = enemyX - self.rect.center[0]
        relativeY = enemyY - self.rect.center[1]
        angle = (180 / math.pi) * -math.atan2(relativeY, relativeX)
        self.image = pygame.transform.rotate(self.originalImage, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        myBullet = bullet.Bullet(self.game,
                                 self.rect.center[0], self.rect.center[1], enemyX, enemyY)
        self.game.bulletGroup.add(myBullet)

    def subtractCost(self):
        self.game.currentBalance -= self.cost
        self.game.addMessageToList(
            f"              -${self.cost}", messageColor='#FF0000')


class MachineGun(Tower):
    def __init__(self, game):
        super().__init__(game)
        self.originalImage = pygame.image.load(
            os.path.join('Assets', 'Tower', 'MG1.png'))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.isPlaced = False
        self.x = 0
        self.y = 0
        self.range = 100
        self.game = game
        self.enemiesInRange = []

        self.cost = 100

        self.originalHealth = 300
        self.health = self.originalHealth

        # time to wait after shooting a bullet (in milliseconds)
        self.coolDown = 100
        self.lastShotTime = 0

    def shoot(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        myBullet = bullet.MG1Bullet(self.game,
                                    self.rect.center[0], self.rect.center[1], enemyX, enemyY)
        self.game.bulletGroup.add(myBullet)


class MissileLauncher(Tower):
    def __init__(self, game):
        super().__init__(game)
        self.originalImage = pygame.image.load(
            os.path.join('Assets', 'Tower', 'ML1.png'))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.isPlaced = False
        self.x = 0
        self.y = 0
        self.range = 500
        self.game = game
        self.enemiesInRange = []

        self.cost = 150

        self.originalHealth = 300
        self.health = self.originalHealth

        # time to wait after shooting a bullet (in milliseconds)
        self.coolDown = 3000
        self.lastShotTime = 0

    def shoot(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        myBullet = bullet.ML1Bullet(self.game,
                                    self.rect.center[0], self.rect.center[1], enemyX, enemyY, self.enemiesInRange[0], self)
        self.game.bulletGroup.add(myBullet)


class BigCannon(Tower):
    def __init__(self, game):
        super().__init__(game)
        self.originalImage = pygame.image.load(
            os.path.join('Assets', 'Tower', 'Cannon2.png'))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.isPlaced = False
        self.x = 0
        self.y = 0
        self.range = 250
        self.game = game
        self.enemiesInRange = []

        self.cost = 200

        self.originalHealth = 400
        self.health = self.originalHealth

        # time to wait after shooting a bullet (in milliseconds)
        self.coolDown = 3000
        self.lastShotTime = 0

    def shoot(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        myBullet = bullet.BigCannonBullet(self.game,
                                          self.rect.center[0], self.rect.center[1], enemyX, enemyY)
        self.game.bulletGroup.add(myBullet)


class BigMachineGun(Tower):
    def __init__(self, game):
        super().__init__(game)
        self.originalImage = pygame.image.load(
            os.path.join('Assets', 'Tower', 'MG2.png'))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.isPlaced = False
        self.x = 0
        self.y = 0
        self.range = 200
        self.game = game
        self.enemiesInRange = []

        self.cost = 300

        self.originalHealth = 100
        self.health = self.originalHealth

        # time to wait after shooting a bullet (in milliseconds)
        self.coolDown = 70
        self.lastShotTime = 0

    def shoot(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        myBullet = bullet.MG2Bullet(self.game,
                                    self.rect.center[0], self.rect.center[1], enemyX, enemyY)
        self.game.bulletGroup.add(myBullet)


class BigMissileLauncher(Tower):
    def __init__(self, game):
        super().__init__(game)
        self.originalImage = pygame.image.load(
            os.path.join('Assets', 'Tower', 'ML2.png'))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.isPlaced = False
        self.x = 0
        self.y = 0
        self.range = 500
        self.game = game
        self.enemiesInRange = []

        self.cost = 500

        self.originalHealth = 500
        self.health = self.originalHealth

        # time to wait after shooting a bullet (in milliseconds)
        self.coolDown = 3000
        self.lastShotTime = 0

    def shoot(self):
        enemyX = self.enemiesInRange[0].rect.center[0]
        enemyY = self.enemiesInRange[0].rect.center[1]
        myBullet = bullet.ML2Bullet(self.game,
                                    self.rect.center[0], self.rect.center[1], enemyX, enemyY, self.enemiesInRange[0], self)
        self.game.bulletGroup.add(myBullet)
