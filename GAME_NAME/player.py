import pygame as pg
import GAME_NAME.entity as ent

class Player( ent.Entity ):
    
    heart_image = ent.pg.image.load('assets/coracao.png').convert_alpha()
    heart_image = pg.transform.smoothscale_by(heart_image, [.5,.5])

    pontuation = 0

    class playerAlredyExits(AssertionError):
        def __init__(self) -> None:
            pass

    def __init__(self, str: str, layer: int, pos: pg.math.Vector2, display: pg.surface.Surface) -> None:
        super().__init__(str, layer, pos)

        if ent.Entity.player != 0:
            raise Player.playerAlredyExits

        self.display = display
        windowSize = self.display.get_size()
        imageSize = self.animator.image.get_size()

        self.txt_pos = pg.math.Vector2( (windowSize[0] - imageSize[0]) *0.5, windowSize[1] - imageSize[1] )
        self.icon_pos = pg.math.Vector2( (windowSize[0] - imageSize[0]) *0.5, self.txt_pos[1]-imageSize[1])

        self.animator = ent.an.Animator(pg.image.load('assets/bonecodeneve.png').convert_alpha(), [32,32], [3,3,3,3])

        ent.Entity.player = self
        
        self.max_lifes = 3
        self.lifes = self.max_lifes

        self.pontuation_to_regen = 100

    def __str__(self) -> str:
        return 'Player'

    def move(self, dt: float) -> None:
        '''Player move caracteristic: Icon pos doesn't change. The text digited is centered.'''

        windowSize = self.display.get_size()
        imageSize = self.text_image.get_size()

        self.txt_pos = pg.math.Vector2( (windowSize[0] - imageSize[0]) *0.5, windowSize[1] - imageSize[1] )

    def checkKeyboard(self, events: list) -> None:
        ''' Checks for keyboard inputs.'''
        
        for ev in events:
            if ev.type == ent.pg.KEYDOWN:
                if ev.key >= 97 and ev.key <= 122 or ev.key >= 65 and ev.key <= 90:
                    self.addCharacters(str(chr(ev.key)))

                elif ev.key == pg.K_BACKSPACE:
                    self.backspace()

                elif ev.key == pg.K_SPACE:
                    self.addCharacters(' ')

                elif ev.key == pg.K_TAB:
                    self.clear()

                elif ev.key == pg.K_RETURN:
                    self.damageEnemy(self.string)
                    self.clear()

    def damageEnemy(self, str: str) -> None:
        '''Kills the first enemy that match the str parameter.'''

        for index in range(len(ent.Entity.enemies)):
            if ent.Entity.enemies[index].string == str:

                # granting the pont, before killing the entity (killing it can result on it being deleted.)
                pont = len(str)
                
                ent.Entity.enemies[index].damageSelf()

                self.pontuation += pont

                return

    def damageSelf(self) -> None:
        
        if self.is_taking_damage:
            return

        if self.lifes == 1:
            self.kill()
            return

        super().damageSelf()
        ent.Timer(0.25, lambda: self.turnDamageBoolOff(), True)

        self.clear()
        self.lifes -= 1

    def collideMethod(self, collideEnt: ent.Entity):
        '''Damages the player.\n'''
        
        super().collideMethod(collideEnt)
        self.damageSelf()

    def blit(self, blitter: ent.blt.Blitter, angle: float) -> None:
        super().blit(blitter, angle)

        for life in range(self.lifes):
            blitter.addImageInLayer(self.layer, self.heart_image, (life*self.heart_image.get_rect().width, blitter.displaySize()[1] - self.heart_image.get_rect().height))

        pontText = ent.fonts[2].render(str(self.pontuation), 1, self.color)
        blitter.addImageInLayer( self.layer, pontText, (self.max_lifes*self.heart_image.get_rect().width, blitter.displaySize()[1] - self.heart_image.get_rect().height - pontText.get_rect().height) )

    def regenLife(self) -> None:
        if self.pontuation >= self.pontuation_to_regen:
            self.pontuation_to_regen += 100
            
            self.lifes += 1

    def update(self, blitter: ent.blt.Blitter, events: list, dt: float) -> None:
        self.checkKeyboard(events)
        self.regenLife()

        return super().update(blitter, dt)