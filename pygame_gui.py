import pygame as pg
from .helpers import(
    isMasterClass,
    getAnchors,
    convertAnchor,
    getPercantage,
    validateDict)
pg.font.init()

# default colors
COLORS = {
    "white": (255 , 255 , 255),
    "black": (0 , 0 , 0),
    "red": (255 , 0 , 0),
    "green": (0 , 255 , 0),
    "blue": (0 , 0 , 255)
    }
# gui defaults
DEFAULTS = {
    "all": {
        "position": (0, 0),
        "size": (0, 0),
        "text": "My Text",
        "font": "arial",
        "font-size": 16,
        "font-color": COLORS["black"]
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
        "font-color": COLORS["black"],
        "font-size": 16
        },
    "simple-text": {
        "text": "New Text",
        "font": "arial",
        "font-color": COLORS["black"],
        "font-size": 16,
        "background": None
        }
    }

class Window(object):
    """pygame window surface in a wrapper."""
    def __init__(self, config={}, type="window"):
        """Constructor."""
        # validate the dict that has been declared self.config
        self.config = validateDict(config, DEFAULTS["window"])
        # give it a non-namespace type for you
        self.type = type
        # TODO percentage size still has to be implemented
        # size of the window. can be tuple of int or strings
        self.size = self.config["size"]
        # anchor poins are positional coordinates to lock elements in it
        self.anchorpoints = getAnchors(self.size)
        # the title for the window
        self.caption = self.config["caption"]
        # TODO background is still only a color. images have to be implemented
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
            "resize": None,# tuple / none
            "move": None,# tuple / none
            "click": None,# tuple / none
            "mousedownleft": False# bool
            }
    def __createWindow(self):# pygame display
        """Create main window element and return it. background is going to be
        filled as well."""
        # initialiaze thw pygame window object
        pg.init()
        # resizability
        if self.resizable:
            pg.display.set_mode(self.size, pg.RESIZABLE)
        else:
            pg.display.set_mode(self.size)
        # set window's caption
        pg.display.set_caption(self.caption)
        # fill it with background-color
        display = pg.display.get_surface()
        display.fill(self.background)
        # return the new created pygame display object
        return display
    def update(self):
        """Update the window surface. to be called at each end of the main
        file's loop."""
        # entire display update. pass surface or rect for area update only
        pg.display.update()
        # pygame tick
        self.clock.tick(self.fps)
        # fill with background color
        self.screen.fill(self.background)
    def draw(self, obj, pos=None):
        """Draw onto the window. obj can be an gui element, pg.Surface, dict or
        list. it will be converted into a iterable list and draw each of them
        to the screen."""
        # new list to fetch all the objects from obj
        elements = []
        # if obj is a gui element
        if isMasterClass(obj, Surface):
            # append this element to elements[]
            elements.append(obj)
        # if obj is a dictionary
        elif obj.__class__ is dict:
            # walk every single object in obj{}
            for each in obj:
                # shortcut
                e = obj[each]
                # if obj is a gui element
                if e.__class__ is Surface or isMasterClass(e, Surface):
                    # append this element to elements[]
                    elements.append(e)
        # elements[] now owns every object from obj and is ready to walk trough
        for each in elements:
            # if there are no given position tuples
            if not pos:
                # set the gui elemenets nested position coordinates
                position = each.position
            # if position argument is given
            else:
                # set the given tuple
                position = pos
            # draw this turn's element to the screen
            self.screen.blit(each, position)
    def getEvents(self, elements={}):
        """Return a dict of window driven events."""
        # for each pygame event
        for event in [pg.event.wait()] + pg.event.get():
            # clicked window close button
            if event.type is pg.QUIT:
                # call the close method
                self.close()
            # pressed ESC key
            elif (event.type is pg.KEYDOWN and event.key is pg.K_ESCAPE):
                # call the close method
                self.close()
            # resized window
            if event.type is pg.VIDEORESIZE:
                # call window's resize method
                self.resize(event.size)
                # set window's resize-event to tuple
                self.events["resize"] = event.size
            # exception made if window hasn't been resized
            else:
                # set window's resize-event to none
                self.events["resize"] = None
            # clicked
            if event.type is pg.MOUSEBUTTONDOWN:
                # if button is left mouse button
                if event.button is 1:
                    # set window's click-event to mouse positional coordinates
                    self.events["click"] = pg.mouse.get_pos()
                    # set window's mousedownleft-event to true
                    self.events["mousedownleft"] = True
            # released button
            if event.type is pg.MOUSEBUTTONUP:
                # if button is left mouse button
                if event.button is 1:
                    # set window's click-event to none
                    self.events["click"] = None
                    # set window's mousedownleft-event to false
                    self.events["mousedownleft"] = False
            # moving the mouse
            if event.type is pg.MOUSEMOTION:
                # set window's move-event to mouse positional coordinates
                self.events["move"] = pg.mouse.get_pos()
            # exception made if mouse hasn't moved
            else:
                # set window's move-event to none
                self.events["move"] = None
            # for each gui elements in elements{}
            for each in elements:
                # shortcut
                elem = elements[each]
                # check if there are events in the elemenet's scope
                elem.getEvents(self.events)
                # if window is getting resized
                if event.type is pg.VIDEORESIZE:
                    # if element has an anchor
                    if elem.anchors:
                        # calculate element's new position
                        position = elem.calcPosition()
                        # call the elements's reposition() function
                        elem.reposition(position)
                    # shortcut
                    width = elem.size[0].__class__
                    # shortcut
                    height = elem.size[1].__class__
                    # if one value in size() is a string
                    if width is str or height is str:
                        # call element's resize method with it's size() as arg
                        elem.resize(elem.size)
                    # call element's update method. IMPORTANT
                    elem.update()
        # return new created events{} dict
        return self.events
    def close(self):
        """Close the window and shut down pygame."""
        #import sys module for quick execution
        import sys
        # exit pygame
        pg.quit()
        # close window and delete process
        sys.exit()
    def resize(self, size):
        """Resizing element."""
        # sets a new size property. tuple can also include strings
        self.size = size
        # recreate the window object
        self.screen = self.__createWindow()
        # recreates window's inner anchor points for sub elements
        self.anchorpoints = getAnchors(self.size)
class Surface(pg.Surface):
    """Surface template class for gui elements."""
    def __init__(self, config={}, type="surface", parent=None):
        """Constructor."""
        # set type's default config dependig on it's given 'type' argument
        if self.__class__ is Surface:
            default = DEFAULTS["surface"]
        elif self.__class__ is Panel:
            default = DEFAULTS["panel"]
        elif self.__class__ is Text:
            default = DEFAULTS["text"]
        elif self.__class__ is Grid:
            default = DEFAULTS["grid"]
        # validate config{} by default{}
        self.config = validateDict(config, default)
        # if parent object is given
        if parent:
            # overtake the object
            self.parent = parent
        # exception on none given parent
        else:
            # make the pygame window surface a parent
            self.parent = pg.display.get_surface()
        # give it a non-namespace type for you
        self.type = type
        # otional title for the gui element
        self.caption = self.config["caption"]
        # set self's size property. tuple can hold strings and integers
        self.size = self.config["size"]
        # calculate width and height out of already given size() property
        self.width, self.height = self.calcSize()
        # position property. tuple must hold integers
        self.position = self.config["position"]
        # x and y are used for calculating position of this gui element
        self.x = self.position[0]
        self.y = self.position[1]
        # anchors are the actual positioners. they can hold strings of
        # positional arguments, which are used to calculate the final position
        # tuple. example: ("left", "top") or ("center", "middle")
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
            cfg["font-color"] = COLORS["white"]
            cfg["font-size"] = 14
            cfg["anchors"] = ("center", 4)
            # TODO optimize caption positioning
            c = Text(cfg, parent=self)
            #c = SimpleText(cfg, parent=self)
            self.blit(c, (c.x, c.y))

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

        self.size = size
        self.width, self.height = s
        self.__built()
    def calcSize(self):
        """Calculate self's size and return a tuple of integers."""
        # shortcuts
        width = self.size[0].__class__
        height = self.size[1].__class__
        parent_size = self.parent.get_rect().size
        # if self's size() property has a string value
        if width is str or height is str:
            # check percantage in self's size() and calculate a new one
            s = getPercantage(parent_size, self.size)
        # except on integers as values in self's size()
        else:
            # s is now a tuple of two integers
            s = self.size

        return s
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
class Text(Surface):
    """Create a new gui text."""
    def __init__(self, config={}, type="text", parent=None):
        """Constructor."""
        # text
        try:
            text = config["text"]
        except KeyError:
            text = DEFAULTS["text"]["text"]
        # font-size
        try:
            font_size = config["font-size"]
        except KeyError:
            font_size = DEFAULTS["text"]["font-size"]
        font = pg.font.SysFont("arial", 12, True, False)
        text = font.render(text, True, COLORS["white"])

        config["size"] = text.get_rect().size
        #config["background"] = colors["white"]
        #config["dragable"] = True

        super().__init__(config, type, parent)
        self.blit(text, (0, 0))
class SimpleText(pg.Surface):
    """Create a new gui text."""
    def __init__(self, config={}, parent=None):
        """Constructor."""
        self.config = validateDict(config, DEFAULTS["simple-text"])
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
