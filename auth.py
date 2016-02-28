import xbmc, xbmcaddon, xbmcgui, json, requests, base64

addon = xbmcaddon.Addon("service.auto3dmodesony")
TvIP = addon.getSetting("tvip")

requrl = 'http://%s/sony/accessControl' % TvIP
reqBody = {
    "id":8,
    "method":"actRegister",
    "version":"1.0",
    "params":[{"clientid":"Kodi","nickname":"Kodi","level":"private"},[{"clientid":"Kodi","value":"yes","nickname":"Kodi","function":"WOL"}]]
    };
reqHeaders = {
    'User-Agent' : 'Kodi',
    'Content-Type': 'application/json'
    };

r = requests.post(requrl, data = json.dumps(reqBody), headers = reqHeaders)
pincode = xbmcgui.Dialog().input('Enter 4 digit Code displayed on TV', type=xbmcgui.INPUT_ALPHANUM)

reqHeaders['Authorization'] = 'Basic '+base64.b64encode(':'+pincode)
r = requests.post(requrl, data = json.dumps(reqBody), headers = reqHeaders)
reqKey = str(r.headers['Set-Cookie'].split("=")[1].split(";")[0])
addon.setSetting("cookie", reqKey)

xbmc.log("[%s] %s" % ("SonyTV 3D AutoSwitch", "Cookie-auth-Key:" + reqKey))
