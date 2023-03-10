import com.softalks.debuggable  # @UnusedImport
from com.softalks.kodi.addon import Setting
from com.softalks.commons import evaluable
from enum import Enum
import sys
from urllib.parse import urlencode, parse_qsl
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from com.softalks.kodi.vfs import path

class Parameter(Enum):
    pass

class Attribute(Enum):
    pass

class By(Enum):
    LABEL = xbmcplugin.SORT_METHOD_LABEL
    
class View(Enum):
    ICON_WALL = 52
    WIDE_LIST = 55

class Request:
    
    addon = xbmcaddon.Addon()
    target = sys.argv[0]
    handle = int(sys.argv[1])
    parameters = dict(parse_qsl(sys.argv[2][1:]))
    
    def __init__(self, *properties):
        storage = xbmcgui.Window(10000)
        for key in properties:
            storage.setProperty(self.target + key, None)            
        
    def synchronize(self):
        xbmc.executebuiltin(f'Container.Update({self.target},replace)')
            
    def url(self, **args):
        return '{0}?{1}'.format(self.target, urlencode(evaluable(**args)))
    
    
    def synchronized(self):
        '''A request made by the container that keeps waiting for a listing to be provided by the plugin'''
        return self.handle != -1
    
    def set(self, variable, value):
        if isinstance(variable, Attribute):
            xbmcgui.Window(10000).setProperty(self.target + variable, value)
        else:
            raise Exception('Illegal argument: variable not a com.softalks.kodi.plugin.Attribute')
        
    def get(self, variable):
        if isinstance(variable, Setting):
            return self.addon.getSetting(variable.value)
        elif isinstance(variable, Parameter):
            return self.parameters.get(variable.value)
        elif isinstance(variable, Attribute):
            return xbmcgui.Window(10000).getProperty(self.target + property)
        else:
            raise Exception('Illegal argument: variable')
        
    def getAll(self, *names):
        values = []
        for name in names:
            values.append(self.get(name))
        return *values
    
    def resolve(self, *nodes):
        xbmcplugin.setResolvedUrl(self.handle, True, xbmcgui.ListItem(path = path(nodes)))
          
class Listing:
    
    items = []
    handle = int(sys.argv[1])
    
    def __init__(self, request, avoidSingletonFolders = False):
        self.request=  request
        self.avoidSingletonBranches = avoidSingletonFolders
        
    def add(self, label, isFolder = False, timestamp = None, art = {}, selected = False, **querystring):
        if action := querystring.get('action'):
            querystring['action'] = label.name if action == True else action
        if isinstance(label, Enum):
            label = self.request.addon.getLocalizedString(label.value)
        item = {
            'label': label,
            'path': self.request.url(**querystring)
        }
        item['selected'] = selected
        item['is folder'] = isFolder
        item['date/time'] = timestamp
        item['art'] = art
        item['action'] = action
        self.items.append(item)
        
    def send(self, mode = None, cache = False, descending = False, contentType = None, *sortMethods):
        if len(self.items) == 1 and self.items[0]['leaf'] == False and self.avoidSingletonFolders:
            raise Exception('Not implemented yet: avoidSingletonFolders')
        else:
            handle = self.request.handle
            for item in self.items:
                gui = xbmcgui.ListItem(label = item['label'], path = item['path'])
                gui.setIsFolder(item['is folder'])
                gui.select(item['selected'])
                label2 = item.get('label2')
                if label2: gui.setLabel2(label2)
                timestamp = item.get('date/time')
                if timestamp: gui.setDateTime(timestamp)
                art = item['art']
                if len(art) > 0:
                    gui.setArt(art)
                xbmcplugin.addDirectoryItem(handle, gui.getPath(), gui)
            if mode:
                xbmc.executebuiltin(f'Container.SetViewMode({mode.value})')
            if not descending and xbmc.getInfoLabel('Container.SortOrder') == 'Descending':
                xbmc.executebuiltin('Container.SetSortDirection()')
            for method in sortMethods:
                xbmcplugin.addSortMethod(handle, method.value)
            if contentType:
                xbmcplugin.setContent(handle, contentType)
            xbmcplugin.setPluginCategory(handle, "To do: Managed bread crumb")
            xbmcplugin.endOfDirectory(handle, cacheToDisc = cache)