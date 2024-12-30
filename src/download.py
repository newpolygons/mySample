#functions responsible for downloading songs from different providers.
#all functions must be passed a link.
import os


DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
song = ''

def youtube(link):
    #https://github.com/yt-dlp/yt-dlp
    SONG_DIR = os.path.join(DOWNLOAD_DIR, "'%(title)s.%(ext)s'")
    
    print(os.system('yt-dlp -f bestaudio --no-playlist --progress -x --audio-format wav --restrict-filenames -o ' + SONG_DIR + " " + link))
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.wav'):
            song = helpers.safeFilename(DOWNLOAD_DIR, file)
    return song

def spotify(link):
    #https://github.com/spotDL/spotify-downloader
    
    print(os.system('spotdl ' + link + " --output " + DOWNLOAD_DIR))
    
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.mp3'):
            helpers.convertToWav(os.path.join(DOWNLOAD_DIR, file))
    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith('.wav'):
            song = helpers.safeFilename(DOWNLOAD_DIR, file)
    return song


def soundcloud(link):
    #https://github.com/scdl-org/scdl
    return

