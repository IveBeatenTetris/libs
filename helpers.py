import inspect
import ctypes
import json
import sys
import os

def validateConfig(config, type=None):  # dict
    """Return a type based configuration to create the gui element."""
    validated_config = {}
    f = os.path.dirname(os.path.realpath(__file__)) + "\\defaults.json"
    defaults = json.loads(readFile(f))
    if config.__class__ is str:
        config = json.loads(readFile(config))

    if type is "window":

        defaults = defaults["window"]
        try:    # size
            validated_config["size"] = config["size"]
        except KeyError:
            validated_config["size"] = defaults["size"]
        try:    # caption
            validated_config["caption"] = config["caption"]
        except KeyError:
            validated_config["caption"] = defaults["caption"]
        try:    # fps
            validated_config["fps"] = config["fps"]
        except KeyError:
            validated_config["fps"] = defaults["fps"]
        try:    # background
            validated_config["background"] = config["background"]
        except KeyError:
            validated_config["background"] = defaults["background"]
        try:    # resizable
            validated_config["resizable"] = config["resizable"]
        except KeyError:
            validated_config["resizable"] = defaults["resizable"]

    if type is "pane":

        defaults = defaults["pane"]
        try:    # size
            validated_config["size"] = config["size"]
        except KeyError:
            validated_config["size"] = defaults["size"]
        try:    # position
            validated_config["position"] = config["position"]
        except KeyError:
            validated_config["position"] = defaults["position"]
        try:    # background
            validated_config["background"] = config["background"]
        except KeyError:
            validated_config["background"] = defaults["background"]
        try:    # resizable
            validated_config["resizable"] = config["resizable"]
        except KeyError:
            validated_config["resizable"] = defaults["resizable"]

    return validated_config

# directive path & file functions
def pythonPath():
    """List all entries in sys.path"""
    for each in sys.path:
        print(each)
def checkPath(path):  # bool
    """Return True if given path exists."""
    if os.path.isfile(path) or os.path.exists(path):   # bool
        return True
    else:
        return False
def readFile(path):  # str
    """Open content from file."""
    content = ""
    if os.path.isfile(path):
        with open(path) as f:
            content = ''.join(f.readlines())
    return content

# class related functions
def getPublicMethodes(obj):  # list
    """Objects public methodes."""
    method_list = []
    for each in inspect.getmembers(obj, predicate=inspect.ismethod):
        if each[0][:1] != "_":
            method_list.append(each[0])
    return method_list
def getPrivateMethodes(obj):  # list
    """Objects private properies."""
    method_list = []
    for each in inspect.getmembers(obj, predicate=inspect.ismethod):
        if each[0][:1] == "_":
            method_list.append(each[0])
    return method_list
def getBuiltinMethodes(obj):   # list
    """Objects builtin methodes."""
    method_list = []
    for each in dir(obj):
        if not callable(each):
            if each[:2] == "__" and each[-2:] == "__":
                method_list.append(each)

    return method_list
def getPublicProperties(obj):  # list
    """Objects public properies."""
    property_dict = {}
    for each in obj.__dict__:
        if each[:1] != "_":
            property_dict.update({each: obj.__dict__[each]})

    return property_dict
def getPrivateProperties(obj):  # list
    """Objects private properies."""
    property_dict = {}
    for each in obj.__dict__:
        if each[:1] == "_":
            property_dict.update({
                each: obj.__dict__[each]
            })

    return property_dict
def isMasterClass(object, masterclass):  # bool
    """Get master class fro object."""
    if object.__class__.__bases__[0] is masterclass:
        bool = True
    else:
        bool = False

    return bool
def isSubClass(object, subclass):  # bool
    """Get sub class fro object."""
    if issubclass(type(object), subclass) is True:
        bool = True
    else:
        bool = False

    return bool

# math operation
def getPercantage(parent, child):  # tuple
    """Parent = (int, int) & child = (int, int)."""
    width = 0
    height = 0
    percentage_width = None
    percentage_height = None

    # check width
    if type(child[0]) == str:
        if child[0][-1] == "%":
            percentage_width = int(child[0].split("%")[0])
            width = int(parent[0] / 100 * percentage_width)
    else:
        width = child[0]

    # check height
    if type(child[1]) == str:
        if child[1][-1] == "%":
            percentage_height = int(child[1].split("%")[0])
            height = int(parent[1] / 100 * percentage_height)
    else:
        height = child[1]

    return (width, height)

def getMachineResolution():  # tuple
    """Return full screen resolution in pixels."""
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    size = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    return size

# console operations
def start(name = ""):
    """Mark beginning process."""
    print("################# starting " + name + " #################")
    print()
def stop(name = ""):
    """Mark ending process."""
    print()
    print("################## ending " + name + " ##################")
def prettyPrint(data, sort=False, tabs=4):
    """Pretty print dict"""
    if data.__class__ is dict:
        print(json.dumps(data, sort_keys=sort, indent=tabs))
    else:
        print("Nothing to pretty-print.")
