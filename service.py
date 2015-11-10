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
WaitStop = (int(addon.getSetting("waitStop")))
KeyWait = (int(addon.getSetting("waitpress")))

ButtonET = "AAAAAQAAAAEAAABlAw/Aw=="
Button3D = "AAAAAgAAAHcAAABNAw=="

KeyWaitFirst = (int("200"))

Button3DTABon = 3
Button3DSBSon = 2
if TvModel == "0":
    Button3DTABoff = 4
    Button3DSBSoff = 5
if TvModel == "1":
    Button3DTABoff = 5
    Button3DSBSoff = 6
if TvModel == "2":
    Button3DTABon = (int(addon.getSetting("Button3DTABon")))
    Button3DSBSon = (int(addon.getSetting("Button3DSBSon")))
    Button3DTABoff = (int(addon.getSetting("Button3DTABoff")))
    Button3DSBSoff = (int(addon.getSetting("Button3DSBSoff")))

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

def runKey(mode, mode3d):
    if mode == "on":
        x = Button3DTABon
        y = Button3DSBSon
    if mode == "off":
        x = Button3DTABoff
        y = Button3DSBSoff
    if mode3d == "TAB":
        z = x
    if mode3d == "SBS":
        z = y
    i = 1
    while i <= z:
        PressKey(Button3D)
        if i == 1:
            xbmc.sleep(KeyWaitFirst)
        else:
            xbmc.sleep(KeyWait)
        i = i + 1
    PressKey(ButtonET)

def start3d():
    if StartSwitch:
        xbmc.sleep(WaitStart)
        mode3d = get3dMode()
        if mode3d == "TAB" or mode3d == "SBS":
            file(os.path.join(addonProfile, ".3dmode"), "w").write(str(mode3d))
            xbmc.log("[%s] %s" % ("SonyTV 3D AutoSwitch", "2D --> " + mode3d))
            runKey("on", mode3d)

def stop3d():
    if StartSwitch:
        xbmc.sleep(WaitStop)
        mode3d = file(os.path.join(addonProfile, ".3dmode"), "r").read()
        if mode3d == "TAB" or mode3d == "SBS":
            file(os.path.join(addonProfile, ".3dmode"), "w").write("")
            xbmc.log("[%s] %s" % ("SonyTV 3D AutoSwitch", mode3d + " --> 2D"))
            runKey("off", mode3d)

class Switcher3D(xbmc.Player) :
    def _init_ (self):
        xbmc.Player._init_(self)

    def onPlayBackStarted(self):
        start3d()

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
