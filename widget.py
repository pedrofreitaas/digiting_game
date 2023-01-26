import pygame as pg 

class Button():
    id = 1
    buttons: list['Button'] = []

    def deleteButtons() -> None:
        '''Deletes all the storaged buttons.\n'''
        Button.buttons.clear()

    def updButtons(events: list[pg.event.Event]) -> None:

        for button in Button.buttons:
            button.update(events)

    def __eq__(self, __o: object) -> bool:
        if type(self) == type(__o) and self.id == __o.id:
            return True
        return False

    def __init__(self, txt: str, pos: pg.math.Vector2, procedure: callable, font: pg.font.Font, color: pg.color.Color, once=True) -> None:
        '''Once-> if false the button won't be deleted after it's clicked.\n'''

        self.id = Button.id
        Button.id += 1

        self.once = once

        self.text = txt
        self.pos = pos
        self.procedure = procedure

        self.font = font
        self.font_color = color

        self.rect = self.getImage().get_rect().move(self.pos)

        Button.buttons.append(self)

    def setPos(self, pos: pg.math.Vector2) -> None:
        self.pos = pos

    def getImage(self) -> pg.surface.Surface:
        return self.font.render(self.text, 1, self.font_color)
    
    def getImageSize(self) -> tuple[float, float]:
        return self.getImage().get_size()

    def update(self, events: list[pg.event.Event]) -> None:
        self.rect = self.getImage().get_rect().move(self.pos)

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
                self.procedure()
                if self.once: self.kill()

    def kill(self) -> None:
        Button.buttons.remove(self)
