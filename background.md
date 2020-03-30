# GNOME Desktop Backround Settings

To get the current image sizing option:
```gsettings get org.gnome.desktop.background picture-options```
To list all size options:
```gsettings range org.gnome.desktop.background picture-options```
To set one of the options:
```gsettings set org.gnome.desktop.background picture-options 'centered'```

To set the color shading options use:
```color-shading-type``` or ```primary-color``` and ```secondary-color``` followed by ```'#hex-val'```