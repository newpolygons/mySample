#Helper Functions
import os
import time
import subprocess
import shutil
from pydub import AudioSegment
from urllib.parse import urlparse
from pathlib import Path
from slugify import slugify

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'tmp')

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

def youtube(link):
    #https://github.com/yt-dlp/yt-dlp
    SONG_DIR = os.path.join(DOWNLOAD_DIR, "'%(title)s.%(ext)s'")
    subprocess.run(['yt-dlp', '-f', 'bestaudio', '--no-playlist', '--progress', '-x', '--audio-format', 'wav', '--restrict-filenames', '-o', str(SONG_DIR), str(link)])
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.wav'):
            song = safeFilename(DOWNLOAD_DIR, file)
    
    return song

def spotify(link):
    #https://github.com/spotDL/spotify-downloader
    subprocess.run(['spotdl', str(link), '--output', DOWNLOAD_DIR])
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.mp3'):
            convertToWav(os.path.join(DOWNLOAD_DIR, file))
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.wav'):
            song = safeFilename(DOWNLOAD_DIR, file)
    
    return song


def soundcloud(link):
    #https://github.com/scdl-org/scdl
    subprocess.run(['scdl', '--no-playlist', '--overwrite', '--onlymp3', '--path', str(DOWNLOAD_DIR), '-l', str(link)])
    for file in os.listdir(DOWNLOAD_DIR):
        print(file)
        if file.endswith('.mp3'):
            convertToWav(os.path.join(DOWNLOAD_DIR, file))
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.wav'):
            song = safeFilename(DOWNLOAD_DIR, file)
    
    return song

#cleans tmp folder, runs automatically on completion or if exception is found in application.
def cleanApplication():
    for i in os.listdir('tmp'):
        os.remove(os.path.join(DOWNLOAD_DIR, i))
    
    for dir in os.listdir('.'):
        if os.path.isdir('separated'):
            shutil.rmtree('separated')
    
    return

# the waiter waits for a specified time period. only called when an error has occured.
def waiter(seconds):
    print("An error has occured, waiting for " + str(seconds) + " and trying one more time.")
    time.sleep(seconds)
    print("Your meal is prepared")
    return

# responsible for stems and midi. pass it the direct path to the audio file.
def proc(song):
    head, tail = os.path.split(song)
    finalSongDir = os.path.join('music', Path(tail).stem)
    # is a better way to do this thats still safe for windows?
    try:
        Path(finalSongDir).mkdir(exist_ok=True)
        os.makedirs(os.path.join(finalSongDir, 'stems'), exist_ok=True)
        os.system('demucs -d cpu ' + str(song))
        seperatedStems = os.path.join(os.path.join('separated', 'htdemucs'), Path(tail).stem)
        os.system('basic-pitch ' + str(os.path.join(finalSongDir, 'stems')) + " " + str(os.path.join(seperatedStems, 'vocals.wav')) + " " + str(os.path.join(seperatedStems, 'other.wav')) + " " + str(os.path.join(seperatedStems, 'bass.wav')))
        os.replace(song, os.path.join(finalSongDir, tail))
        for i in os.listdir(seperatedStems):
            head, tail = os.path.split(i)
            os.replace(i, os.path.join(finalSongDir, tail))
    except Exception as e:
        print("An error has occured")
        print(str(e))
        helpers.waiter(2)
    

    