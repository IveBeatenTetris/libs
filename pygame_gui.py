import pygame as pg
from .helpers import(
    isMasterClass,
    getAnchors,
    convertAnchor,
    getPercantage,
    validateDict)
pg.font.init()

# default colors
colors = {
    "white": (255 , 255 , 255),
    "black": (0 , 0 , 0),
    "red": (255 , 0 , 0),
    "green": (0 , 255 , 0),
    "blue": (0 , 0 , 255)
    }
# gui defaults
defaults = {
    "all": {
        "position": (0, 0),
        "size": (0, 0),
        "text": "My Text",
        "font": "arial",
        "font-size": 16,
        "font-color": colors["black"]
        },
    "window": {
        "caption": "new window",
        "size": (320, 240),
        "background": (25, 25, 30),
        "resizable": False,
        "fps": 10
        },
    "surface": {
        "caption": None,
        "size": (200, 150),
        "background": (255, 255, 255),
        "position": (0, 0),
        "resizable": False,
        "dragable": True,
        "drag-area": None,
        "anchors": None,
        "text": None
        },
    "grid": {
        "caption": None,
        "size": ("100%", "100%"),
        "position": (0, 0),
        "background": None,
        "anchors": None,
        "resizable": False,
        "drag-area": None,
        "dragable": False,

        "cells": (10, 10),
        "line-color": (100, 148, 237),
        "line-weight": 1,
        },
    "panel": {
        "caption": None,
        "size": (100, 300),
        "background": (100, 100, 100),
        "position": (0, 0),
        "resizable": False,
        "dragable": False,
        #"drag-area": pg.Rect((0, 0), (100, 20)),
        "drag-area": None,
        "anchors": None,
        "text": None
        },
    "text": {
        "caption": None,
        "size": (0, 0),
        "background": None,
        "position": (0, 0),
        "resizable": False,
        "dragable": False,
        "drag-area": None,
        "anchors": None,

        "text": "New Text",
        "font": "arial",
        "font-color": colors["black"],
        "font-size": 16
        },
    "simple-text": {
        "text": "New Text",
        "font": "arial",
        "font-color": colors["black"],
        "font-size": 16,
        "background": None
        }
    }

class Window(object):
    """pygame window surface in a wrapper."""
    def __init__(self, config={}, type="window"):
        """Constructor."""
        # validate the dict that has been declared self.config
        self.config = validateDict(config, defaults["window"])
        # give it a non-namespace type for you
        self.type = type
        # size of the window. can be tuple of int or strings
        self.size = self.config["size"]
        # anchor poins are positional coordinates to lock elements in it
        self.anchorpoints = getAnchors(self.size)
        # the title for the window
        self.caption = self.config["caption"]
        # TODO background is still only a color. images have to be implated
        # window's background color in a tuple (int, int, int)
        self.background = self.config["background"]
        # True or False
        self.resizable = self.config["resizable"]
        # pygame clock to manage ticks
        self.clock = pg.time.Clock()
        # each fps is a tick that calls pygame's update function
        self.fps = self.config["fps"]
        # create the pygame surface for window as a property
        self.screen = self.__createWindow()
        # predefined events. they will be updated with each window check
        self.events = {
            "resize": None,
            "move": None,
            "click": None,
            "mousedownleft": False
            }
    def __createWindow(self):
        """Create main window element."""
        # initialiaze thw pygame window object
        pg.init()
        # decide if either resizable or not
        if self.resizable:
            pg.display.set_mode(self.size, pg.RESIZABLE)
        else:
            pg.display.set_mode(self.size)
        # fill it with background-color
        display = pg.display.get_surface()
        display.fill(self.background)

        return display
    def update(self):
        """Update the window surface."""
        pg.display.update()
        # pg.display.flip()
        self.clock.tick(self.fps)
        self.screen.fill(self.background)
    def draw(self, obj, pos=None):
        """Draw onto the window."""
        elements = []

        if isMasterClass(obj, Surface):
            elements.append(obj)
        elif obj.__class__ is dict:
            for each in obj:
                if obj[each].__class__ is Surface or isMasterClass(obj[each], Surface):
                    elements.append(obj[each])

        for each in elements:
            #each.update()# needed to pre-draw surfaces
            if not pos:
                position = each.position
            else:
                position = pos
            self.screen.blit(each, position)
    def getEvents(self, elements={}):
        """Return a dict of window driven events."""
        for event in [pg.event.wait()] + pg.event.get():
            # closed window
            if event.type is pg.QUIT or (event.type is pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.close()
            # window resized
            if event.type is pg.VIDEORESIZE:
                self.resize(event.size)
                self.events["resize"] = event.size
            else:
                self.events["resize"] = None
            # clicked
            if event.type is pg.MOUSEBUTTONDOWN:
                # clicked left
                if event.button is 1:
                    self.events["click"] = pg.mouse.get_pos()
                    self.events["mousedownleft"] = True
            # released
            if event.type is pg.MOUSEBUTTONUP:
                # released left
                if event.button is 1:
                    self.events["click"] = None
                    self.events["mousedownleft"] = False
            # moving the mouse
            if event.type is pg.MOUSEMOTION:
                self.events["move"] = pg.mouse.get_pos()
            else:
                self.events["move"] = None

            # elements events
            for each in elements:
                elem = elements[each]
                # update events
                elem.getEvents(self.events)
                # if anchor: change position on resize
                if event.type is pg.VIDEORESIZE:
                    if elem.anchors:
                        elem.reposition(elem.calcPosition())
                    if elem.size[0].__class__ is str or elem.size[1].__class__ is str:
                        elem.resize(elem.size)
                        #print(elem.width, elem.height)
                    elem.update()

        return self.events
    def close(self):
        """Close the window and shut down pygame."""
        import sys
        pg.quit()
        sys.exit()
    def resize(self, size):
        """Resizing element."""
        self.size = size
        self.screen = self.__createWindow()
        self.anchorpoints = getAnchors(self.size)
class Surface(pg.Surface):
    """Surface template class for gui elements."""
    def __init__(self, config={}, type="surface", parent=None):
        """Constructor."""
        if self.__class__ is Surface:
            default = defaults["surface"]
        elif self.__class__ is Panel:
            default = defaults["panel"]
        elif self.__class__ is Text:
            default = defaults["text"]
        elif self.__class__ is Grid:
            default = defaults["grid"]
        self.config = validateDict(config, default)
        if parent:
            self.parent = parent
        else:
            self.parent = pg.display.get_surface()
        self.type = type
        self.caption = self.config["caption"]
        self.size = self.config["size"]
        if self.size[0].__class__ is str or self.size[1].__class__ is str:
            s = getPercantage(self.parent.get_rect().size, self.size)
        else:
            s = self.size
        self.width, self.height = s
        self.position = self.config["position"]
        self.x = self.position[0]
        self.y = self.position[1]
        self.anchors = self.config["anchors"]
        self.anchorpoints = getAnchors((self.width, self.height))
        self.background = self.config["background"]
        self.resizable = self.config["resizable"]
        self.dragable = self.config["dragable"]
        if "drag-area" in self.config:
            if self.config["drag-area"].__class__ is pg.Rect:
                self.dragarea = self.config["drag-area"]
            elif self.config["drag-area"].__class__ is tuple:
                self.dragarea = pg.Rect(self.config["drag-area"])
            else:
                self.dragarea = None
        else:
            self.dragarea = None

        self.__built()
        self.reposition(self.calcPosition())

        self.events = {
            "hover": None,
            "click": False,
            "clickedAt": None
        }
    def __str__(self):
        """Object to str."""
        return repr(self)
    def __repr__(self):
        """Object representation."""
        return '<Surface({}, {})>'.format((self.x, self.y), self.size)
    def __built(self):
        """Throw everything together."""
        if self.background is None:
            pg.Surface.__init__(self, (self.width, self.height), pg.SRCALPHA)
        else:
            pg.Surface.__init__(self, (self.width, self.height))
        self.rect = self.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # background
        self.__createBackground()
        # dragging bar
        if self.dragarea:
            pg.draw.rect(self, (30, 50, 70), self.dragarea)
        # caption
        if self.caption:
            cfg = {}
            cfg["text"] = self.caption
            cfg["font-color"] = colors["white"]
            cfg["font-size"] = 14
            cfg["anchors"] = ("center", 4)
            c = Text(cfg, parent=self)
            #c = SimpleText(cfg, parent=self)
            self.blit(c, (c.x, c.y))
            #self.blit(c, (0, 0))

        #self.update()
    def __createBackground(self):
        if self.background is not None:
            if self.background.__class__ is tuple:
                self.fill(self.background)
    def update(self):
        """Update method for overwriting purpose."""
        pass
    def getEvents(self, window_events):
        """Return a dict of events."""
        mx, my = pg.mouse.get_pos()

        # hover
        collision = {"x": None, "y": None}
        if self.dragarea is not None:
            dragx = self.rect.x + self.dragarea.x
            dragy = self.rect.y + self.dragarea.y
            dragw = self.dragarea.w
            dragh = self.dragarea.h
        else:
            dragx = self.rect.x
            dragy = self.rect.y
            dragw = self.rect.w
            dragh = self.rect.h
        if mx >= dragx and mx <= dragx + dragw:
            collision["x"] = mx
        if my >= dragy and my <= dragy + dragh:
            collision["y"] = my
        if collision["x"] and collision["y"]:
            self.events["hover"] = (mx - self.x, my - self.y)
        else:
            self.events["hover"] = None

        # //TODO dragging still works from outside of the surface to the inside
        # click
        if self.events["hover"]:
            if window_events["click"]:
                self.events["click"] = True
                if not self.events["clickedAt"]:
                    self.events["clickedAt"] = (mx - self.x, my - self.y)
            else:
                self.events["click"] = False
                self.events["clickedAt"] = None

        # drag and drop
        if self.events["clickedAt"]:
            cl = self.events["clickedAt"]
            if self.dragable:
                self.reposition((mx - cl[0], my - cl[1]))

        return self.events
    def reposition(self, pos=None):
        if pos:
            self.position = pos
            self.x, self.y = pos
            self.rect.x = self.x
            self.rect.y = self.y
    def calcPosition(self):
        """Calculate position coordinates of anchors."""
        #position = (self.width, self.height)
        if self.anchors:
            parent_anchors = getAnchors(self.parent.get_rect().size)
            position = convertAnchor(parent_anchors, self.size, self.anchors)
        else:
            position = (self.x, self.y)

        return position
    def resize(self, size):
        """Calculate size if percantage is given."""
        if size[0].__class__ is str or size[1].__class__ is str:
            s = getPercantage(self.parent.get_rect().size, size)
        else:
            s = size

        self.width, self.height = s
        self.__built()
class Grid(Surface):
    """Surface template class for gui elements."""
    def __init__(self, config={}, type="grid", parent=None):
        """Constructor."""
        super().__init__(config, type)
    def __createGrid(self):
        """Create a grid, draw it to a surface and return it."""
        size = self.parent.get_rect().size
        surface = pg.Surface(size, pg.SRCALPHA)
        surface = self.drawGrid(surface)

        return surface
    def update(self):
        """Overwrite the Surface's update method."""
        # create the lines
        self.grid = self.__createGrid()
        self.blit(self.grid , self.parent.get_rect().topleft)
    def drawGrid(self, surface):
        """Draw lines in a grid to the given surface. Then return it."""
        color = self.config["line-color"]
        weight = self.config["line-weight"]
        cells = self.config["cells"]
        parent = self.parent.get_rect()
        size = self.rect.size
        left = int(size[0] / cells[0])
        top = int(size[1] / cells[1])

        # drawing
        start = (0, 0)
        end = (0, parent.height)
        for i in range(cells[0]):
            pg.draw.line(surface, color, start, end, weight)
            start = (start[0] + left, start[1])
            end = (end[0] + left, end[1])
        start = (0, 0)
        end = (parent.width, 0)
        for i in range(cells[0]):
            pg.draw.line(surface, color, start, end, weight)
            start = (start[0], start[1] + top)
            end = (end[0], end[1] + top)

        return surface
class Panel(Surface):
    """Create a new gui panel."""
    def __init__(self, config={}, type="panel"):
        """Constructor."""
        super().__init__(config, type)
        # Surface.__init__(self, config=config, type=type)
        #print(self.config)
class Text(Surface):
    """Create a new gui text."""
    def __init__(self, config={}, type="text", parent=None):
        """Constructor."""
        # text
        try:
            text = config["text"]
        except KeyError:
            text = defaults["text"]["text"]
        # font-size
        try:
            font_size = config["font-size"]
        except KeyError:
            font_size = defaults["text"]["font-size"]
        font = pg.font.SysFont("arial", 12, True, False)
        text = font.render(text, True, colors["white"])

        config["size"] = text.get_rect().size
        #config["background"] = colors["white"]
        #config["dragable"] = True

        super().__init__(config, type, parent)
        self.blit(text, (0, 0))
class SimpleText(pg.Surface):
    """Create a new gui text."""
    def __init__(self, config={}, parent=None):
        """Constructor."""
        self.config = validateDict(config, defaults["simple-text"])
        self.text = self.config["text"]
        self.font = self.config["font"]
        self.fontSize = self.config["font-size"]
        self.fontColor = self.config["font-color"]
        self.background = self.config["background"]

        font = pg.font.SysFont(self.font, self.fontSize, True, False)
        text = font.render(self.text, True, self.fontColor)

        if self.background is None:
            pg.Surface.__init__(self, text.get_rect().size, pg.SRCALPHA)
        else:
            pg.Surface.__init__(self, (0, 0))
        self.blit(text, (0, 0))
