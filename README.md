Boilerplate
============

To begin with, you have to create a main file. i usually call my start scripts **main.py**.

```python
import pygame_gui as gui
# gui elements
window = gui.Window()
elements = {
	"sf1": gui.Surface()
}
# main loop
while True:
	# events
	window.getEvents(elements)
	# drawing
	window.draw(elements)
	# updating
	window.update()
```
