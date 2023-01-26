import time as tm
import blitter as bl
import GAME_NAME.player as pl
import GAME_NAME.enemy as emy
import GAME_NAME.boss as boss
import GAME_NAME.summoner as sm
import GAME_NAME.map as map
from GAME_NAME.gameprop import *
from widget import *
from random import randint

def randomPos() -> pg.math.Vector2:
    return pg.math.Vector2(randint(0,pg.display.get_surface().get_size()[0]), -randint(0,200))

def summonEnemy() -> None:
    emy.Enemy('', 1, randomPos())

def summonBoss() -> None:
    boss.Boss(pl.ent.getBigWord(), 1, randomPos())

def summonSummoner() -> None:
    sm.Summoner(pl.ent.getRandomWord(), 1, randomPos())

class Game():
    game_sound = pg.mixer.Sound('assets/sounds/epic.mp3')
    game_sound.set_volume(game_volume)

    def __init__(self, display) -> None:
        
        #booleans
        self.show_fps = True

        # 0 -> playing, 1-> paused, 2-> endscreen, 3-> quit.
        self.state = 0

        #Blitter
        self.Blitter = bl.Blitter(display, 2)

        #Player
        self.player = pl.Player('', 1, pg.math.Vector2(0,0), self.Blitter.display)

        for layer in range(5):
            self.Blitter.createLayer()

        #Clock
        self.clock = pg.time.Clock()

        #Fps
        self.font = pl.ent.fonts[0]

        #Background
        self.map = map.Map(self.Blitter.displaySize())

        #Timers
        self.enemy_generator = pl.ent.Timer(spawn_enemy_timer, lambda: summonEnemy(), False)
        self.boss_generator = pl.ent.Timer(spawn_boss_timer, lambda: summonBoss(), False)
        self.summoner_generator = pl.ent.Timer(spawn_summoner_timer, lambda: summonSummoner(), False)
        self.increase_difficult_timer = pl.ent.Timer(increase_difficult_timer, lambda: self.increaseDifficult(), False)

    def updateFPS(self) -> pg.surface:
        fps = str(int(self.clock.get_fps()))
        fpsText = self.font.render(fps, 1, pg.Color("coral"))
        
        return fpsText

    def blitFPS(self) -> None:
        if not self.show_fps:
            return
        
        blitPOS = [self.Blitter.displaySize()[0]-100,0]
        self.Blitter.addImageInLayer(self.Blitter.lastLayer(), self.updateFPS(), blitPOS )

    def checkEvents(self, events: list) -> None:
        """Keys general game events, such as keys."""
        
        for event in events:
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    self.pause()

    def increaseDifficult(self) -> None:
        '''After a {increase_difficult_timer} seconds, the time of the cycle to spawn enemies is decreased.\n'''

        global spawn_enemy_timer, spawn_summoner_timer, spawn_boss_timer, summoner_spawn_minion_timer

        if spawn_enemy_timer > 0.85:
            spawn_enemy_timer -= 0.1
            self.enemy_generator.changeTime(spawn_enemy_timer)

        if spawn_summoner_timer > 8:
            spawn_summoner_timer -= 0.1
            self.summoner_generator.changeTime(spawn_summoner_timer)

        if spawn_boss_timer > 10:
            spawn_boss_timer -= 0.1
            self.boss_generator.changeTime(spawn_boss_timer)

        # only affects new summoners.
        if summoner_spawn_minion_timer > 3:
            summoner_spawn_minion_timer -= 0.1

# game states controllers.
    def unpause(self) -> None:
        self.state = 0

    def pause(self) -> None:
        self.state = 1

    def playerDead(self) -> None:
        self.state = 2

    def quit(self) -> None:
        self.state = 3
# --------------------------- #

    def UNmute(self) -> None:
        if pg.mixer.get_busy():
            self.game_sound.stop()
        else:
            self.game_sound.play(-1)

    def UNshowFPS(self) -> None:
        self.show_fps = not self.show_fps

    def gamescreen(self) -> None:

        previous = tm.time()

        while self.state == 0:
            
            if self.player.is_dead:
                self.playerDead()
                break
                    
            # delta time
            current =  tm.time()
            dt = current - previous
            previous = current

            events = pg.event.get()
            self.checkEvents(events)

            self.map.update(self.Blitter)

            pl.ent.Entity.updEntities(self.Blitter, events, dt)
            pl.ent.Entity.checkLists()

            self.clock.tick(120)
            
            self.blitFPS()

            self.Blitter.update( pg.math.Vector2(0,0) )

        pl.ent.Timer.pauseAllTimers()

    def pausescreen(self) -> None:
        
        playBt = Button('Click to play.', pg.math.Vector2(), lambda: self.unpause(), self.font, 'black')
        playBt.setPos( pg.math.Vector2(pg.display.get_window_size())/2 - pg.math.Vector2(playBt.getImageSize())/2 )

        muteBt = Button('Mute', pg.math.Vector2(), lambda: self.UNmute(), self.font, 'black', once=False)
        muteBt.setPos(pg.math.Vector2(pg.display.get_window_size()[0] - muteBt.getImageSize()[0], 0))

        showFPSBt = Button('Show Fps', pg.math.Vector2(), lambda: self.UNshowFPS(), self.font, 'black', once=False)
        showFPSBt.setPos(pg.math.Vector2(pg.display.get_window_size()[0] - showFPSBt.getImageSize()[0], muteBt.getImageSize()[1]+20))

        while self.state == 1:
            
            events = pg.event.get()
            self.checkEvents(events)
            
            self.Blitter.addImageInLayer(1, playBt.getImage(), playBt.pos)
            self.Blitter.addImageInLayer(1, muteBt.getImage(), muteBt.pos)
            self.Blitter.addImageInLayer(1, showFPSBt.getImage(), showFPSBt.pos)

            self.Blitter.update( pg.math.Vector2() )
            Button.updButtons(events)

        Button.deleteButtons()
        pl.ent.Timer.unpauseAllTimers()

    def endscreen(self) -> None:

        pontuation = Button('Pontuation: ' + str(self.player.pontuation), pg.math.Vector2(), None, self.font, 'black')
        pontuation.setPos( pg.math.Vector2(pg.display.get_window_size())/2 - pg.math.Vector2(pontuation.getImageSize())/2 )

        quitBt = Button('Quit', pg.math.Vector2(), lambda: self.quit(), self.font, 'black', once=True)
        quitBt.setPos( pg.math.Vector2(pg.display.get_window_size())/2 - pg.math.Vector2(quitBt.getImageSize())/2 + pg.math.Vector2(0, pontuation.getImageSize()[1]))

        while self.state == 2:
            
            events = pg.event.get()
            self.checkEvents(events)
            
            self.Blitter.addImageInLayer(1, pontuation.getImage(), pontuation.pos)
            self.Blitter.addImageInLayer(1, quitBt.getImage(), quitBt.pos)

            self.Blitter.update( pg.math.Vector2() )
            Button.updButtons(events)

        Button.deleteButtons()

    def run(self) -> None:
        self.game_sound.play(-1)

        while self.state != 3:

            if self.state == 0:
                self.gamescreen()

            elif self.state == 1:
                self.pausescreen()

            elif self.state == 2:
                self.endscreen()

        self.game_sound.stop()