# librecall (LibreCall)

An open-source alternative to Microsoft's "Recall" feature on Windows. Works on both Windows and Linux, with a "not official" macOS support.

### <ins>Download</ins>

<hr>

**Dependencies**\
Librecall requires 3 python dependencies to run:
- customtkinter
- pillow
- cryptography

\
Using `pip`, you can download all dependencies with either `python -m pip install -r requirements.txt`, or `python -m pip install customtkinter pillow`\
\
On Linux, you are (as always) recommended to use your package manager for system-wide packages.\
For Arch Linux you can download all dependencies with `sudo pacman -S python-pillow && yay -S python-customtkinter python-cryptography`.\
For other linux distributions.. *use your distros package manager*

Now, for the actual program, you can download it with either one of these options:
1) Download a premade bin:
    1) **For Windows**, a premade executable can be found in the [releases tab](https://github.com/xeaft/librecall/releases). This is [unsigned code](https://en.wikipedia.org/wiki/Code_signing), which *may* prompt Windows Defender and its [Smart Screen filter](https://answers.microsoft.com/en-us/windows/forum/all/i-get-the-windows-protected-your-pc-message-is-my/c4d4f9c5-43b3-42ca-a199-dd253222915b). You can, but arent forced to, press "More info" and click "Run anyways". If you do not trust this, you can build the project from source with the steps below.
    2) **For Linux (x86_64)**, a premade binary can be found in the [releases tab](https://github.com/xeaft/librecall/releases). If it doesnt work, or you dont trust it, you can build the project from source with the steps below, or use it in raw source code format (via point `3)`)
    3) *If your operating system isnt one of the 2 above, you need to use another method below.*

2) Build from source:\
    To build it from source, you will need `pyinstaller` (or some other Python packaging tools).\
    To download `pyinstaller`, you can either download it with `pip` - `python -m pip install pyinstaller`, or use your python package manager ([conda](https://docs.conda.io/en/latest/), [poetry](https://python-poetry.org/), ...). For Linux, its recommended to download the package from your distributions package manager. For Arch Linux, you use the [AUR](https://wiki.archlinux.org/title/Arch_User_Repository) with an [AUR helper](https://wiki.archlinux.org/title/AUR_helpers). With [yay](https://aur.archlinux.org/packages/yay), you use `yay -S pyinstaller`\
    \
    Now that you have pyinstaller, you need to get the location of your "customtkinter" and "PIL" package. This is going to be in your `site-packages` folder under your python install. Common locations (by which i mean "my locations") are:\
    On Windows: `C:\Users\[USERNAME]\AppData\Local\Programs\Python\Python[VERSION]\Lib\site-packages\[PACKAGE]` - **use the full path, not `%localappdata%`**\
    On Linux (system wide): `/usr/lib/python[VERSION]/site-packages/[PACKAGE]`\
    **don't blindly copy this, verify this for your environment.**\
    Universally, you can get execute `python -c "import PACKAGE; import os; print(os.path.dirname(PACKAGE.__file__))"` in your terminal. it will print the path for you.\
    \
    Now that you got your CTK and PIL paths, in your terminal, navigate to the project files and run, with your specified package paths instead of their placeholders:\
    On Windows: `pyinstaller -w -y --clean -n Librecall -D -i img/icon.ico --add-data img;img --add-data CTK_PATH:customtkinter --add-data PIL_PATH:PIL librecall.py`\
    On Linux: `pyinstaller -y --clean -n Librecall -D --add-data img:img --add-data CTK_PATH:customtkinter --add-data PIL_PATH:PIL librecall.py`

    (Troubleshooting) If you downloaded pyinstaller (via pip), but getting an error that pyinstaller wasnt found, either add it to your PATH, or use `python -m PyInstaller` instead of `pyinstaller`\
    \
    (Info) Do **not** use the `--onefile` flag, as pyinstaller will create a folder in your temp folder each time you run the program. This will make both accessing images (within the ui) and keeping configurations impossible.\
    \
    (Second variant) If you dont want to do all of this, try running the build script with `python build.py`, should work for most cases.\
    \
    Now, navigate to the newly created `dist/Librecall` folder and use the `Librecall` or `Librecall.exe` (for Windows) file.\
    \
    Keep the original file in the location that its in, and only create shortcuts/symlinks.\
    To access the librecall UI, copy the shortcut, go into its properties (Alt + Enter) and in its destination, add the `-c` flag.\
    If you are on Linux, and on a DE that doesnt have the option to do so automatically, create wrapper that runs the `librecall` bin with the "-c" flag, and make a symlink to that (or, run the `uisymlink.py` script, that *should* do everything for you).\


3) Download (and run) via CLI. minimal, but works:\
    `git clone https://github.com/xeaft/librecall`\
    `cd librecall`\
    `python librecall.py` (-c)


### <ins>Auto start:</ins>
<hr>

**Linux:**\
If you are using a distribution using the `systemd` init system, you can run `python autorun.py` to automatically create and use librecall every time.\
To remove the autorun script, you can either
1) run the `autorun.py` script with the `--remove` (or `-r`, for short) flag => `python autorun.py -r`. this will stop and disable the service, and remove the .service file from your system.
2) manually stop the service via `systemctl --user stop librecall`. To disable it, so it doesnt run again, you use the `systemctl --user disable librecall`
For other operating systems... you need to make your own form of an autorun.\

**Windows**\
For windows, you will need to use an executable. Check `Download (1)` and either download or build your executable.\
Now you have one of 2 options, either manully setup autostart with the steps below:
1) Create a shortcut for that executable
2) Open the properties of the shortcut
3) Add the `-s` flag to the destination
4) Open the `%appdata%\Microsoft\Windows\Start Menu\Programs\Startup` folder
5) Move the shortcut to that folder

Or simply, run the `autorun.py` script with `python autorun.py`

<hr>

**Usage**:\
Run `librecall.py` with either `-c` or `--config` to access the settings menu (that would be `python librecall.py -c`.)\
To view the timeline, use `python librecall.py -c` and press the `View timeline` button on the bottom

**Additional info:**\
All images are in a `png` format.\
All screenshots are saved in a sqlite3 database (`images.db`). by default, the db is located under the `data` folder under the original directory. this can be changed inside of the config menu.\
Images can be encrypted with a password if you want them to be.\
If you forget your password, there's (or shouldn't, at least) no way to get your data.\
Your unique salt and a key used for verifying your password is stored in your config file (data/settings.json). If you delete that file, you will not be able to decrypt your data.

<hr>

*Currently supporting*:
 - Windows: default PIL screenshot (Tested on Windows 10 22H2)
 - MacOS: default PIL screenshot (Not tested)
 - Linux (Tested on Arch Linux - `6.10.3-arch1-2`):
    - X11: default PIL screenshot (Tested on [Xfce4](https://www.xfce.org/), [i3wm (i3)](https://i3wm.org/), [KDE Plasma](https://kde.org/plasma-desktop/), and a lot more from the [Arch DE wiki](https://wiki.archlinux.org/title/Desktop_environment) *([this didnt go really well](/img/des.png))*)
    - Wayland (Tested on [KDE Plasma](https://kde.org/plasma-desktop/), [GNOME](https://www.gnome.org/) and a few (a whole 2) WMs.):
        - [flameshot](https://flameshot.org/)
        - [spectacle](https://github.com/KDE/spectacle)
        - [gnome-screenshot](https://gitlab.gnome.org/GNOME/gnome-screenshot)
        - [scrot](https://github.com/resurrecting-open-source-projects/scrot)
        - [grim](https://sr.ht/~emersion/grim/)
        - [grimblast](https://github.com/hyprwm/contrib/tree/main/grimblast)

\
For wayland, not all tools work under all compositors, but all mentioned compositors are supported, you just need to choose the right tool (and set it up correctly).\
Your compositor not being mentioned doesnt mean it won't work, but dont be surprised if it doesnt.\
If you have a screenshotting tool thats not supported and can provide raw data of a full monitor screenshot, feel free to open an issue or a pull request with that tool.

For xorg/x11, the default option *should* work pretty much everywhere.