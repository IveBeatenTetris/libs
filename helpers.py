import inspect
import ctypes
import json
import sys
import os

# directive path & file functions
def pythonPath():
    """List all entries in sys.path"""
    for each in sys.path:
        print(each)
def checkPath(path):# bool
    """Return True if given path exists."""
    if os.path.isfile(path) or os.path.exists(path):# bool
        return True
    else:
        return False
def readFile(path):# str
    """Open content from file."""
    content = ""
    if os.path.isfile(path):
        with open(path) as f:
            content = ''.join(f.readlines())
    return content

# class related functions
def getPublicMethodes(obj):# list
    """Objects public methodes."""
    method_list = []
    for each in inspect.getmembers(obj, predicate=inspect.ismethod):
        if each[0][:1] != "_":
            method_list.append(each[0])
    return method_list
def getPrivateMethodes(obj):# list
    """Objects private properies."""
    method_list = []
    for each in inspect.getmembers(obj, predicate=inspect.ismethod):
        if each[0][:1] == "_":
            method_list.append(each[0])
    return method_list
def getBuiltinMethodes(obj):# list
    """Objects builtin methodes."""
    method_list = []
    for each in dir(obj):
        if not callable(each):
            if each[:2] == "__" and each[-2:] == "__":
                method_list.append(each)

    return method_list
def getPublicProperties(obj):# list
    """Objects public properies."""
    property_dict = {}
    for each in obj.__dict__:
        if each[:1] != "_":
            property_dict.update({each: obj.__dict__[each]})

    return property_dict
def getPrivateProperties(obj):# list
    """Objects private properies."""
    property_dict = {}
    for each in obj.__dict__:
        if each[:1] == "_":
            property_dict.update({
                each: obj.__dict__[each]
            })

    return property_dict
def isSubClass(object, subclass):# bool
    """Get sub class fro object."""
    if issubclass(type(object), subclass) is True:
        bool = True
    else:
        bool = False

    return bool
def isMasterClass(object, masterclass):# bool
    """Get master class from object."""
    if object.__class__.__bases__[0] is masterclass:
        bool = True
    else:
        bool = False

    return bool

# math operation
def getPercantage(parent, child):# tuple
    """Parent = (int, int) & child = (int/str, int/str)."""
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
def getAnchors(room):# dict
    """Return a dict of room's anchor point."""
    anchors = {
        "top" : 0,
        "middle" : int(room[1] / 2),
        "bottom" : room[1],
        "left" : 0,
        "center" : int(room[0] / 2),
        "right" : room[0],
        "topleft" : (0 , 0),
        "topcenter" : (int(room[0] / 2) , 0),
        "topright" : (room[0] , 0),
        "midleft" : (0 , int(room[1] / 2)),
        "midcenter" : (int(room[0] / 2) , int(room[1] / 2)),
        "midright" : (room[0] , int(room[1] / 2)),
        "bottomleft" : (0 , room[1]),
        "bottomcenter" : (int(room[0] / 2) , room[1]),
        "bottomright" : (room[0] , room[1])
    }
    return anchors
def convertAnchor(parent , child , anchor):# tuple
    """Calculate x and y trough parental sizing."""
    x , y = (0 , 0)

    if type(anchor[1]) is str:
        if anchor[1] == "top":
            y = parent["top"]
        elif anchor[1] == "middle":
            y = parent["middle"] - int(child[1] / 2)
        elif anchor[1] == "bottom":
            y = parent["bottom"] - child[1]
        elif type(anchor[1]) is int:
            y = anchor[1]
    if type(anchor[0]) is str:
        if anchor[0] == "left":
            x = parent["left"]
        elif anchor[0] == "center":
            x = parent["center"] - int(child[0] / 2)
        elif anchor[0] == "right":
            x = parent["right"] - child[0]
        elif type(anchor[0]) is int:
            x = anchor[0]

    return (x , y)

#
def getMachineResolution():# tuple
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
