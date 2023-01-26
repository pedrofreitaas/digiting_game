import pygame as pg

pg.init()

#Display
sizeDisplay = [1120, 630]
screen = pg.display.set_mode( (sizeDisplay[0],sizeDisplay[1]) )

import GAME_NAME.game as gm

#Create Game
game = gm.Game( screen )

#Game loop
game.run()

pg.quit()