#Helper Functions
import os
import time
from pydub import AudioSegment
from urllib.parse import urlparse
from pathlib import Path
from slugify import slugify


# parse download link to determine provider, returns string of provider name
def parseLink(link):
    parsed_uri = urlparse(link)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    if (result == 'https://open.spotify.com/'):
        provider = 'spotify'
    elif (result == 'https://www.youtube.com/'  or result == 'https://youtu.be/'):
        provider = 'youtube'
    elif (result == 'https://soundcloud.com/' or result == 'https://m.soundcloud.com/'):
        provider = 'soundcloud'
    else:
        provider = 'none'
    return provider

def createFolderName():
    return str(round(time.time() * 1000))

def convertToWav(filePath):
    sound = AudioSegment.from_mp3(filePath)
    sound.export(filePath, format='wav')
    p = Path(filePath)
    p.rename(p.with_suffix('.wav'))


def safeFilename(fileDir, file):
    oldName = os.path.join(fileDir, file)
    newName = os.path.join(fileDir, slugify(file) + '.wav')
    os.rename(oldName, newName)
    return newName