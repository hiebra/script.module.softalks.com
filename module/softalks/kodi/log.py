import xbmcaddon
import xbmc
class Session:
    addon = xbmcaddon.Addon()
    def __init__(self, debug = 'False', breakpoints = {}):
        self.debugging = debug and self.addon.getAddonInfo('version').endswith('-snapshot')
        self.breakpoints = breakpoints
    def info(self, event, *data):
        xbmc.log(event.format(*data), xbmc.LOGINFO)
        if self.debugging and self.breakpoint(event):
            import web_pdb; web_pdb.set_trace()  # @UnresolvedImport
    def breakpoint(self, event):
        return self.breakpoints.get(event)