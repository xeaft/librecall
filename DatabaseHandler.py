import sqlite3
import os
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

    def saveImage(self, imgBin, imgCreate):
        self.cursor.execute("INSERT INTO Images (date_created_ms, image) VALUES (?, ?)", (imgCreate, imgBin))
        self.conn.commit()

    def deleteImage(self, imageID):
        self.cursor.execute("DELETE FROM Images WHERE id = ?", (imageID,))
        self.conn.commit()

    def extractAll(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

        self.cursor.execute("SELECT id, date_created_ms, image FROM Images")
        images = cursor.fetchall()
        
        for image_id, date, blob_data in images:
            outputFP = os.path.join(dir, f"{date}_{image_id}.jpg")
            
            with open(outputFP, "wb") as file:
                file.write(blob_data)

    def getImages(self) -> list[dict]:
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