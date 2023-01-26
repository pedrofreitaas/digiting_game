import blitter as blt
import pygame as pg

backgrounds_strs = ['assets/map/mountain1.png',
                    'assets/map/mountain2.png',
                    'assets/map/mountain3.png',
                    'assets/map/mountain4.png',
                    'assets/map/mountain5.png']

class Map():
    def __init__(self, displaySize: pg.math.Vector2()) -> None:
        
        self.current_image = 1

        self.image = pg.image.load(backgrounds_strs[self.current_image]).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, displaySize)

        self.pos = pg.math.Vector2()
    
    def changeImage(self) -> None:
        '''Changes the background image.'''

        self.current_image += 1
        if self.current_image >= len(backgrounds_strs):
            self.current_image = 0

        oldSize = self.image.get_rect().size

        self.image = pg.image.load(backgrounds_strs[self.current_image]).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, oldSize)

    def blit(self, blitter: blt.Blitter) -> None:
        
        blitter.addImageInLayer(0, self.image, self.pos)

    def update(self, blitter: blt.Blitter):
        
        self.blit(blitter)