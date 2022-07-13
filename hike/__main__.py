import os
from . import initHikari
from dotenv import load_dotenv
load_dotenv()

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    initHikari().run()
