import ast
import sqlite3
import os
import passwd
from ConfigManager import ConfigManager

class DatabaseHandler:
    _insts = []

    def __new__(cls):
        if DatabaseHandler._insts:
            return DatabaseHandler._insts[0]
        
        dbHandler = super().__new__(cls)
        DatabaseHandler._insts.append(dbHandler)

        dbHandler.conn = None
        dbHandler.cursor = None
        dbHandler.configManager = ConfigManager()
        dbHandler.loc = dbHandler.configManager.get("SAVE_LOCATION")

        return dbHandler
        
    def makeConnection(self):
        self.conn = sqlite3.connect(self.loc)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_created_ms TEXT NOT NULL,
                image BLOB NOT NULL
            )
        ''')

        self.conn.commit()

    def saveImage(self, imgBin, imgCreate, nocrypt=False):
        useBin = imgBin
        useCreate = imgCreate
        if self.configManager.get("USE_PASSWORD") and not nocrypt:
            passhash = passwd.passhash
            useBin = passwd.encrypt(passhash, useBin)
            useCreate = passwd.encrypt(passhash, str(useCreate))

        self.cursor.execute("INSERT INTO Images (date_created_ms, image) VALUES (?, ?)", (useCreate, useBin))
        self.conn.commit()

    def deleteImage(self, imageID):
        self.cursor.execute("DELETE FROM Images WHERE id = ?", (imageID,))
        self.conn.commit()

    def exportAll(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

        images = self.getImages()
        
        for image in images:
            outputFP = os.path.join(dir, f"{image["date"]}_{image["id"]}.png")
            with open(outputFP, "wb") as file:
                bin = image["bin"]
                if isinstance(bin, str):
                    bin = ast.literal_eval(bin)
                file.write(bin)

    def getImages(self, nocrypt=False) -> list[dict]:
        rImages = []
        self.cursor.execute("SELECT id, date_created_ms, image FROM Images")
        images = self.cursor.fetchall()
        for image_id, date, blob_data in images:
            image = {
                "id": image_id,
                "date": date,
                "bin": blob_data
            }
            rImages.append(image)
        
        if self.configManager.get("USE_PASSWORD") and not nocrypt:
            passhash = passwd.passhash
            for img in rImages:
                img["date"] = int(passwd.decrypt(passhash, img["date"]))
                img["bin"] = passwd.decrypt(passhash, img["bin"])

        return rImages

    def deleteAll(self):
        self.cursor.execute("DROP TABLE Images")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_created_ms TEXT NOT NULL,
                image BLOB NOT NULL
            )
        ''')
        self.conn.commit()

    def endConnection(self):
        self.conn.close()

    def encryptImages(self, password, nocrypt=False):
        images = self.getImages(nocrypt)
        images.sort(key=lambda x: x["id"])
        self.deleteAll()
        for image in images:
            newImageBin = passwd.encrypt(password, image["bin"])
            newImageDate = passwd.encrypt(password, image["date"])
            self.saveImage(newImageBin, newImageDate, True)

        del images

    def decryptImages(self):
        images = self.getImages()
        self.deleteAll()
        for image in images:
            self.saveImage(image["bin"], image["date"], True)

        del images
