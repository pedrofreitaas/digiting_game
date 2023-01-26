import GAME_NAME.entity as ent
from random import randint

# don't forget to use convert_alpha() when the display is set.
possibleSprites = [ent.pg.image.load('assets/esqueletoguarda.png'), 
                   ent.pg.image.load('assets/ninjaroxo.png'),
                   ent.pg.image.load('assets/alienchique.png'),
                   ent.pg.image.load('assets/cabecaabobora.png'),
                   ent.pg.image.load('assets/soldado1.png'),
                   ent.pg.image.load('assets/soldado2.png'),
                   ent.pg.image.load('assets/soldado3.png'),
                   ent.pg.image.load('assets/fantasma.png'),
                   ent.pg.image.load('assets/fantasmaroxo.png'),
                   ent.pg.image.load('assets/bolaverde.png') ]

not_fusion_limit = 75000
max_enemy_speed = 85
min_enemy_speed = 45

class Enemy(ent.Entity):

    def fusion(en1: 'Enemy', en2: 'Enemy') -> None:
        '''Kills both parameters and creates a big word enemy.\n
           Only fusion if both enemies are fusion enabled.\n'''

        if en1.fusion_enabled and en2.fusion_enabled:
            en1.kill()
            en2.kill()

            Enemy(ent.getBigWord(), en1.layer, en1.icon_pos)

    class playerNotDefined(ValueError):
        def __str__(self) -> str:
            return 'player was not defined and it\'s set as 0'

    def __init__(self, str: str, layer: int, pos: ent.pg.math.Vector2, canFusion: bool = True) -> None:
        '''Initializes the enemy. If the word str parameter is \'\',\n
        generates a random small word to be the self.string.'''

        super().__init__(str, layer, pos)

        if self.string == '':
            self.string = ent.getSmallWord()

        ent.Entity.enemies.append(self)

        self.animator = ent.an.Animator(possibleSprites[randint(0, len(possibleSprites)-1)].convert_alpha(), [32,32], [3,3,3,3])

        self.speed_value = randint(min_enemy_speed,max_enemy_speed)

        self.fusion_enabled = canFusion

        self.changeFont(2)

    def __str__(self) -> str:
        return 'Enemy'

    def goBackward(self) -> None:
        '''Changes speed dir to make the enemy move backward.'''

        self.speed_dir = -1

    def goFoward(self) -> None:
        '''Changes speed dir to make the enemy move foward.'''

        self.speed_dir = 1

    def move(self, dt: float) -> None:
        '''Enemy move caracteristic: Icon pos does change, goes in the direction of the player.\n
           The text is centered below the icon.\n'''

        if ent.Entity.player == 0:
            raise Enemy.playerNotDefined
        
        distance = ent.pg.math.Vector2(ent.Entity.player.getIconCenter() - self.getIconCenter())

        if distance == ent.pg.math.Vector2(0,0):
            self.speed = ent.pg.math.Vector2()
        else:
            self.speed = distance.normalize()

        super().move(dt)

    def collideMethod(self, collideEnt: ent.Entity) -> None:
        super().collideMethod(collideEnt)

        if collideEnt.__str__() == 'Player':
            self.damageSelf()
            return
        
        # both are regular enemies.
        if collideEnt.__str__() == 'Enemy':
            if len(self.string) + len(collideEnt.string) >= 20:
                return

            distancePlayer = ent.pg.math.Vector2(self.getIconCenter() - ent.Entity.player.getIconCenter()).length_squared()
            if distancePlayer <= not_fusion_limit:
                return

            Enemy.fusion(self, collideEnt)

            return

        # not implemented
        if collideEnt.__str__() == 'Boss':
            pass      

    def damageSelf(self) -> None:
        '''Calls kill procedures for normal enemies.\n
           Kills the enemy after a short time.\n'''

        super().damageSelf()
        ent.Timer(0.25, lambda: self.kill(), True)

    def kill(self) -> None:
        '''Make the enemy bool death variable go True.\n
           Removes the enemy from the enemies list in the super class.\n'''
        
        super().kill()
