from enum import Enum
import xbmcaddon
from com.softalks.commons import evaluable

addon = xbmcaddon.Addon()

class Setting(Enum):
    pass

def thumb(file, size = None):
    images = addon.getAddonInfo('path') + 'resources/images'
    return evaluable(thumb = f'{images}/{size}/{file}' if size else file)