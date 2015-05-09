import xbmc, xbmcaddon, xbmcvfs, re, httplib, os

addon = xbmcaddon.Addon("service.auto3dmodesony")
addonName = addon.getAddonInfo("name")
addonVersion = addon.getAddonInfo("version")
addonProfile = xbmc.translatePath(addon.getAddonInfo("profile"))
addonPath = xbmc.translatePath(addon.getAddonInfo("path"))
addonIcon = os.path.join(addonPath, "icon.png")

TvIP = addon.getSetting("tvip")
StartSwitch = addon.getSetting("enabled")
WaitStart = addon.getSetting("waitStart")
WaitStop = addon.getSetting("waitStop")

ButtonET = "AAAAAQAAAAEAAABlAw/Aw=="
Button3D = "AAAAAgAAAHcAAABNAw=="

KeyWaitFirst = "200"
KeyWait = "50"

SBSTags = ['.sbs.', '.hsbs.', '-hsbs-', '_sbs_', 'sbs', '-sbs', 'hsbs_']
TABTags = ['.tab.', '.htab.', '-htab-', '_tab_', 'tab', '-tab', 'htab_', 'hou', 'ou']

headers = {
    'User-Agent': 'TVSideView/2.0.1 CFNetwork/672.0.8 Darwin/14.0.0',
    'Content-Type': 'text/xml; charset=UTF-8',
    'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

def PressKey(key):
    command = "<?xml version=\"1.0\"?>" \
              + "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" \
              + "<s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>" \
              + key \
              + "</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>"
    conn = httplib.HTTPConnection( str(TvIP), port=80)
    conn.request("POST", "/sony/IRCC", command, headers=headers)
    httpResponse = conn.getresponse()

class Switcher3D(xbmc.Player) :
    def _init_ (self):
        xbmc.Player._init_(self)

    def onPlayBackStarted(self):
        if StartSwitch:
            if xbmc.Player().isPlayingVideo():
                currentPlayingFile = xbmc.Player().getPlayingFile()
                if re.search('3D', currentPlayingFile, re.I):
                    for TAG3D in TABTags:
                        if re.search(TAG3D, currentPlayingFile, re.I):
                            mode3d = "TAB"
                            break
                    for SBS3D in SBSTags:
                        if re.search(SBS3D, currentPlayingFile, re.I):
                            mode3d = "SBS"
                            break
                if not(xbmcvfs.exists(addonProfile)):
                    xbmcvfs.mkdir(addonProfile)
                file(os.path.join(addonProfile, ".3dmode"), "w").write(str(mode3d))
                xbmc.log("[%s] %s" % ("SonyTV 3D AutoSwitch", "2D --> " + mode3d))
                xbmc.sleep(int(WaitStart))
                if mode3d == "TAB":
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWaitFirst))
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWait))
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWait))
                    PressKey(ButtonET)
                else:
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWaitFirst))
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWait))
                    PressKey(ButtonET)

    def onPlayBackStopped(self):
        if StartSwitch:
            mode3d = file(os.path.join(addonProfile, ".3dmode"), "r").read()
            xbmc.log("[%s] %s" % ("SonyTV 3D AutoSwitch", mode3d + " --> 2D"))
            xbmc.sleep(int(WaitStop))
            if "TAB" in mode3d:
                PressKey(Button3D)
                xbmc.sleep(int(KeyWaitFirst))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(ButtonET)
            else:
                PressKey(Button3D)
                xbmc.sleep(int(KeyWaitFirst))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
                PressKey(ButtonET)

if __name__ == "__main__":
    xbmc.log("Starting %s v%s" % (addonName , addonVersion))
    player = Switcher3D()
    while True:
        if xbmc.abortRequested:
            break
        xbmc.sleep(500)
    xbmc.log("Stopping %s v%s" % (addonName , addonVersion))
