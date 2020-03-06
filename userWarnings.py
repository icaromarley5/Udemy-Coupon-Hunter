import win32api

def alertUser(title, message):
    # handler, message, title, windowType
    win32api.MessageBox(0, message, title, 0x00001000) 