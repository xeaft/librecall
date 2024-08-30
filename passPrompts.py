import base64
import os
import passwd
import secrets
import WindowComponents
from ConfigManager import ConfigManager
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from DatabaseHandler import DatabaseHandler
from SystemInfo import SystemInfo

sysInfo = SystemInfo()
base = WindowComponents.Base
ctk = base.ctk
backend = default_backend()
dbHandler = DatabaseHandler()
configMgr = ConfigManager()
incorrectPassAttempts = 0

def makeToplevel(window):
    if window:
        base.passPrompt = ctk.CTk()
    else:
        base.passPrompt = ctk.CTkToplevel()
    base.passPrompt.title("Librecall - Input Password")

    base.passPrompt.geometry("300x200")
    base.passPrompt.focus()
    base.passPrompt.resizable(False, False)


def passInput(firstTime=False, onSuccess=lambda:0, window=False, onQuit=lambda:0):  
    if not base.passPrompt or not base.passPrompt.winfo_exists():
        makeToplevel(window)

    title = ctk.CTkLabel(base.passPrompt, text="Input password")
    title.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

    passInput = ctk.CTkEntry(base.passPrompt, show="*", height=10, width=290)
    passInput.grid(row=1, column=0, padx=5, sticky="ew")

    def submitPass():
        global incorrectPassAttempts
        password = passInput.get()
        if len(password) < 3:
            incorrectPass.configure(text="password too short")
            return

        if firstTime:
            salt = os.urandom(16)
            configMgr.set("SALT", base64.b64encode(salt).decode("utf-8"))

        salt = configMgr.get("SALT")
        saltBytes = salt.encode("utf-8")
        passBytes = password.encode("utf-8")
        saltedPassBytes = passBytes + saltBytes
        passHash = passwd.getSHA256(saltedPassBytes)

        del password
        del passBytes

        doExit = False

        if firstTime:
            passwd.setPassword(passHash)
            dbHandler.makeConnection()
            dbHandler.encryptImages(passHash)
            dbHandler.endConnection()
            doExit = True
        else:
            valid = passwd.verifyPassword(passHash)
            if valid:
                passwd.passhash = passHash
                doExit = True
            else:
                passInput.delete(0, ctk.END)
                incorrectPassAttempts += 1
                incorrectPass.configure(text=f"incorrect password ({incorrectPassAttempts})")
                if incorrectPassAttempts >= 4:
                    close()

        if doExit:
            onSuccess()
            base.passPrompt.destroy()

    passSubmit = ctk.CTkButton(base.passPrompt, text="Submit", width=290, command=submitPass)
    passSubmit.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    
    incorrectPass = ctk.CTkLabel(base.passPrompt, text="", text_color="red", font=(None, 12))
    incorrectPass.grid(row=3, column=0, padx=5, pady=10, sticky="w")

    def close():
        onQuit()
        base.passPrompt.destroy()

    base.passPrompt.protocol("WM_DELETE_WINDOW", close)

    def enterBreak(_):
        submitPass()
        return "break"

    passInput.bind("<Return>", enterBreak)

    if window:
        base.passPrompt.mainloop()
    else:
        base.passPrompt.grab_set()

def passChange(onQuit=lambda:0):
    if not base.passPrompt or not base.passPrompt.winfo_exists():
        makeToplevel(False)

    def submitPass():
        global incorrectPassAttempts
        oldPassword = oldPassInput.get()
        newPassword = passInput.get()

        if len(oldPassword) < 3 or len(newPassword) < 3:
            incorrectPass.configure(text="password too short")
            return
        
        salt = configMgr.get("SALT")
        saltBytes = salt.encode("utf-8")
        oldPassBytes = oldPassword.encode("utf-8")
        saltedOldPassBytes = oldPassBytes + saltBytes
        oldPassHash = passwd.getSHA256(saltedOldPassBytes)

        del oldPassword
        del oldPassBytes
        del saltedOldPassBytes

        isOldPassValid = passwd.verifyPassword(oldPassHash)
        if not isOldPassValid:
            incorrectPass.configure(text="old password is incorrect")
            return
        
        newPassBytes = newPassword.encode("utf-8")
        saltedNewPassBytes = newPassBytes + saltBytes
        newPassHash = passwd.getSHA256(saltedNewPassBytes)

        del newPassBytes
        del saltedNewPassBytes
        del newPassword

        dbHandler.makeConnection()
        dbHandler.decryptImages()
        passwd.setPassword(newPassHash)
        images = dbHandler.getImages(True)
        dbHandler.encryptImages(newPassHash, True)
        dbHandler.endConnection()

        del oldPassHash
        del newPassHash
        
        base.passPrompt.destroy()

    title = ctk.CTkLabel(base.passPrompt, text="Change password")
    title.grid(row=0, column=0, padx=5, pady=10, sticky="ew", columnspan=2)

    oldPassTxt = ctk.CTkLabel(base.passPrompt, text="old pass: ")
    oldPassTxt.grid(row=1, column=0, padx=5, sticky="w")
    oldPassInput = ctk.CTkEntry(base.passPrompt, show="*", height=10)
    oldPassInput.grid(row=1, column=1, padx=5, sticky="ew")

    newPassTxt = ctk.CTkLabel(base.passPrompt, text="new pass: ")
    newPassTxt.grid(row=2, column=0, padx=5, sticky="w")
    passInput = ctk.CTkEntry(base.passPrompt, show="*", height=10, width=220)
    passInput.grid(row=2, column=1, padx=5, sticky="ew")

    passSubmit = ctk.CTkButton(base.passPrompt, text="Submit", command=submitPass)
    passSubmit.grid(row=3, column=0, padx=5, pady=10, sticky="ew", columnspan=2)
    
    incorrectPass = ctk.CTkLabel(base.passPrompt, text="", text_color="red", font=(None, 12))
    incorrectPass.grid(row=4, column=0, padx=5, pady=10, sticky="w", columnspan=2)


    def close():
        onQuit()
        base.passPrompt.destroy()

    base.passPrompt.protocol("WM_DELETE_WINDOW", close)

    def enterBreak(_):
        submitPass()
        return "break"

    passInput.bind("<Return>", enterBreak)
