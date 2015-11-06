import xbmc, xbmcaddon, xbmcvfs, re, httplib, os

addon = xbmcaddon.Addon("service.auto3dmodesony")
addonName = addon.getAddonInfo("name")
addonVersion = addon.getAddonInfo("version")
addonProfile = xbmc.translatePath(addon.getAddonInfo("profile"))
addonPath = xbmc.translatePath(addon.getAddonInfo("path"))
addonIcon = os.path.join(addonPath, "icon.png")

TvIP = addon.getSetting("tvip")
TvModel = addon.getSetting("tvmodel")
cookiekey = addon.getSetting("cookie")
StartSwitch = addon.getSetting("enabled")
WaitStart = addon.getSetting("waitStart")
WaitStop = addon.getSetting("waitStop")
KeyWait = addon.getSetting("waitpress")

ButtonET = "AAAAAQAAAAEAAABlAw/Aw=="
Button3D = "AAAAAgAAAHcAAABNAw=="

KeyWaitFirst = "200"

SBSTags = ['.sbs.', '.hsbs.', '-hsbs-', '_sbs_', 'sbs', '-sbs', 'hsbs_']
TABTags = ['.tab.', '.htab.', '-htab-', '_tab_', 'tab', '-tab', 'htab_', 'hou', 'ou']

headers = {}
headers['User-Agent'] = 'TVSideView/2.0.1 CFNetwork/672.0.8 Darwin/14.0.0'
headers['Content-Type'] = 'text/xml; charset=UTF-8'
headers['SOAPACTION'] = '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Connection'] = 'keep-alive'
headers['Cookie'] = 'auth=%s' % cookiekey

def PressKey(key):
    command = "<?xml version=\"1.0\"?>" \
              + "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" \
              + "<s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>" \
              + key \
              + "</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>"
    conn = httplib.HTTPConnection( str(TvIP), port=80)
    conn.request("POST", "/sony/IRCC", command, headers=headers)
    httpResponse = conn.getresponse()

def stop3d():
    if StartSwitch:
        mode3d = file(os.path.join(addonProfile, ".3dmode"), "r").read()
        if mode3d != "":
            file(os.path.join(addonProfile, ".3dmode"), "w").write("")
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
            if TvModel == "KDL-50W805":
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
            PressKey(ButtonET)
        if "SBS" in mode3d:
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
            if TvModel == "KDL-50W805":
                PressKey(Button3D)
                xbmc.sleep(int(KeyWait))
            PressKey(ButtonET)

class Switcher3D(xbmc.Player) :
    def _init_ (self):
        xbmc.Player._init_(self)

    def onPlayBackStarted(self):
        if StartSwitch:
            if xbmc.Player().isPlayingVideo():
                currentPlayingFile = xbmc.Player().getPlayingFile()
                mode3d = ""
                if re.search('3D', currentPlayingFile, re.I):
                    for TAG3D in TABTags:
                        if re.search(TAG3D, currentPlayingFile, re.I):
                            mode3d = "TAB"
                            break
                    for SBS3D in SBSTags:
                        if re.search(SBS3D, currentPlayingFile, re.I):
                            mode3d = "SBS"
                            break
                if mode3d != "":
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
                if mode3d == "SBS":
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWaitFirst))
                    PressKey(Button3D)
                    xbmc.sleep(int(KeyWait))
                    PressKey(ButtonET)

    def onPlayBackStopped(self):
        stop3d()

    def onPlayBackEnded(self):
        stop3d()

if __name__ == "__main__":
    xbmc.log("Starting %s v%s" % (addonName , addonVersion))
    if not(xbmcvfs.exists(addonProfile)):
        xbmcvfs.mkdir(addonProfile)
    file(os.path.join(addonProfile, ".3dmode"), "w").write("")
    player = Switcher3D()
    monitor = xbmc.Monitor()
    while True:
        if monitor.waitForAbort(1):
            break
        xbmc.sleep(500)
    xbmc.log("Stopping %s v%s" % (addonName , addonVersion))
