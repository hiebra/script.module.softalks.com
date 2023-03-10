from enum import Enum

import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()

class Warning(Enum):  # @ReservedAssignment
    pass

def nofity(notification):
    heading = addon.getLocalizedString(notification.value['heading'])
    message = addon.getLocalizedString(notification.value['message'])
    if isinstance(notification, Warning):
        severity = xbmcgui.NOTIFICATION_WARNING
    else:
        raise Exception('Not implemented yet')
    xbmcgui.Dialog().notification(heading, message, severity)