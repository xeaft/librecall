# librecall (LibreCall)

An open-source alternative to Microsoft's "Recall" feature on Windows. Works on both Windows and Linux (WIP), with a "not official" macOS support.

Download (and run) via CLI:\
`git clone https://github.com/xeaft/librecall`\
`cd librecall`\
`python main.py`

**Auto start:**\
If you are on Liunx, specifically on a distribution using the `systemd` init system, you can run `python autorun.py` to automatically create and use librecall every time.
To remove the autorun script, you can either
1) run the `autorun.py` script with the `--remove` (or `-r`, for short) flag => `python autorun.py -r`. this will stop and disable the service, and remove the .service file from your system.
2) manually stop the service via `systemctl --user stop librecall`. To disable it, so it doesnt run again, you use the `systemctl --user disable librecall`
For other operating systems... you need to make your own form of an autorun.

**Usage (?)**:\
Run `main.py` with either `-c` or `--config` to access the settings menu\
(that would be `python main.py -c`.)
To view the timeline, use `python main.py -c` and press the `View timeline` button on the bottom

**Additionally:**\
To access your saved screenshots, go into the settings menu (2 paragraphs above) and click on the big gray "Extract screenshots" button. this will save all the screenshots to a `/ExtractedScreenshots` directory under the directory of `main.py`. _might be a setting at some point_\
All images are in `.png` format. _might be a setting at some point_\
All screenshots are saved in a sqlite3 database (`images.db`). by default, the db is located under the original directory. this can be changed inside of the config menu

*Currently supporting*:
 - Windows: default PIL screenshot (Tested on Windows 10 22H2)
 - MacOS: default PIL screenshot (Not tested)
 - Linux (Tested on Arch Linux - `6.10.3-arch1-2`):
    - X11: default PIL screenshot (Tested on [Xfce4](https://www.xfce.org/), [i3wm (i3)](https://i3wm.org/), [KDE Plasma](https://kde.org/plasma-desktop/), [Cutefish](https://cutefish-ubuntu.github.io/), [Budgie](https://buddiesofbudgie.org/), [Deepin](https://www.deepin.org/), [Enlightenment](https://www.enlightenment.org/), [Fluxbox](https://github.com/fluxbox/fluxbox), [MATE](https://mate-desktop.org/) and more from the [Arch DE wiki](https://wiki.archlinux.org/title/Desktop_environment) *([this didnt go really well](/img/des.png))*)
    - Wayland (Tested on [KDE Plasma](https://kde.org/plasma-desktop/), [GNOME](https://www.gnome.org/) and a few WMs):
        - [flameshot](https://flameshot.org/)
        - [spectacle](https://github.com/KDE/spectacle)
        - [gnome-screenshot](https://gitlab.gnome.org/GNOME/gnome-screenshot)
        - [scrot](https://github.com/resurrecting-open-source-projects/scrot)