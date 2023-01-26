import pygame as pg
import blitter as blt
import animator as an
import requests
from random import randint
from timer import *

pg.font.init()

words_api = requests.get('https://random-word-api.herokuapp.com/word?number=2000')
words_list = list(words_api.json())
words_list.sort(key=len)

def getRandomWord() -> str:
    return words_list[randint(0, len(words_list)-1)]

def getSmallWord() -> str:
    return words_list[randint(0, int(0.2*len(words_list)))]

def getBigWord() -> str:
    return words_list[randint(int(0.8*len(words_list)), len(words_list)-1)]

fonts = [pg.font.Font('assets/gamefont.ttf', 24),
         pg.font.Font('assets/gamefont.ttf', 20),
         pg.font.Font('assets/gamefont.ttf', 16),
         pg.font.Font('assets/gamefont.ttf', 12)]

class Entity():
    player : 'Entity' = 0
    enemies : list['Entity'] = []

    # unique id for each entity.
    id = 1

# class procedures.
    def updEntities(blitter: blt.Blitter, events: list[pg.event.Event], dt: float) -> None:
        '''Updates all the registered entites.\n
           And updates the timers.\n'''

        Entity.player.update(blitter, events, dt)
        for enemy in Entity.enemies:
            enemy.update(blitter, dt)

        Timer.updAllTimers()

    def checkLists() -> None:
        '''Checks the global lists. Removes entities if they are dead.\n
           Detects colission between entities in the game.\n
           Calls the collide procedure if finds collision.\n'''

        for en1 in Entity.enemies:

            if en1.is_dead: 
                Entity.enemies.remove(en1)
                continue

            if Entity.player.is_dead: return

            # enemy <-> player colision.
            if Entity.collide(Entity.player, en1):
                en1.collideMethod(Entity.player)
                Entity.player.collideMethod(en1)

            for en2 in Entity.enemies:    
                
                # enemy is dead.
                if en1.is_dead:
                    Entity.enemies.remove(en1)
                    break
                if en2.is_dead:
                    Entity.enemies.remove(en2)
                    continue
                
                # same entity.
                if en1.id == en2.id:
                    continue
                
                # enemy <-> enemy colision.
                if Entity.collide(en1, en2):
                    en1.collideMethod(en2)                              

    def collide(ent1: 'Entity', ent2: 'Entity', maskCollision : bool = False) -> bool:
        '''Return true if self entities collide.\n
           If needed to check mask collision, just set the maskCollision parameter to true.\n'''

        if maskCollision:
            if ent1.mask.overlap_mask(ent2.mask, ent1.icon_pos - ent2.icon_pos):
                return True
            return False
        
        if ent1.rect.colliderect(ent2.rect):
            return True
        return False

    class notStringEntity(ValueError):
        def __init__(self, obj) -> None:
            self.found_type = type(obj)
            
        def __str__(self) -> str:
            return '''Entity has been set with a parameter that isn't a string.'''

# instance's procedures.
    def __init__(self, str: str, layer: int, icon_pos: pg.math.Vector2) -> None:
        if type(str) != type(''):
            raise Entity.notStringEntity()

        self.id = Entity.id
        Entity.id += 1

        self.is_dead = False
        self.is_taking_damage = False

        # 1 or -1.
        self.speed_dir = 1

        self.font_index = 0

        self.string = str
        self.color = pg.color.Color('black')
        self.text_image = fonts[self.font_index].render(str, 1, self.color)

        self.layer = layer

        self.icon_pos = icon_pos
        self.txt_pos = pg.math.Vector2()

        self.speed = pg.math.Vector2()
        self.speed_value = 0

        self.angle = 0

        self.animator = an.Animator(pg.image.load('assets/empty.png').convert_alpha(), [30,30], [1])

        # colission variables.
        self.rect = self.animator.image.get_rect()
        self.mask = pg.mask.from_surface(self.animator.image)

    def __eq__(self, __o: object) -> bool:
        if type(__o) == type(self) and self.id == __o.id:
            return True

        return False
    
    def changeFont(self, index: int) -> None:
        if type(index) != type(1):
            raise ValueError
        
        elif index < 0 or not index < len(fonts):
            raise ValueError

        self.font_index = index

    def getIconCenter(self) -> pg.math.Vector2():
        return self.icon_pos + (pg.math.Vector2(self.animator.image.get_size()) * 0.5)

    def clear(self) -> None:
        # clear instance's string.
        self.string = ''

    def changeColor(self, color: pg.color.Color) -> None:
        # changes the instance color.

        self.color = color

    def addCharacters(self, str: str) -> None:
        # adds chars to instance's string.

        if type(str) != type(''):
            raise Entity.notStringEntity(str)

        self.string += str

    def backspace(self) -> None:
        '''Simulates backspace key to the player's word.\n'''
        self.string = self.string[:-1]

    def updateTxtImage(self) -> None:
        # updates the current image to represent the current word.

        self.text_image = fonts[self.font_index].render(self.string, 1, self.color)

    def move(self, dt: float) -> None:
        '''Moves the icon based in self.speed.\n
           Moves the text to be bellow the icon, centered.\n'''

        self.icon_pos = self.icon_pos + self.speed * dt * self.speed_value * self.speed_dir

        iconImageSize = self.animator.image.get_size()
        txtImageSize = self.text_image.get_size()

        self.txt_pos = self.icon_pos + pg.math.Vector2( (iconImageSize[0]-txtImageSize[0])/2, 10 + iconImageSize[1] )

    def blit(self, blitter: blt.Blitter, angle: float) -> None:
        '''Rotates image by given angle and blits it in the instance's pos.\n
           If the entity has been damaged, blits a white cover in front of the entity's icon.\n'''

        # adding text to the display.
        txt = blt.rotCenter(self.text_image, angle)
        blitter.addImageInLayer(blitter.lastLayer(), txt, self.txt_pos)

        # adding icon to the display.
        if not self.is_taking_damage:
            icon = blt.rotCenter(self.animator.image, angle)
            blitter.addImageInLayer(self.layer, icon, self.icon_pos)
        
        else:
            whiteCover = self.mask.to_surface()
            whiteCover.set_colorkey((0,0,0))
            whiteCover = blt.rotCenter(whiteCover, angle)

            blitter.addImageInLayer(self.layer, whiteCover, self.icon_pos)

    def collideMethod(self, collideEnt: 'Entity'):
        '''Abstract function for when entities collide.\n'''

    def damageSelf(self) -> None:
        '''Abstract function to damages the entity.\n
           This version just sets the damage bool variable to true.\n'''

        self.is_taking_damage = True
    
    def turnDamageBoolOff(self) -> None:
        self.is_taking_damage = False

    def kill(self) -> None:
        self.is_dead = True

    def goingOutOfBounds(self) -> bool:
        '''Return's true if the instance's rect is not completely inside the display.\n'''

        displayRect = pg.display.get_surface().get_rect()

        if not displayRect.contains(self.rect):
            return True
        return False

    def update(self, blitter: blt.Blitter, dt: float) -> None:
        # does all the loop procedures of an entity.
        self.move(dt)

        self.animator.update(dt)
        self.rect = self.animator.image.get_rect().move(self.icon_pos)
        self.mask = pg.mask.from_surface(self.animator.image)

        self.updateTxtImage()
        self.blit( blitter, self.angle )