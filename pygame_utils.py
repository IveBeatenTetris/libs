import pygame as pg

defaults = {
  "window" : {
    "size" : (320 , 240),
    "caption" : "new window",
    "background" : (25 , 25 , 30),
    "resizable" : False,
    "fps": 10
  },
  "pane" : {
    "size" : (200 , 150),
    "background" : (255 , 255 , 255),
    "position" : (0 , 0),
    "resizable" : False
  }
}

def validateGuiConfig(config, type=None):
    """Return a type based configuration to create the gui element."""
    validated_config = {}
    if type == "Window":
        default = defaults["window"]
        try:# size
            validated_config["size"] = config["size"]
        except KeyError:
            validated_config["size"] = default["size"]
        try:# caption
            validated_config["caption"] = config["caption"]
        except KeyError:
            validated_config["caption"] = default["caption"]
        try:# background
            validated_config["background"] = config["background"]
        except KeyError:
            validated_config["background"] = default["background"]
        try:# resizable
            validated_config["resizable"] = config["resizable"]
        except KeyError:
            validated_config["resizable"] = default["resizable"]
        try:# fps
            validated_config["fps"] = config["fps"]
        except KeyError:
            validated_config["fps"] = default["fps"]

    return validated_config

class Window(object):
    """pygame window surface in a wrapper."""
    def __init__(self, config={}):
        """Constructor."""
        self.config = validateGuiConfig(config, type="Window")
        self.size = self.config["size"]
        self.caption = self.config["caption"]
        self.background = self.config["background"]
        self.resizable = self.config["resizable"]
        self.fps = self.config["fps"]
        self.display = self.__createWindow()
    def __createWindow(self):
        """Create main window element."""
        if self.resizable:
            pg.display.set_mode(self.size, pg.RESIZABLE)
        else:
            pg.display.set_mode(self.size)
        display = pg.display.get_surface()
        display.fill(self.background)
        return display
