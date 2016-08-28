# pypihomebase

Initial config: Make the following file modifications:

+---------------------------------------------+
| File: ~/.xinitrc:                           |
+---------------------------------------------+
| openbox-session                             |
|                                             |
+---------------------------------------------+
| File: ~/.config/openbox/autostart           |
+---------------------------------------------+
| python3 /path/to/pypihomebase/pi_home.py    |
| openbox --exit                              |
|                                             |
+---------------------------------------------+

Then go to ~/.bashrc and add startx just before the end
