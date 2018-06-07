import pygame as pg
from .helpers import isMasterClass

defaults = {
  "window" : {
    "size" : (320 , 240),
    "caption" : "new window",
    "background" : (25 , 25 , 30),
    "resizable" : False,
    "fps": 10
  },
  "surface" : {
    "size" : (200 , 150),
    "background" : (255 , 255 , 255),
    "position" : (0 , 0),
    "resizable" : False
  },
  "panel" : {
    "size" : (100 , 300),
    "background" : (100 , 100 , 100),
    "position" : (100 , 100),
    "resizable" : False
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

    return validated_config

class Window(object):
    """pygame window surface in a wrapper."""
    def __init__(self, config={}, type="window"):
        """Constructor."""
        self.config = validateGuiConfig(config, type)
        self.size = self.config["size"]
        self.caption = self.config["caption"]
        self.background = self.config["background"]
        self.resizable = self.config["resizable"]
        self.clock = pg.time.Clock()
        self.fps = self.config["fps"]
        self.screen = self.__createWindow()
        self.events = {
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
        if obj.__class__ is dict:
            for each in obj:
                if obj[each].__class__ is Surface or isMasterClass(obj[each], Surface):
                    if not pos:
                        pos = obj[each].position
                    self.screen.blit(obj[each], pos)
        elif obj.__class__ is Surface or isMasterClass(obj, Surface):
            if not pos:
                pos = obj.position
            self.screen.blit(obj, pos)
    def getEvents(self, elements={}):
        """Return a dict of window driven events."""
        for event in [pg.event.wait()] + pg.event.get():
            # closed window
            if event.type is pg.QUIT or (event.type is pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.close()
            # window resized
            if event.type is pg.VIDEORESIZE:
                self.resize(event.size)
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
                elements[each].getEvents(self.events)

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
class Surface(pg.Surface):
    """Surface template class for gui elements."""
    def __init__(self, config={}, type="surface"):
        """Constructor."""
        self.config = validateGuiConfig(config, type)
        self.size = self.config["size"]
        self.width = self.size[0]
        self.height = self.size[1]
        self.position = self.config["position"]
        self.x = self.position[0]
        self.y = self.position[1]
        pg.Surface.__init__(self, self.size)
        self.rect = self.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.resizable = self.config["resizable"]
        self.background = self.config["background"]
        self.fill(self.background)
        self.events = {
            "hover": None,
            "click": False,
            "clickedAt": None
        }
    def getEvents(self, window_events):
        """Return a dict of events."""
        mx, my = pg.mouse.get_pos()

        # hover
        collision = {"x": None, "y": None}
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
            self.reposition((mx - cl[0], my - cl[1]))

        return self.events
    def reposition(self, pos=None):
        if pos:
            self.position = pos
            self.x, self.y = pos
            self.rect.x = self.x
            self.rect.y = self.y
class Panel(Surface):
    """Create a new gui panel"""
    def __init__(self, config={}, type="panel"):
        """Constructor."""
        super().__init__(config, type)
        #print(self.config)
