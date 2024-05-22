# Mohamed Elzeni / msmohame
# 15-112 Term Project

import pygame
import os
import healthBar


class Enemy(pygame.sprite.Sprite):
    # ghost

    def __init__(self, game, x, y):
        super().__init__()
        # frames
        self.upFrames = []
        self.downFrames = []
        self.rightFrames = []
        self.leftFrames = []

        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '1GhostU.png')), (40, 40)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '2GhostU.png')), (40, 40)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '3GhostU.png')), (40, 40)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '4GhostU.png')), (40, 40)))

        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '1GhostD.png')), (40, 40)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '2GhostD.png')), (40, 40)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '3GhostD.png')), (40, 40)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '4GhostD.png')), (40, 40)))

        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '1GhostR.png')), (40, 40)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '2GhostR.png')), (40, 40)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '3GhostR.png')), (40, 40)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '4GhostR.png')), (40, 40)))

        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '1GhostL.png')), (40, 40)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '2GhostL.png')), (40, 40)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '3GhostL.png')), (40, 40)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Ghost', '4GhostL.png')), (40, 40)))

        self.currentFrameUp = 0
        self.currentFrameDown = 0
        self.currentFrameRight = 0
        self.currentFrameLeft = 0
        self.image = self.downFrames[self.currentFrameDown]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.originalHealth = 100
        self.health = self.originalHealth
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.game = game
        self.steps = self.game.levelDict['steps']

        # 0 left or right, 1 up, -1 down
        self.facingDirection = 0

        # index in the list of steps
        self.stepIndex = 0
        self.damage = 20

        # gained amount of money when dead
        self.returnValue = 25

        self.addHealthBar()
        if self.game.level != 2:
            self.game.enemiesRemaining -= 1

    def animateUp(self):
        self.currentFrameUp += 0.2
        if int(self.currentFrameUp) >= len(self.upFrames):
            self.currentFrameUp = 0
        self.image = self.upFrames[int(self.currentFrameUp)]
        self.facingDirection = 1

    def animateDown(self):
        self.currentFrameDown += 0.2
        if int(self.currentFrameDown) >= len(self.downFrames):
            self.currentFrameDown = 0
        self.image = self.downFrames[int(self.currentFrameDown)]
        self.facingDirection = -1

    def animateRight(self):
        self.currentFrameRight += 0.2
        if int(self.currentFrameRight) >= len(self.rightFrames):
            self.currentFrameRight = 0
        self.image = self.rightFrames[int(self.currentFrameRight)]
        self.facingDirection = 0

    def animateLeft(self):
        self.currentFrameLeft += 0.2
        if int(self.currentFrameLeft) >= len(self.leftFrames):
            self.currentFrameLeft = 0
        self.image = self.leftFrames[int(self.currentFrameLeft)]
        self.facingDirection = 0

    def update(self):
        if self.health > 0:
            self.collideWithHousehold()
            if self.stepIndex < len(self.steps):
                step = self.steps[self.stepIndex]
                if step[0] == 'x':
                    dx = (
                        step[1] - self.rect.centerx) // abs(step[1] - self.rect.centerx)
                    self.rect.centerx += dx
                    if dx < 0:
                        self.animateLeft()
                    elif dx > 0:
                        self.animateRight()
                    if self.rect.centerx == step[1]:
                        self.stepIndex += 1
                elif step[0] == 'y':
                    dy = (
                        step[1] - self.rect.centery) // abs(step[1] - self.rect.centery)
                    self.rect.centery += dy

                    if dy < 0:
                        self.animateUp()
                    elif dy > 0:
                        self.animateDown()

                    if self.rect.centery == step[1]:
                        self.stepIndex += 1
            else:
                self.killAndAddMoney()
        else:
            self.killAndAddMoney()

    def collideWithHousehold(self):
        if pygame.sprite.collide_rect(self, self.game.householdGroup.sprite):
            self.game.householdGroup.sprite.health -= self.damage
            self.killAndAddMoney()

    def addHealthBar(self):
        self.game.healthBarGroup.add(healthBar.HealthBar(self.game, self))

    def killAndAddMoney(self):
        self.kill()
        if self.game.currentBalance + self.returnValue <= self.game.balance:
            self.game.currentBalance += self.returnValue
            self.game.addMessageToList(
                f"              +${self.returnValue}")

        if self.game.level == 2:
            self.game.score += 1


class Warrior(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.upFrames = []
        self.downFrames = []
        self.rightFrames = []
        self.leftFrames = []

        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '1WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '2WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '3WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '4WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '5WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '6WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '7WarriorU.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '8WarriorU.png')), (50, 50)))

        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '1WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '2WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '3WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '4WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '5WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '6WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '7WarriorD.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '8WarriorD.png')), (50, 50)))

        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '1WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '2WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '3WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '4WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '5WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '6WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '7WarriorR.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '8WarriorR.png')), (50, 50)))

        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '1WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '2WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '3WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '4WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '5WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '6WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '7WarriorL.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Warrior', '8WarriorL.png')), (50, 50)))

        self.currentFrameUp = 0
        self.currentFrameDown = 0
        self.currentFrameRight = 0
        self.currentFrameLeft = 0
        self.image = self.downFrames[self.currentFrameDown]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.originalHealth = 400
        self.health = self.originalHealth
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.game = game
        self.steps = self.game.levelDict['steps']

        # index in the list of steps
        self.stepIndex = 0
        self.damage = 20

        # gained amount of money when dead
        self.returnValue = 50
        self.addHealthBar()


class Goblin(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.upFrames = []
        self.downFrames = []
        self.rightFrames = []
        self.leftFrames = []

        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinU1.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinU2.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinU3.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinU4.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinU5.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinU6.png')), (50, 50)))

        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinD1.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinD2.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinD3.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinD4.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinD5.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinD6.png')), (50, 50)))

        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinR1.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinR2.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinR3.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinR4.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinR5.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinR6.png')), (50, 50)))

        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinL1.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinL2.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinL3.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinL4.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinL5.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Goblin', 'GoblinL6.png')), (50, 50)))

        self.currentFrameUp = 0
        self.currentFrameDown = 0
        self.currentFrameRight = 0
        self.currentFrameLeft = 0
        self.image = self.downFrames[self.currentFrameDown]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.originalHealth = 500
        self.health = self.originalHealth
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.game = game
        self.steps = self.game.levelDict['steps']

        # index in the list of steps
        self.stepIndex = 0
        self.damage = 20

        # gained amount of money when dead
        self.returnValue = 100
        self.addHealthBar()


class Skeleton(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.upFrames = []
        self.downFrames = []
        self.rightFrames = []
        self.leftFrames = []
        self.upAttackFrames = []
        self.downAttackFrames = []

        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU1.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU2.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU3.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU4.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU5.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU6.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU7.png')), (50, 50)))
        self.upAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAU8.png')), (50, 50)))

        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD1.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD2.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD3.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD4.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD5.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD6.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD7.png')), (50, 50)))
        self.downAttackFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonAD8.png')), (50, 50)))

        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonU1.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonU2.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonU3.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonU4.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonU5.png')), (50, 50)))
        self.upFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonU6.png')), (50, 50)))

        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonD1.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonD2.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonD3.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonD4.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonD5.png')), (50, 50)))
        self.downFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonD6.png')), (50, 50)))

        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonR1.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonR2.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonR3.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonR4.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonR5.png')), (50, 50)))
        self.rightFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonR6.png')), (50, 50)))

        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonL1.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonL2.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonL3.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonL4.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonL5.png')), (50, 50)))
        self.leftFrames.append(pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Skeleton', 'SkeletonL6.png')), (50, 50)))

        self.currentFrameUp = 0
        self.currentFrameDown = 0
        self.currentFrameRight = 0
        self.currentFrameLeft = 0
        self.currentUpAttackFrame = 0
        self.currentdownAttackFrame = 0
        self.image = self.downFrames[self.currentFrameDown]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.originalHealth = 400
        self.health = self.originalHealth
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.game = game
        self.steps = self.game.levelDict['steps']

        # 0 left or right, 1 up, -1 down
        self.facingDirection = 0

        # tower detection
        self.range = 400
        self.towersInRange = []
        self.engaged = False
        self.isAnimatingAttack = False
        self.attackStartTime = 0
        self.attackDamage = 100
        self.coolDown = 2000
        self.tower = None

        # index in the list of steps
        self.stepIndex = 0
        self.damage = 20

        # gained amount of money when dead
        self.returnValue = 10
        self.addHealthBar()

    def getDistance(self, x1, y1, x2, y2):
        return ((x2-x1)**2 + (y2-y1)**2)**(1/2)

    def inRange(self, tower):
        towerBorderPoints = [(tower.rect.topleft[0],
                              tower.rect.topleft[1]),
                             (tower.rect.topright[0],
                             tower.rect.topright[1]),
                             (tower.rect.bottomleft[0],
                              tower.rect.bottomleft[1]),
                             (tower.rect.bottomright[0],
                             tower.rect.bottomright[1])]
        myCenter = self.rect.center
        for point in towerBorderPoints:
            if self.getDistance(point[0], point[1], myCenter[0], myCenter[1]) <= self.range:
                return True

    def detectTowersInRange(self):
        self.towersInRange.clear()
        for tower in self.game.towerGroup.sprites():
            if self.inRange(tower):
                if tower not in self.towersInRange:
                    self.towersInRange += [tower]
            elif tower in self.towersInRange:
                self.towersInRange.remove(tower)
        if len(self.towersInRange) > 0:
            min = 10000
            minTower = 0
            for tower in self.towersInRange:
                towerBorderPoints = [(tower.rect.topleft[0],
                                      tower.rect.topleft[1]),
                                     (tower.rect.topright[0],
                                      tower.rect.topright[1]),
                                     (tower.rect.bottomleft[0],
                                      tower.rect.bottomleft[1]),
                                     (tower.rect.bottomright[0],
                                      tower.rect.bottomright[1])]
                myCenter = self.rect.center
                for point in towerBorderPoints:
                    if self.getDistance(point[0], point[1], myCenter[0], myCenter[1]) <= min:
                        minTower = tower
            self.towersInRange[0] = minTower

    def toggleEngageState(self):
        if len(self.towersInRange) >= 1:
            if self.towersInRange[0].rect.center[0] == self.rect.center[0]:
                self.tower = self.towersInRange[0]
                self.engaged = True
        else:
            self.engaged = False

    def update(self):
        if self.health > 0:
            self.collideWithHousehold()
            self.detectTowersInRange()
            self.toggleEngageState()
            if self.engaged:
                self.engageWithTower()
            else:
                self.moveInPath()
        else:
            self.killAndAddMoney()

    def engageWithTower(self):
        direction = self.tower.rect.center[1]
        dy = 0
        if pygame.sprite.collide_rect(self, self.tower):
            dy = 0
        else:
            if direction != self.rect.centery:
                dy = (direction - self.rect.centery) // abs(direction -
                                                            self.rect.centery)
        self.rect.centery += dy
        if dy < 0:
            self.animateUp()
        elif dy > 0:
            self.animateDown()

        # we reached the tower
        if dy == 0:
            if len(self.towersInRange) > 0 and (self.game.currentTime - self.attackStartTime > self.coolDown):
                self.isAnimatingAttack = True
                self.attackStartTime = self.game.currentTime
        if (len(self.towersInRange) > 0) and (direction != self.rect.centery):
            dy = (direction - self.rect.centery) // abs(direction - self.rect.centery)
        if self.facingDirection == 1 or dy < 0:
            self.animateAttackUp()
            if self.tower.health < 0:
                self.tower = None
                self.engaged = False
        elif self.facingDirection == -1 or dy > 0:
            self.animateAttackDown()
            if self.tower.health < 0:
                self.tower = None
                self.engaged = False

    def animateAttackUp(self):
        if self.isAnimatingAttack:
            self.currentUpAttackFrame += 0.2
            if int(self.currentUpAttackFrame) >= len(self.upAttackFrames):
                self.currentUpAttackFrame = 0
                self.isAnimatingAttack = False
                self.tower.health -= self.attackDamage
            self.image = self.upAttackFrames[int(self.currentUpAttackFrame)]

    def animateAttackDown(self):
        if self.isAnimatingAttack:
            self.currentdownAttackFrame += 0.2
            if int(self.currentdownAttackFrame) >= len(self.downAttackFrames):
                self.currentdownAttackFrame = 0
                self.isAnimatingAttack = False
                self.tower.health -= self.attackDamage
            self.image = self.downAttackFrames[int(
                self.currentdownAttackFrame)]

    def moveInPath(self):
        if self.stepIndex < len(self.steps):
            step = self.steps[self.stepIndex]
            if step[0] == 'x':
                dx = (
                    step[1] - self.rect.centerx) // abs(step[1] - self.rect.centerx)
                self.rect.centerx += dx
                if dx < 0:
                    self.animateLeft()
                elif dx > 0:
                    self.animateRight()
                if self.rect.centerx == step[1]:
                    self.stepIndex += 1
            elif step[0] == 'y':
                dy = (
                    step[1] - self.rect.centery) // abs(step[1] - self.rect.centery)
                self.rect.centery += dy

                if dy < 0:
                    self.animateUp()
                elif dy > 0:
                    self.animateDown()

                if self.rect.centery == step[1]:
                    self.stepIndex += 1
        else:
            self.killAndAddMoney()
