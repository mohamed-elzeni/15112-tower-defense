# Mohamed Elzeni / msmohame
# 15-112 Term Project

import pygame
import os


class LevelButton(pygame.sprite.Sprite):
    def __init__(self, game, text, index):
        super().__init__()
        self.pressed = False
        self.game = game
        self.width = 200
        self.height = 60
        self.index = index

        if self.index == 0:
            self.images = (pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Green1.png')), (200, 60)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Green2.png')), (200, 60)))
        elif self.index == 1:
            self.images = (pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Orange1.png')), (200, 60)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Orange2.png')), (200, 60)))
        elif self.index == 2:
            self.images = (pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Red1.png')), (200, 60)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Red2.png')), (200, 60)))
        else:
            self.images = (pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Blue1.png')), (200, 60)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Buttons', 'Blue2.png')), (200, 60)))

        self.image = self.images[0]

        # position (4 buttons on screen)
        if index == 0:
            self.x = game.width / 2 - self.width / 2
            self.y = game.height / 2 - 2*self.height
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        elif index == 1:
            self.x = game.width / 2 - self.width / 2
            self.y = game.height / 2 - self.height / 2
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        elif index == 2:
            self.x = game.width / 2 - self.width / 2
            self.y = game.height / 2 + self.height
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        elif index == 3:
            self.x = game.width / 2 - self.width / 2
            self.y = game.height / 2 + 2.5*self.height
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # text
        self.textColor = '#FF0000'
        self.textSurface = self.game.gameFont.render(
            text, True, self.textColor)
        self.textRect = self.textSurface.get_rect(
            center=(self.rect.center[0], self.rect.center[1]-5))

    def update(self):
        self.checkForClick()
        self.rect.topleft = (self.x, self.y)
        self.game.win.blit(self.textSurface, self.textRect)

    def checkForClick(self):
        mousePosition = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.image = self.images[1]
                self.rect = self.image.get_rect(topleft=(self.x, self.y))
                self.pressed = True
            else:
                if self.pressed == True:

                    if self.index == 0:
                        self.game.gameActive = True
                        self.game.__init__(level=0, isActive=True)
                    elif self.index == 1:
                        self.game.gameActive = True
                        self.game.__init__(level=1, isActive=True)
                    elif self.index == 2:
                        self.game.gameActive = True
                        self.game.__init__(level=2, isActive=True)
                    elif self.index == 3:
                        self.game.quitGame()
                    self.pressed = False
                    self.game.clickSound.play()
        else:
            self.image = self.images[0]


class DeckButton(pygame.sprite.Sprite):
    def __init__(self, game, x, y, towertype):
        super().__init__()
        self.pressed = False
        self.game = game
        self.width = 128
        self.height = 80

        # ["Cannon1", "MG1", "ML1", "Cannon2", "MG2", "ML2"]
        self.tower = towertype

        self.x = x
        self.y = y

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def checkForClick(self):
        mousePosition = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    # button action
                    if len(self.game.unplacedTowerGroup) == 1:
                        self.game.unplacedTowerGroup.empty()
                    else:
                        self.game.addTower(self.tower)
                    self.pressed = False

    def update(self):
        self.checkForClick()
        self.rect.topleft = (self.x, self.y)


class QuitButton(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.pressed = False
        self.game = game
        self.images = (pygame.image.load(os.path.join('Assets', 'Buttons', 'Quit1.png')),
                       pygame.image.load(os.path.join('Assets', 'Buttons', 'Quit2.png')))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.game.width - 110
        self.rect.y = self.game.height - 50

    def checkForClick(self):
        mousePosition = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed()[0]:
                self.image = self.images[1]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.pressed = True
            else:
                if self.pressed:
                    # action
                    score = self.game.score
                    self.game.reset()
                    self.game.score = score
                    self.game.winLoseMessage = "You Lost!"
                    self.pressed = False
                    self.game.clickSound.play()
        else:
            self.image = self.images[0]

    def update(self):
        self.checkForClick()
        self.rect.center = self.rect.center
