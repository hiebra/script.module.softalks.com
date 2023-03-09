import xbmcvfs
from com.softalks.commons import startsWith, endsWith

def listDirectory(path):
    return xbmcvfs.listdir(path)

def existsPath(path):
    return xbmcvfs.exists(path)

def read(file):
    file = xbmcvfs.File(file)
    return file.read().rstrip()

def setPlot(item, plot):
    item.setInfo('video', {'plot': 'La aplicación no ha podido arrancar con normalidad. Vuelva a intentarlo una vez establecida la configuración solicitada'})

def path(*nodes):
    path = ''
    for node in nodes:
        if startsWith('/', node):
            node = node[1:]
        if endsWith('/', node):
            node = node[:-1]
        path += '/' + node
    return path