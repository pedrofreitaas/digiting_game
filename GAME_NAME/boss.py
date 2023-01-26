import GAME_NAME.enemy as en
from time import time as tm

boss_png = en.ent.pg.image.load('assets/bosses.png')
possibleSprites = [ boss_png.subsurface((0,0),(288,96)),
                    boss_png.subsurface((0,96),(288,96)),
                    boss_png.subsurface((0,192),(288,96)),
                    boss_png.subsurface((0,288),(288,96)) ]

class Boss(en.Enemy):
    def __init__(self, str: str, layer: int, pos: en.ent.pg.math.Vector2) -> None:
        super().__init__(str, layer, pos, canFusion=False)
        
        self.lifes = 3

        self.animator = en.ent.an.Animator(possibleSprites[en.randint(0, len(possibleSprites)-1)].convert_alpha(), [96,96], [3])

        self.speed_value = en.randint(10,40)

    def __str__(self) -> str:
        return 'Boss'

    def damageSelf(self) -> None:
        '''A boss can take three hits. Every time they get hitted, the word changes\n
           and they go back a little bit.\n'''

        super(en.Enemy, self).damageSelf()
        en.ent.Timer(1, lambda: self.turnDamageBoolOff(), True)

        self.goBackward()
        en.ent.Timer(1, lambda: self.goFoward(), True)

        # don't changes word in last life.
        if self.lifes == 1:
            super(en.Enemy, self).damageSelf()
            en.ent.Timer(1, lambda: self.kill(), True)
            return

        self.clear()
        self.string = en.ent.getBigWord()
        self.lifes -= 1        

    def collideMethod(self, collideEnt: en.ent.Entity) -> None:
        '''On collision bosses suffer no effect.\n'''      
        
        if collideEnt.__str__() == 'Player':
            super(en.Enemy, self).damageSelf()
            en.ent.Timer(0.25, lambda: self.kill(), True)
    
    def pontuation(self) -> int:
        return super().pontuation() * 3

    def move(self, dt: float) -> None:
        '''Moves the boss normally if it isn't going backwards.\n
           If it's going backwards, moves backwards.\n''' 

        super().move(dt)