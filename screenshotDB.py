import sqlite3
import os
import config

conn = None
cursor = None

def makeConnection():
    global conn, cursor

    loc = config.get("SAVE_LOCATION")
    conn = sqlite3.connect(loc)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_created_ms TEXT NOT NULL,
            image BLOB NOT NULL
        )
    ''')

    conn.commit()

def saveImage(imgBin, imgCreate):
    cursor.execute("INSERT INTO Images (date_created_ms, image) VALUES (?, ?)", (imgCreate, imgBin))
    conn.commit()

def deleteImage(imageID):
    cursor.execute("DELETE FROM Images WHERE id = ?", (imageID,))
    conn.commit()

def extractAll(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

    cursor.execute("SELECT id, date_created_ms, image FROM Images")
    images = cursor.fetchall()
    
    for image_id, date, blob_data in images:
        outputFP = os.path.join(dir, f"{date}_{image_id}.jpg")
        
        with open(outputFP, "wb") as file:
            file.write(blob_data)

def getImages() -> list[dict]:
    rImages = []
    cursor.execute("SELECT id, date_created_ms, image FROM Images")
    images = cursor.fetchall()
    for image_id, date, blob_data in images:
        image = {
            "id": image_id,
            "date": date,
            "bin": blob_data
        }
        rImages.append(image)
    return rImages

def deleteAll():
    cursor.execute("DROP TABLE Images")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_created_ms TEXT NOT NULL,
            image BLOB NOT NULL
        )
    ''')
    conn.commit()

def end():
    conn.close()