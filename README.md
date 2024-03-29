# Nautilus Extension: Unicode Tag Columns

Tag files and folders with unicode emoji and display tags in a column.

![screenshot showing the "Emoji Tags" column in nautilus](/docs/Screenshot from 2024-03-29 11-47-42.png)

## Usage/What it does

After successful install a column "Emoji Tags" can be added in Nautilus "List View" (via "Visible Columns …" Menu). This column will display the Emoji that can be chosen in the right-click menu "Emoji Tags", when right clicking on one or more selected files or directories.

I'm personaly happy with just the color circles for my needs, but all of unicode and its emoji could be used. I'd be glad to see someone develop a concept and interface that allows for easy use and more choice of symbols..

## Dependencies

You'll need https://gitlab.gnome.org/GNOME/nautilus-python on my distribution the package name is `python-nautilus`
See also the README of nautilus-python for usage/debugging info, examples and docs.

## Install


Just use

```
$ make install
```

This will put the extension module file into `~/.local/share/nautilus-python/extensions`.

## Uninstall

```
$ make uninstall
```

## Development/Debugging

Make sure nautilus is not already running.

With `NAUTILUS_PYTHON_DEBUG=misc` you will see python output and errors in the shell output.

```
$ export NAUTILUS_PYTHON_DEBUG=misc
$ make install && nautilus
```

To reload the extension, end all Nautilus instances, wait until the prompt is available again in your shell, then do `make install && nautilus` again.


## Thanks

Started from playing with and modifying of:
 * Nautilus-Emblems-Menu-Extension
   https://github.com/allefant/Nautilus-Emblems-Menu-Extension
 * Nautilus extension: nautilus extra columns
   https://github.com/3ed/nautilus-nec
