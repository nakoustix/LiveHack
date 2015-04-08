import shutil
src = "C:/Users/nAkoustix/Documents/Development/Ableton Live/LiveHack/LiveHack"
dst = "C:/ProgramData/Ableton/Live 9 Suite x64/Resources/MIDI Remote Scripts/Live Hack"
#try:
try:
    shutil.rmtree(dst)
    print("Dir already existed...")
except:
    print("Dir has to be created...")
try:
    shutil.copytree(src, dst)
    print("Success!")
except Exception as e:
    print("Something went wrong!")
dst += "/__pycache__"
try:
    shutil.rmtree(dst)
    print("cache deleted")
except:
    print("no cache to delete")