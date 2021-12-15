from PyML import Window

win = Window()
win.location.href = "http://google.com"
# fails because the parser incorrectly parses scripts that contain html inside strings
