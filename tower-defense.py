# Name: Mohamed Elzeni
# AndrewID: msmohame
# 15-112 Term Project

import pygame
import os
from sys import exit
import random
import enemy
import tower
import household
import button
import prohibited

# Center screen on monitor
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


class Game:
    # having constant fps makes speeds consistent across devices
    fps = 60

    # Store colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    gold = (255, 215, 0)

    # sounds
    clickSound = pygame.mixer.Sound(os.path.join('Audio', 'click.mp3'))

    # prohibited (x, y, x2, y2)
    easy = {"map": "map1.png",
            'money': 500, 'health': 200, 'steps': [('x', 130), ('y', 420),
                                                   ('x', 388), ('y', 800)],
            'enemy start pos': (840, 162), "household pos": (436, 800),
            "enemy choices": ['enemy', 'warrior', 'goblin'], 'enemy num': 100,
            'prohibited': ((0, 0, 800, 212), (0, 480, 44, 800), (83, 204, 176, 463), (176, 367, 431, 465), (338, 467, 437, 800), (530, 215, 800, 800), (46, 580, 196, 800))
            }

    normal = {"map": "map2.png",
              'money': 250, 'health': 100, 'steps': [('x', 570), ('y', 412),
                                                     ('x', 130), ('y', 705),
                                                     ('x', 380), ('y', 555),
                                                     ('x', 800)],
              'enemy start pos': (-40, 162), "household pos": (800, 590),
              "enemy choices": ['enemy', 'warrior', 'goblin'], 'enemy num': 200,
              'prohibited': ((0, 0, 145, 50), (0, 50, 77, 103), (563, 0, 800, 50),
                             (622, 50, 800, 112), (692, 112,
                                                   800, 235), (444, 763, 800, 800),
                             (512, 700, 800, 763),
                             (580, 668, 800, 700), (696, 592,
                                                    800, 668), (0, 213, 80, 800),
                             (0, 112, 620, 212), (528, 212, 615, 454), (92, 377, 615, 457), (92, 375, 172, 738), (172, 659, 425, 743), (348, 504, 425, 743), (348, 504, 800, 590))
              }

    # number of remaining enemies doesn't change anyway in hard
    hard = {"map": "map3.png",
            'money': 200, 'health': 100, 'steps': [('x', 680), ('y', 647),
                                                   ('x', 600), ('y', 765),
                                                   ('x', 220), ('y', 730),
                                                   ('x', 130), ('y', 352),
                                                   ('x', 290), ('y', 606),
                                                   ('x', 436), ('y', 386),
                                                   ('x', 753), ('y', 68),
                                                   ('x', 610), ('y', 225),
                                                   ('x', 385), ('y', 67),
                                                   ('x', 0)],
            'enemy start pos': (630, 595), "household pos": (105, 108),
            "enemy choices": ['enemy', 'warrior', 'goblin', 'skeleton', 'skeleton'], 'enemy num': 10,
            'prohibited': ((0, 0, 81, 800), (0, 0, 430, 108), (340, 108, 428, 265), (426, 182, 650, 268), (571, 0, 800, 108), (726, 108, 800, 426), (408, 344, 800, 426), (408, 344, 458, 639), (245, 565, 458, 639), (245, 312, 328, 645), (90, 318, 329, 402), (90, 318, 172, 796), (178, 724, 800, 800), (465, 500, 800, 800), (746, 432, 800, 500))
            }

    def __init__(self, level=0, isActive=False):
        # level (0 easy / 1 normal / 2 hard)
        self.levels = [self.easy, self.normal, self.hard]
        self.level = level
        self.levelDict = self.levels[self.level]

        # font
        self.gameFont = pygame.font.Font(
            os.path.join('Fonts', 'Boogaloo-Regular.ttf'), 25)
        self.mainMenuFont = pygame.font.Font(
            os.path.join('Fonts', 'Boogaloo-Regular.ttf'), 30)

        # Main screen
        self.size = self.width, self.height = 950, 800
        self.win = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Tower Defense')

        # window icon
        self.icon = pygame.image.load(os.path.join('Assets', 'Icon.png'))
        pygame.display.set_icon(self.icon)
        self.background = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', self.levelDict['map'])), (800, 800))
        self.deckbg = pygame.image.load(
            os.path.join('Assets', 'Deck', 'deckbg.png'))
        self.clock = pygame.time.Clock()
        self.inGameMessageHeight = 0
        self.timeToDisplayMessages = 2000

        # main menu buttons
        self.mainMenuButtonsGroup = pygame.sprite.Group()
        self.mainMenuButtonsGroup.add(button.LevelButton(self, 'Easy', 0))
        self.mainMenuButtonsGroup.add(button.LevelButton(self, 'Medium', 1))
        self.mainMenuButtonsGroup.add(
            button.LevelButton(self, 'Hard (infinite)', 2))
        self.mainMenuButtonsGroup.add(button.LevelButton(self, 'Quit Game', 3))

        # enemy
        self.enemiesGroup = pygame.sprite.Group()
        self.lastSpawnTime = 0
        self.spawnFrequency = 5000

        # tower
        self.towertypes = ["Cannon1", "MG1", "ML1", "Cannon2", "MG2", "ML2"]
        self.unplacedTowerGroup = pygame.sprite.GroupSingle()
        self.towerGroup = pygame.sprite.Group()

        self.bulletGroup = pygame.sprite.Group()

        self.deckButtonsGroup = pygame.sprite.Group()

        self.householdGroup = pygame.sprite.GroupSingle()

        self.healthBarGroup = pygame.sprite.Group()

        # game state
        self.gameActive = isActive
        if self.level == 2:
            self.score = 0
        else:
            self.score = -1

        # money!
        self.balance = self.levelDict["money"]
        self.currentBalance = self.balance

        # wave length
        self.waveLength = self.levelDict["enemy num"]
        self.enemiesRemaining = self.waveLength

        # win - lose state
        self.winLoseMessage = ""
        self.winLoseFont = pygame.font.Font(None, 50)

        # prohibited areas. not allowed to place defenses in them
        self.prohibitedAreaGroup = pygame.sprite.Group()
        self.addProhibitedArea()

        # a list that contains lists [surface, time, color]
        self.displayedMessages = []
        self.addDeckbuttons()

    def addEnemy(self):
        if (self.lastSpawnTime == 0) or (self.currentTime - self.lastSpawnTime > self.spawnFrequency):
            if self.enemiesRemaining > 0:
                choice = random.choice(self.levelDict['enemy choices'])
                if choice == 'enemy':
                    enemies = enemy.Enemy(
                        self, self.levelDict['enemy start pos'][0], self.levelDict['enemy start pos'][1])
                elif choice == 'warrior':
                    enemies = enemy.Warrior(
                        self, self.levelDict['enemy start pos'][0], self.levelDict['enemy start pos'][1])
                elif choice == 'goblin':
                    enemies = enemy.Goblin(
                        self, self.levelDict['enemy start pos'][0], self.levelDict['enemy start pos'][1])
                elif choice == 'skeleton':
                    enemies = enemy.Skeleton(
                        self, self.levelDict['enemy start pos'][0], self.levelDict['enemy start pos'][1])
                self.enemiesGroup.add(enemies)
                self.lastSpawnTime = pygame.time.get_ticks()
            if self.spawnFrequency - 400 >= 1000:
                self.spawnFrequency -= 400

    def addHousehold(self):
        self.householdGroup.add(household.Household(self))

    def addDeckbuttons(self):
        x = 821
        self.deckButtonsGroup.add(
            button.DeckButton(self, x, 5, self.towertypes[0]))
        self.deckButtonsGroup.add(button.DeckButton(
            self, x, 5 + 1*119, self.towertypes[1]))
        self.deckButtonsGroup.add(button.DeckButton(
            self, x, 5 + 2*119, self.towertypes[2]))
        self.deckButtonsGroup.add(button.DeckButton(
            self, x, 5 + 3*119, self.towertypes[3]))
        self.deckButtonsGroup.add(button.DeckButton(
            self, x, 5 + 4*119, self.towertypes[4]))
        self.deckButtonsGroup.add(button.DeckButton(
            self, x, 5 + 5*119, self.towertypes[5]))
        # quit button
        self.deckButtonsGroup.add(button.QuitButton(self))

    def showDeck(self):
        textColor = '#000000'
        woodCard = pygame.image.load(
            os.path.join('Assets', 'Deck', 'woodcardbg.png'))
        silverCard = pygame.image.load(
            os.path.join('Assets', 'Deck', 'silvercardbg.png'))
        goldCard = pygame.image.load(
            os.path.join('Assets', 'Deck', 'goldcardbg.png'))

        # framing
        goldFrame = pygame.image.load(
            os.path.join('Assets', 'Deck', 'goldframe.png'))
        silverFrame = pygame.image.load(
            os.path.join('Assets', 'Deck', 'silverframe.png'))
        woodFrame = pygame.image.load(
            os.path.join('Assets', 'Deck', 'woodframe.png'))

        # text boxes
        woodTextBox = pygame.image.load(
            os.path.join('Assets', 'Deck', 'woodtextbox.png'))
        silverTextBox = pygame.image.load(
            os.path.join('Assets', 'Deck', 'silvertextbox.png'))
        goldTextBox = pygame.image.load(
            os.path.join('Assets', 'Deck', 'goldtextbox.png'))

        # show card backgrounds
        y = 5
        for i in range(2):
            self.win.blit(woodCard, (821, y))
            y += 119

        for i in range(2):
            self.win.blit(silverCard, (821, y))
            y += 119

        for i in range(2):
            self.win.blit(goldCard, (821, y))
            y += 119

        # show card framing
        self.win.blit(woodFrame, (821, 5))
        self.win.blit(woodFrame, (821, 5 + 1*119))
        self.win.blit(silverFrame, (821, 5 + 2*119))
        self.win.blit(silverFrame, (821, 5 + 3*119))
        self.win.blit(goldFrame, (821, 5 + 4*119))
        self.win.blit(goldFrame, (821, 5 + 5*119))

        # show text boxes
        self.win.blit(woodTextBox, (821, 84))
        self.win.blit(woodTextBox, (821, 84 + 1*119))
        self.win.blit(silverTextBox, (821, 84 + 2*119))
        self.win.blit(silverTextBox, (821, 84 + 3*119))
        self.win.blit(goldTextBox, (821, 84 + 4*119))
        self.win.blit(goldTextBox, (821, 84 + 5*119))

        # show prices
        p1 = self.gameFont.render('$50', True, textColor)
        p1Rect = p1.get_rect(center=(self.width - 64, 85 + 34//2))
        self.win.blit(p1, p1Rect)

        p2 = self.gameFont.render('$100', True, textColor)
        p2Rect = p2.get_rect(center=(self.width - 64, 85 + 34//2 + 1*119))
        self.win.blit(p2, p2Rect)

        p3 = self.gameFont.render('$150', True, textColor)
        p3Rect = p3.get_rect(center=(self.width - 64, 85 + 34//2 + 2*119))
        self.win.blit(p3, p3Rect)

        p4 = self.gameFont.render('$200', True, textColor)
        p4Rect = p4.get_rect(center=(self.width - 64, 85 + 34//2 + 3*119))
        self.win.blit(p4, p4Rect)

        p5 = self.gameFont.render('$300', True, textColor)
        p5Rect = p5.get_rect(center=(self.width - 64, 85 + 34//2 + 4*119))
        self.win.blit(p5, p5Rect)

        p6 = self.gameFont.render('$500', True, textColor)
        p6Rect = p6.get_rect(center=(self.width - 64, 85 + 34//2 + 5*119))
        self.win.blit(p6, p6Rect)

        cannon1 = pygame.image.load(
            os.path.join('Assets', 'Tower', 'Cannon1.png'))
        cannon1Rect = cannon1.get_rect()
        cannon1Rect.center = (self.width - 64, 5 + 80//2)
        self.win.blit(cannon1, cannon1Rect)

        mg1 = pygame.image.load(
            os.path.join('Assets', 'Tower', 'MG1.png'))
        mg1Rect = mg1.get_rect()
        mg1Rect.center = (self.width - 64, 5 + 80//2 + 1*119)
        self.win.blit(mg1, mg1Rect)

        ml1 = pygame.image.load(
            os.path.join('Assets', 'Tower', 'ML1.png'))
        ml1Rect = ml1.get_rect()
        ml1Rect.center = (self.width - 64, 5 + 80//2 + 2*119)
        self.win.blit(ml1, ml1Rect)

        cannon2 = pygame.image.load(
            os.path.join('Assets', 'Tower', 'Cannon2.png'))
        cannon2Rect = cannon2.get_rect()
        cannon2Rect.center = (self.width - 64, 5 + 80//2 + 3*119)
        self.win.blit(cannon2, cannon2Rect)

        mg2 = pygame.image.load(
            os.path.join('Assets', 'Tower', 'MG2.png'))
        mg2Rect = mg2.get_rect()
        mg2Rect.center = (self.width - 64, 5 + 80//2 + 4*119)
        self.win.blit(mg2, mg2Rect)

        ml2 = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Tower', 'ML2.png')), (57, 60))
        ml2Rect = ml2.get_rect()
        ml2Rect.center = (self.width - 64, 5 + 80//2 + 5*119)
        self.win.blit(ml2, ml2Rect)

    def drawGameWindow(self):
        self.win.blit(self.background, (0, 0))

        self.enemiesGroup.draw(self.win)
        self.enemiesGroup.update()

        self.towerGroup.draw(self.win)
        self.towerGroup.update()

        self.bulletGroup.draw(self.win)
        self.bulletGroup.update()

        self.householdGroup.draw(self.win)
        self.householdGroup.update()

        self.healthBarGroup.draw(self.win)
        self.healthBarGroup.update()

        self.win.blit(self.deckbg, (800, 0))
        self.showDeck()

        self.deckButtonsGroup.draw(self.win)
        self.deckButtonsGroup.update()

        self.unplacedTowerGroup.draw(self.win)
        self.unplacedTowerGroup.update()

        self.displayInfo()
        self.showInGameMessages()

        pygame.display.update()

    def drawMainMenu(self):
        bg = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'menubg.png')), (self.width, self.height))
        self.win.blit(bg, (0, 0))
        self.mainMenuButtonsGroup.draw(self.win)
        self.mainMenuButtonsGroup.update()

        if len(self.winLoseMessage) > 0:
            if self.winLoseMessage == "You Lost!":
                winLoseSurface = self.winLoseFont.render(
                    self.winLoseMessage, True, (self.red))
                self.win.blit(winLoseSurface, (self.width / 2 -
                                               winLoseSurface.get_width() / 2, 50))
            elif self.winLoseMessage == "Victory!":
                winLoseSurface = self.winLoseFont.render(
                    self.winLoseMessage, True, (self.red))
                self.win.blit(winLoseSurface, (self.width / 2 -
                                               winLoseSurface.get_width() / 2, 50))
            if self.score != -1:
                scoreSurface = self.winLoseFont.render(
                    f"Score: {self.score}", True, (self.white))
                self.win.blit(scoreSurface, (self.width / 2 -
                                             winLoseSurface.get_width() / 2, 100))
        else:
            titleFont = pygame.font.Font(
                os.path.join('Fonts', 'Boogaloo-Regular.ttf'), 60)
            titleSurface = titleFont.render(
                "TOWER DEFENSE", True, (self.green))
            self.win.blit(titleSurface, (self.width / 2 -
                                         titleSurface.get_width() / 2, 50))
        pygame.display.update()

    # displays money and remaining enemies
    def displayInfo(self):
        bgX, bgY = 634, 675
        messagesbg = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'Deck', 'messagebg.png')), (800-bgX, 800-bgY))
        self.win.blit(messagesbg, (bgX, bgY))
        if self.level != 2:
            enemiesRemainingSurface = self.gameFont.render(
                f'Enemies Left: {self.enemiesRemaining}', True, self.white)
        else:
            enemiesRemainingSurface = self.gameFont.render(
                f'Enemies Left: ∞', True, self.white)
        self.inGameMessageHeight = enemiesRemainingSurface.get_height()
        self.win.blit(enemiesRemainingSurface, (640, self.height -
                                                enemiesRemainingSurface.get_height() - 1))

        currentBalanceSurface = self.gameFont.render(
            f'Balance: ${self.currentBalance}', True, self.white)
        self.win.blit(currentBalanceSurface, (820, self.height -
                      50 - currentBalanceSurface.get_height()))

        if self.level == 2:
            scorebgX, scorebgY = 502, 766
            scorebg = pygame.transform.scale(pygame.image.load(
                os.path.join('Assets', 'Deck', 'messagebg.png')), (634-scorebgX, 800-scorebgY))
            self.win.blit(scorebg, (scorebgX, scorebgY))
            scoreSurface = self.gameFont.render(
                f'Score: {self.score}', True, self.white)
            self.win.blit(scoreSurface, (510, self.height -
                                         1 - currentBalanceSurface.get_height()))

    # temporary messages
    def showInGameMessages(self):
        messagesToRemove = []
        for i in range(len(self.displayedMessages)):
            if self.currentTime - self.displayedMessages[i][1] > self.timeToDisplayMessages:
                messagesToRemove += [self.displayedMessages[i]]

        for i in range(len(messagesToRemove)):
            if messagesToRemove[i] in self.displayedMessages:
                self.displayedMessages.remove(messagesToRemove[i])

        for i in range(len(self.displayedMessages)):
            messageSurface = self.gameFont.render(
                self.displayedMessages[i][0], True, self.displayedMessages[i][2])

            messageNum = 2 + i
            y = self.height - 1 - messageNum*self.inGameMessageHeight
            self.win.blit(messageSurface, (640, y))

    def addMessageToList(self, message, messageColor='#FFFFFF'):
        exists = False
        for lst in self.displayedMessages:
            if lst[0] == message:
                exists = True

        if not exists:
            self.displayedMessages += [[message,
                                        self.currentTime, messageColor]]

    def addProhibitedArea(self):
        for i in range(len(self.levelDict['prohibited'])):
            x = self.levelDict['prohibited'][i][0]
            y = self.levelDict['prohibited'][i][1]
            x2 = self.levelDict['prohibited'][i][2]
            y2 = self.levelDict['prohibited'][i][3]
            self.prohibitedAreaGroup.add(
                prohibited.ProhibitedArea(x, y, x2, y2))

    def canAddTower(self, tower, tryingToPlace=False):
        if pygame.mouse.get_pos()[0] >= 800:
            return False
        for otherTower in self.towerGroup.sprites():
            if pygame.sprite.collide_rect(tower, otherTower):
                return False
        if not (self.currentBalance - tower.cost >= 0):
            if tryingToPlace:
                self.addMessageToList("No enough money!")
            return False
        for prohibitedArea in self.prohibitedAreaGroup.sprites():
            if pygame.sprite.collide_rect(tower, prohibitedArea):
                return False
        return True

    # make a tower hover with the mouse to be replaced
    def addTower(self, towertype):
        # ["Cannon1", "MG1", "ML1", "Cannon2", "MG2", "ML2"]
        if towertype == "Cannon1":
            towers = tower.Tower(self)
        elif towertype == "MG1":
            towers = tower.MachineGun(self)
        elif towertype == "ML1":
            towers = tower.MissileLauncher(self)
        elif towertype == "Cannon2":
            towers = tower.BigCannon(self)
        elif towertype == "MG2":
            towers = tower.BigMachineGun(self)
        elif towertype == "ML2":
            towers = tower.BigMissileLauncher(self)
        self.unplacedTowerGroup.add(towers)

    # place a tower permanently
    def placeTower(self):
        sprite = self.unplacedTowerGroup.sprite
        if self.canAddTower(sprite, tryingToPlace=True):
            sprite.x = pygame.mouse.get_pos()[0]
            sprite.y = pygame.mouse.get_pos()[1]
            sprite.isPlaced = True
            sprite.subtractCost()
            sprite.addHealthBar()
            self.towerGroup.add(sprite)
            self.unplacedTowerGroup.empty()
        else:
            self.addMessageToList("Can't place here!")

    def reset(self):
        self.bulletGroup.empty()
        self.enemiesGroup.empty()
        self.householdGroup.empty()
        self.towerGroup.empty()
        self.unplacedTowerGroup.empty()
        self.healthBarGroup.empty()
        self.__init__()

    def checkForWin(self):
        if len(self.enemiesGroup) < 1 and self.enemiesRemaining < 1:
            self.gameActive = False
            self.reset()
            self.winLoseMessage = "Victory!"

    def quitGame(self):
        self.running = False
        pygame.quit()
        exit()

    def runGame(self):
        self.running = True
        # main loop
        while self.running:
            self.clock.tick(self.fps)
            self.currentTime = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                if self.gameActive:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if len(self.unplacedTowerGroup) == 1:
                            self.placeTower()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                            if len(self.unplacedTowerGroup) == 1:
                                self.unplacedTowerGroup.empty()
            if self.gameActive:
                if len(self.householdGroup) < 1:
                    self.addHousehold()

                self.addEnemy()

                self.checkForWin()

                self.drawGameWindow()
            else:
                self.drawMainMenu()


def main():
    Game().runGame()


if __name__ == "__main__":
    main()
