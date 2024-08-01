# librecall (LibreCall)

An open-source alternative to Microsoft's "Recall" feature on Windows. Works on both Windows and Linux (WIP), with a "not official" macOS support.

Made primarily as a joke.

Download (and run) via CLI:\
`git clone https://github.com/xeaft/librecall`\
`cd librecall`\
`python main.py`

(maybe) i will add a systemd service at some point.

**Usage (?)**:\
run `main.py` with either `-c` or `--config` to access the settings menu\
that would be `python main.py -c`.

program is not suitable for ordinary use, as it most likely wont function very well.

**Additionally:**\
To access your saved screenshots, go into the settings menu (2 paragraphs above) and click on the big gray "Extract screenshots" button. this will save all the screenshots to a `/ExtractedScreenshots` directory under the directory of `main.py`. _might be a setting at some point_\
All images are in `.png` format. _might be a setting at some point_\
No "timeline" is available (yet).\
All screenshots are saved in a sqlite3 database (`images.db`). by default, the db is located under the original directory. this can be changed inside of the config menu