import pygame as pg
from .helpers import isMasterClass, getAnchors, convertAnchor, getPercantage

defaults = {
  "window": {
    "size": (320, 240),
    "caption": "new window",
    "background": (25, 25, 30),
    "resizable": False,
    "fps": 10
  },
  "surface": {
    "size": (200, 150),
    "background": (255, 255, 255),
    "position": (0, 0),
    "resizable": False,
    "dragable": True,
    "drag-area": None,
    "anchors": None
  },
  "panel": {
    "size": (100, 300),
    "background": (100, 100, 100),
    "position": (0, 0),
    "resizable": False,
    "dragable": False,
    #"drag-area": pg.Rect((0, 0), (100, 20)),
    "drag-area": None,
    "anchors": None
  }
}

def validateGuiConfig(config, type):
    """Return a type based configuration to create the gui element."""
    t = type
    validated_config = {}

    # size
    if t == "window" or t == "surface" or t == "panel":
        try:
            validated_config["size"] = config["size"]
        except KeyError:
            validated_config["size"] = defaults[type]["size"]
    # caption
    if t == "window":
        try:
            validated_config["caption"] = config["caption"]
        except KeyError:
            validated_config["caption"] = defaults[type]["caption"]
    # background
    if t == "window" or t == "surface" or t == "panel":
        try:
            validated_config["background"] = config["background"]
        except KeyError:
            validated_config["background"] = defaults[type]["background"]
    # resizable
    if t == "window" or t == "surface" or t == "panel":
        try:
            validated_config["resizable"] = config["resizable"]
        except KeyError:
            validated_config["resizable"] = defaults[type]["resizable"]
    # dragable
    if t == "surface" or t == "panel":
        try:
            validated_config["dragable"] = config["dragable"]
        except KeyError:
            validated_config["dragable"] = defaults[type]["dragable"]
    # drag area
    if t == "surface" or t == "panel":
        try:
            validated_config["drag-area"] = config["drag-area"]
        except KeyError:
            validated_config["drag-area"] = defaults[type]["drag-area"]
    # fps
    if t == "window":
        try:
            validated_config["fps"] = config["fps"]
        except KeyError:
            validated_config["fps"] = defaults[type]["fps"]
    # position
    if t == "surface" or t == "panel":
        try:
            validated_config["position"] = config["position"]
        except KeyError:
            validated_config["position"] = defaults[type]["position"]
    # anchors
    if t == "surface" or t == "panel":
        try:
            validated_config["anchors"] = config["anchors"]
        except KeyError:
            validated_config["anchors"] = defaults[type]["anchors"]

    return validated_config

class Window(object):
    """pygame window surface in a wrapper."""
    def __init__(self, config={}, type="window"):
        """Constructor."""
        self.config = validateGuiConfig(config, type)
        self.type = type
        self.size = self.config["size"]
        self.anchorpoints = getAnchors(self.size)
        self.caption = self.config["caption"]
        self.background = self.config["background"]
        self.resizable = self.config["resizable"]
        self.clock = pg.time.Clock()
        self.fps = self.config["fps"]
        self.screen = self.__createWindow()
        self.events = {
            "resize": None,
            "move": None,
            "click": None,
            "mousedownleft": False
            }
    def __createWindow(self):
        """Create main window element."""
        pg.init()
        if self.resizable:
            pg.display.set_mode(self.size, pg.RESIZABLE)
        else:
            pg.display.set_mode(self.size)
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
        self.config = validateGuiConfig(config, type)
        if parent:
            self.parent = parent
        else:
            self.parent = pg.display.get_surface()
        self.type = type
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
        if self.config["drag-area"].__class__ is pg.Rect:
            self.dragarea = self.config["drag-area"]
        elif self.config["drag-area"].__class__ is tuple:
            self.dragarea = pg.Rect(self.config["drag-area"])
        else:
            self.dragarea = None
        self.__built()
        self.reposition(self.calcPosition())
        self.events = {
            "hover": None,
            "click": False,
            "clickedAt": None
        }
    def __built(self):
        """Throw everything together."""
        pg.Surface.__init__(self, (self.width, self.height))
        self.rect = self.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.fill(self.background)
        # dragging bar
        if self.dragarea is not None:
            pg.draw.rect(self, (30, 50, 70), self.dragarea)
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
            if mx >= dragy and mx <= dragx + dragw:
                collision["x"] = mx
            if my >= dragy and my <= dragy + dragh:
                collision["y"] = my
        else:
            if mx >= self.rect.x and mx <= self.rect.x + self.rect.w:
                collision["x"] = mx
            if my >= self.rect.y and my <= self.rect.y + self.rect.h:
                collision["y"] = my
        if collision["x"] and collision["y"]:
            self.events["hover"] = (mx - self.x, my - self.y)
        else:
            self.events["hover"] = None
        # click
        if self.events["hover"]:
            if window_events["click"]:
                self.events["click"] = True
                if not self.events["clickedAt"]:
                    self.events["clickedAt"] = (mx - self.x, my - self.y)
            else:
                self.events["click"] = False
                self.events["clickedAt"] = None
        #drag and drop
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
        position = (self.width, self.height)
        if self.anchors:
            parent_anchors = getAnchors(self.parent.get_rect().size)
            position = convertAnchor(parent_anchors, self.size, self.anchors)
        else:
            position = (self.width, self.height)

        return position
    def resize(self, size):
        """Calculate size if percantage is given."""
        if size[0].__class__ is str or size[1].__class__ is str:
            s = getPercantage(self.parent.get_rect().size, size)
        else:
            s = size

        self.width, self.height = s
        self.__built()
class Panel(Surface):
    """Create a new gui panel"""
    def __init__(self, config={}, type="panel"):
        """Constructor."""
        super().__init__(config, type)
        # Surface.__init__(self, config=config, type=type)
        #print(self.config)
