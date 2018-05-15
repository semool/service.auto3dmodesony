import xbmc, xbmcaddon, xbmcvfs, re, httplib, os, json

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
WaitStart = (int(addon.getSetting("waitStart")))
KeyWait = (int(addon.getSetting("waitpress")))
KeyWaitFirst = (int(addon.getSetting("waitfirst")))

Button3D = "AAAAAgAAAHcAAABNAw=="
ButtonET = "AAAAAgAAAJcAAABKAw=="
ButtonUP = "AAAAAgAAAJcAAABPAw=="
ButtonDN = "AAAAAgAAAJcAAABQAw=="
ButtonPL = "AAAAAgAAAJcAAAAaAw=="

if TvModel == "KDL-50W685A" or TvModel == "KD-65X8507C" or TvModel == "KDL-50W805C":
    ButtonUPDNTAB = 2
    ButtonUPDNSBS = 1
if TvModel == "KDL-50W805B":
    ButtonUPDNTAB = 3
    ButtonUPDNSBS = 2
if TvModel == "Unknown":
    ButtonUPDNTAB = (int(addon.getSetting("ButtonUPDNTAB")))
    ButtonUPDNSBS = (int(addon.getSetting("ButtonUPDNSBS")))

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

def get3dMode():
    data = json.dumps({'jsonrpc': '2.0', 'method': 'GUI.GetProperties', 'params': {'properties': ['stereoscopicmode']}, 'id': 1})
    result = json.loads(xbmc.executeJSONRPC(data))
    if not "error" in result:
        if result['result'].has_key('stereoscopicmode'):
            if result['result']['stereoscopicmode'].has_key('mode'):
                result = result['result']['stereoscopicmode']['mode'].encode('utf-8')
                if result == 'split_horizontal':
                    result = "TAB"
                elif result == 'split_vertical':
                    result = "SBS"
    return result

def getSwitch2DonStop():
    data = json.dumps({'jsonrpc': '2.0', 'method': 'Settings.GetSettingValue', 'params': {'setting':'videoplayer.quitstereomodeonstop'}, 'id': 1})
    result = json.loads(xbmc.executeJSONRPC(data))
    if not "error" in result:
        if result['result'].has_key('value'):
            if result['result']['value'] == True:
                result = "true"
            else:
                result = "false"
    return result

def runKey(mode, mode3d):
    if mode3d == "TAB":
        z = ButtonUPDNTAB
    if mode3d == "SBS":
        z = ButtonUPDNSBS
    if mode3d == "SWITCH":
        z = 1
    i = 1
    PressKey(Button3D)
    xbmc.sleep(KeyWaitFirst)
    while i <= z:
        if mode == "on":
            PressKey(ButtonDN)
        if mode == "off":
            PressKey(ButtonUP)
        if mode == "switchSBS":
            PressKey(ButtonUP)
        if mode == "switchTAB":
            PressKey(ButtonDN)
        xbmc.sleep(KeyWait)
        i = i + 1
    PressKey(ButtonET)

    # Bugfix for some Android TV's
    if mode =="on" and xbmc.Player().isPlayingVideo() == False:
        xbmc.sleep(int("1500"))
        PressKey(ButtonPL)

def start3d():
    StartSwitch = addon.getSetting("enabled")
    WaitStart = (int(addon.getSetting("waitStart")))
    if StartSwitch == "true":
        xbmc.sleep(WaitStart)
        xbmc.log("[%s] %s" % (addonName, "Checking Gui 3D Mode"))
        mode3d = get3dMode()
        mode3dcheck = file(os.path.join(addonProfile, ".3dmode"), "r").read().rstrip()
        if mode3d != mode3dcheck:
            if mode3d == "TAB" or mode3d == "SBS":
                xbmc.sleep(WaitStart)
                if mode3dcheck == "TAB":
                    mode3d = "SWITCH"
                    xbmc.log("[%s] %s" % (addonName, "TAB --> SBS"),level=xbmc.LOGNOTICE)
                    runKey("switchSBS", mode3d)
                    file(os.path.join(addonProfile, ".3dmode"), "w").write(str("SBS"))
                if mode3dcheck == "SBS":
                    mode3d = "SWITCH"
                    xbmc.log("[%s] %s" % (addonName, "SBS --> TAB"),level=xbmc.LOGNOTICE)
                    runKey("switchTAB", mode3d)
                    file(os.path.join(addonProfile, ".3dmode"), "w").write(str("TAB"))
                if mode3dcheck == "off":
                    xbmc.log("[%s] %s" % (addonName, "2D --> " + mode3d),level=xbmc.LOGNOTICE)
                    runKey("on", mode3d)
                    file(os.path.join(addonProfile, ".3dmode"), "w").write(str(mode3d))
            else:
                if mode3dcheck == "TAB" or mode3dcheck == "SBS":
                    xbmc.sleep(WaitStart)
                    xbmc.log("[%s] %s" % (addonName, mode3d + " --> 2D"),level=xbmc.LOGNOTICE)
                    runKey("off", mode3dcheck)
                file(os.path.join(addonProfile, ".3dmode"), "w").write(str("off"))

class Switcher3D(xbmc.Player) :
    def _init_ (self):
        xbmc.Player._init_(self)

    def onPlayBackStopped(self):
        if getSwitch2DonStop() == "true":
            mode3d = get3dMode()
            file(os.path.join(addonProfile, ".3dmode"), "w").write(str("off"))
            if mode3d == "TAB" or mode3d == "SBS":
                xbmc.log("[%s] %s" % (addonName, "Switching GUI to 2D"),level=xbmc.LOGNOTICE)
                xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"videoscreen.stereoscopicmode","value":0}, "id":1}')

    def onPlayBackEnded(self):
        if getSwitch2DonStop() == "true":
            mode3d = get3dMode()
            file(os.path.join(addonProfile, ".3dmode"), "w").write(str("off"))
            if mode3d == "TAB" or mode3d == "SBS":
                xbmc.log("[%s] %s" % (addonName, "Switching GUI to 2D"),level=xbmc.LOGNOTICE)
                xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"videoscreen.stereoscopicmode","value":0}, "id":1}')

if __name__ == "__main__":
    xbmc.log("[%s] Starting v%s" % (addonName , addonVersion),level=xbmc.LOGNOTICE)
    if not(xbmcvfs.exists(addonProfile)):
        xbmcvfs.mkdir(addonProfile)
    file(os.path.join(addonProfile, ".3dmode"), "w").write(str("off"))
    player = Switcher3D()
    monitor = xbmc.Monitor()
    while True:
        start3d()
        if monitor.waitForAbort(1):
            break
        xbmc.sleep(500)
    xbmc.log("[%s] Stopping v%s" % (addonName , addonVersion),level=xbmc.LOGNOTICE)
