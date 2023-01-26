import GAME_NAME.enemy as en
from GAME_NAME.boss import Boss
from GAME_NAME.gameprop import *
import random

possibleSprites = ['assets/summoner/fancyalien.png',
                   'assets/summoner/soldieralien.png',
                   'assets/summoner/redcloak.png']

class Summoner(en.Enemy):
    def __init__(self, str: str, layer: int, pos: en.ent.pg.math.Vector2) -> None:
        
        super().__init__(str, layer, pos, canFusion=False)

        self.animator = en.ent.an.Animator( en.ent.pg.image.load(possibleSprites[en.ent.randint(0,len(possibleSprites)-1)]),
                                            [32,32],
                                            [3,3,3,3])

        self.summon_timer = en.ent.Timer(summoner_spawn_minion_timer, lambda: self.createMinion(), False)

        self.change_speed_timer = en.ent.Timer(4, lambda: self.changeSpeed(), False)

        self.randomizer = random.Random()
        self.speed_value = self.randomizer.randint(30,50)

    def __str__(self) -> str:
        return 'Summoner'

    def createMinion(self) -> None:
        '''Creates a summoner if too close to the player.\n
           If it's far away from the player, can create summoner, enemy or boss.\n'''

        distance = en.ent.pg.math.Vector2(self.getIconCenter() - en.ent.Entity.player.getIconCenter()).length_squared()

        if distance <= 200000:
            Summoner('', self.layer, self.icon_pos)
            return
        
        rand = self.randomizer.random()

        if rand < 0.05:
            Boss(en.ent.getBigWord(), self.layer, self.icon_pos)

        elif rand < 0.5:
            en.Enemy('', self.layer, self.icon_pos)

        else:
            Summoner(en.ent.getSmallWord(), self.layer, self.icon_pos)

    def changeSpeed(self) -> None:
        '''Changes summoner's speed randomly.\n'''

        a = self.randomizer.random()
        b = self.randomizer.randint(-1,1)
        c = self.randomizer.randint(-1,1)

        self.speed = en.ent.pg.math.Vector2(a*b, a*c)

        if self.speed.length_squared() == 0:
            self.speed = en.ent.pg.math.Vector2()
        else:
            self.speed.normalize()

    def move(self, dt: float) -> None:
        '''Summoner pursues the player if it's to far away, and moves randomly if not.\n
           Summoner can easily go out of the screen. When it happens, kills the instance.\n'''

        # pursues the player.
        distance = en.ent.pg.math.Vector2( en.ent.Entity.player.getIconCenter() - self.getIconCenter() ).length_squared()
        if distance >= 300000:
            super().move(dt)
            self.change_speed_timer.deactiveTimer()
            return

        # random movement.
        if not self.change_speed_timer.activated:
            self.change_speed_timer.activateTimer()

        if self.goingOutOfBounds():
            self.kill()
            return

        super(en.Enemy, self).move(dt)
    
    def kill(self) -> None:
        '''Deletes the entity.\n'''

        self.change_speed_timer.destroyTimer()
        self.summon_timer.destroyTimer()
        super().kill()

    def update(self, blitter: en.ent.blt.Blitter, dt: float) -> None:
        
        super().update(blitter, dt)