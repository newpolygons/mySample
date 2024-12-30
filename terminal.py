# CLI implementation of the project. Why bother with a frontend :)

from src import demucs, basicpitch, download, helpers


def main(theType, linkOrLocation):
    songType = theType # 'download' or 'local'
    linkOrLocation = linkOrLocation # 'link' or filePath
    if songType == 'download':
        download(linkOrLocation)
    elif songType == 'local':
        local(linkOrLocation)
    else:
        print("this shouldnt ever happen but if it does!")
        pass
    
def download(link):
    provider = helpers.parseLink(link)
    if provider == 'spotify':
        download.spotify(link)
    elif provider == 'youtube':
        download.youtube(link)
    elif provider == 'soundcloud':
        download.spotify(link)

    pass

def local(path):
    pass




if __name__ == '__main__':
    print("Running as CLI app")
    #implement sys args to determine type

