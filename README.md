Boilerplate
============

To begin with, you have to create a main file. i usually call my start scripts **main.py**.

```python
# everything pygame does, is stored in this single module
from libs import pygame_gui as gui
# this is the whole pygame app
window = gui.Window()
# main loop
while True:
	# events
	window.getEvents(elements)
	# updating
	window.update()
```
