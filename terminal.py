# CLI implementation of the project. Why bother with a frontend :)
import os
import logging
from pathlib import Path
from src import helpers

logging.basicConfig(filename='mySample.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger = logging.getLogger(__name__)


def main(theType, linkOrLocation):
    songType = theType # 'download' or 'local'
    linkOrLocation = linkOrLocation # 'link' or filePath
    if songType == 'download':
        online(linkOrLocation)
    elif songType == 'local':
        local(linkOrLocation)
    else:
        print("this shouldnt ever happen but if it does!")
        pass
    
def online(link):
    provider = helpers.parseLink(link)
    if provider == 'spotify':
        try:
            song = helpers.spotify(link)
        except Exception as e:
            logger.error(e)
            print("An error has occured and been logged in the mySample.log file")
            print("Clearing some temporary files")
            helpers.cleanApplication()
            helpers.waiter(2)
    elif provider == 'youtube':
        try:
            song = helpers.youtube(link)
        except Exception as e:
            logger.error(e)
            print("An error has occured and been logged in the mySample.log file")
            print("Clearing some temporary files")
            helpers.cleanApplication()
            helpers.waiter(2)
    elif provider == 'soundcloud':
        try:
            song = helpers.soundcloud(link)
        except Exception as e:
            logger.error(e)
            print("An error has occured and been logged in the mySample.log file")
            print("Clearing some temporary files")
            helpers.cleanApplication()
            helpers.waiter(2)

    if song != None:
        helpers.proc(song)
        helpers.cleanApplication()
    return



def local(path):
    pass




if __name__ == '__main__':
    import sys
    helpers.cleanApplication()
    print('''
        
                                ____                                        ___              
                                /\  _`\                                     /\_ \             
        ___ ___     __  __    \ \,\L\_\      __       ___ ___     _____   \//\ \       __   
        /' __` __`\  /\ \/\ \    \/_\__ \    /'__`\   /' __` __`\  /\ '__`\   \ \ \    /'__`\ 
        /\ \/\ \/\ \ \ \ \_\ \     /\ \L\ \ /\ \L\.\_ /\ \/\ \/\ \ \ \ \L\ \   \_\ \_ /\  __/ 
        \ \_\ \_\ \_\ \/`____ \    \ `\____\\ \__/.\_\\ \_\ \_\ \_\ \ \ ,__/   /\____\\ \____\
        \/_/\/_/\/_/  `/___/> \    \/_____/ \/__/\/_/ \/_/\/_/\/_/  \ \ \/    \/____/ \/____/
                        /\___/                                      \ \_\                   
                        \/__/                                        \/_/                   
                                                                                                             
        Developed by: Newpolygons
    ''')


    #implement sys args to determine type

    if len(sys.argv) <= 1:
        print('Please supply either a link with "python3 terminal.py -l "https://spotify.com/song" INCLUDE THE QUOTES AROUND YOUR LINK')
        print('or')
        print('Place any local .mp3 or .wav files you want to process in the music folder and run "python3 terminal.py -f"')
    elif len(sys.argv) > 1:
        if sys.argv[1] == '-l':
            link = str(sys.argv[2])
            online(link)
        elif sys.argv[1] == '-f':
            for i in os.listdir('music'):
                if i.endswith('.wav') or i.endswith('.mp3'):
                    pass




