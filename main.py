import pygame as pg
from random import random
from math import sqrt

# pg setup
pg.init()
SCRN = pg.Vector2(432, 768)
screen = pg.display.set_mode(SCRN)
clock = pg.time.Clock()
running = True

# variables
pfColor = (20, 170, 40)
pfColor2 = (50, 70, 230)
gameHeight = 0
GRAV = pg.Vector2(0, .25)
moving = 0
platforms = []
platformSpawn = -30
platformHeightDiff = 100
platformHeightDiffRand = 150
gameoverAlpha = 0
gameoverAlphaDelta = 0.05
gameover = False
highscore = 0

# gameover sprite
gameoverSprite = pg.image.load('gameover.png')
gameoverSprite = pg.transform.scale(gameoverSprite, SCRN)
gameoverSpriteRect = gameoverSprite.get_rect(center=SCRN/2)

class Player:
    pos = pg.Vector2(SCRN.x/2, 200)
    velo = pg.Vector2(0, 0)
    jump = pg.Vector2(0, -14)
    spd = 1.5
    sprite = pg.image.load('doodle.png').convert_alpha()
    sprite = pg.transform.scale(sprite, (100, 100))

# fonts
FONT = pg.font.Font('Nice Paper.ttf', 40)
FONT_HIGHSCORE = pg.font.Font('Nice Paper.ttf', 20)


class Platform:
    def __init__(self, width: float, height: float, color: tuple, pos):
        self.width = width
        self.height = height
        self.color = color
        self.pos = pos 
    
    def draw(self):
        drawPos = self.pos + pg.Vector2(0, gameHeight)
        p_rect = pg.Rect(drawPos.x - self.width/2, drawPos.y - self.height/2, self.width, self.height)
        pg.draw.rect(screen, self.color, p_rect, border_radius=5)
    
    def update(self):
        pass

def drawGui():
    # score
    borderWidth = 6
    scoreW, scoreH = 120, 50
    scorePos = pg.Vector2(SCRN.x/2, 50)
    textOffset = pg.Vector2(0, 4)
    scoreBoxRect = pg.Rect(scorePos.x - scoreW/2, scorePos.y - scoreH/2, scoreW, scoreH)
    scoreBorderRect = pg.Rect(scorePos.x - scoreW/2 - borderWidth, scorePos.y - scoreH/2 - borderWidth, scoreW + borderWidth*2, scoreH + borderWidth*2)
    pg.draw.rect(screen, (0, 0, 0), scoreBorderRect, border_radius=borderWidth)
    pg.draw.rect(screen, (255, 255, 255), scoreBoxRect, border_radius=borderWidth)
    scoreText = FONT.render(str(int(gameHeight/100)).zfill(4) + "m", True, (0, 0, 0))
    scoreTextRect = scoreText.get_rect(center= scorePos + textOffset)
    screen.blit(scoreText, scoreTextRect)

def playerUpdate():
    Player.velo += GRAV
    Player.pos += Player.velo
    
    # friction
    fric = 0.85
    Player.velo.x *= fric

def playerDraw():
    if Player.velo.x < 0:
        sprite = pg.transform.flip(Player.sprite, True, False)
    else:
        sprite = Player.sprite
    rect = sprite.get_rect(center=(Player.pos.x, Player.pos.y-50 + gameHeight))
    screen.blit(sprite, rect)

def playerJump(j):
    if Player.velo.y < 0:
        Player.velo += j
    else:
        Player.velo = j.copy()

def playerWrap():
    if Player.pos.x < -10:
        Player.pos.x = SCRN.x+10
    elif Player.pos.x > SCRN.x+10:
        Player.pos.x = -10

def dist(v1, v2):
    xDiff = v1.x - v2.x
    yDiff = v1.y - v2.y
    return sqrt(xDiff**2 + yDiff**2)


def playerCheckCol():
    if Player.velo.y >= 0:
        for p in platforms:
            if dist(p.pos, Player.pos) < 75 and p.pos.y < Player.pos.y + Player.velo.y and p.pos.y > Player.pos.y - 10:
                return p
    return False

def drawGameoverScreen():
    gameoverSprite.set_alpha(gameoverAlpha*255)
    screen.blit(gameoverSprite, gameoverSpriteRect)

def drawHighscore():
    pg.draw.line(screen, (0, 0, 0), (0, -highscore+300 + gameHeight), (SCRN.x, -highscore+300 + gameHeight))
    hsText = FONT_HIGHSCORE.render(str(int(highscore/100)).zfill(4) + "m", True, (0, 0, 0))
    hsTextRect = hsText.get_rect(center=(SCRN.x-40, -highscore+290 + gameHeight))
    screen.blit(hsText, hsTextRect)

def updateHighscore():
    global highscore
    if gameHeight > highscore:
        highscore = gameHeight


platforms.append(Platform(100, 22, pfColor, pg.Vector2(Player.pos.x, Player.pos.y + 100)))


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                moving -= 1
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                moving += 1
        if event.type == pg.KEYUP:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                moving += 1
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                moving -= 1
    
    Player.velo.x += Player.spd * moving

    screen.fill((130, 236, 255))

    if Player.velo.y < 0:
        platformSpeedMult = -Player.velo.y * -((Player.pos.y - SCRN.y)/SCRN.y)
    else:
        platformSpeedMult = 0
    
    gameHeight += (SCRN.y/2 - (Player.pos.y+gameHeight)) * .1
    if gameHeight <= 0:
        gameHeight = 0

    if Player.velo.y > 120 * GRAV.y:
        if gameoverAlpha < 1:
            gameoverAlpha += gameoverAlphaDelta
        else:
            for p in platforms:
                del p
            platforms = []
            platformSpawn = -30
            Player.pos = pg.Vector2(SCRN.x/2, 200)
            gameover = True
            gameoverAlpha = 1
    

    if gameover == True:
        if gameoverAlpha > 0:
            gameoverAlpha -= gameoverAlphaDelta
            Player.velo = pg.Vector2(0, 0)
        else:
            platforms.append(Platform(100, 22, pfColor, pg.Vector2(Player.pos.x, Player.pos.y + 100)))
            gameover = False


    for i, p in enumerate(platforms):
        if p.pos.y < Player.pos.y + SCRN.y:
            p.update()
            p.draw()
        else:
            platforms.pop(i)
            del p


    col = playerCheckCol()
    if col:
        if col.color == pfColor:
            playerJump(Player.jump)
        else:
            playerJump(Player.jump*1.6)

    updateHighscore()
    drawHighscore()

    playerUpdate()
    playerDraw()
    playerWrap()


    if Player.pos.y - SCRN.y < platformSpawn:
        if random() < 0.1:
            col = pfColor2
        else:
            col = pfColor
        platforms.append(Platform(100, 22, col, pg.Vector2((SCRN.x-100) * random() + 50, platformSpawn)))
        platformSpawn -= platformHeightDiff + platformHeightDiffRand * random()

    drawGui()
    drawGameoverScreen()

    pg.display.flip()

    clock.tick(60)

pg.quit()