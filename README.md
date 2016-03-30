#Power View
Plugin-in to have more control over your tabbed views.
Specificly increasing and decreasing the size of them.

So far this is a super simple plugin, but it has asperations for greatness.

The current three commands are zoom in, zoom out and mega zoom.

### Zoom In
This takes the current view that has focus and makes it bigger by sqeezing the other views.

### Zoom Out
This takes the current view that has focus and makes it smaller by expanding the other views.

### Mega Zoom
This takes the current view and expands it to the edges of the window. But you don't loose the current layout. Call the command again and it puts it back.


### Calling these commands

#### Keyboard Shortcuts
I do not presume to know how you want to add these commands to you key maps but here are my suggestions. Just add these to you user keymap

```
{ "keys": ["ctrl+-"], "command": "power_view_zoom_out" },
{ "keys": ["ctrl+="], "command": "power_view_zoom_in" },
{ "keys": ["ctrl+0"], "command": "power_view_mega_zoom" },
```

#### Other
You can find the commands in the Command Palette or the menu bar under view.

Easy as Pi.