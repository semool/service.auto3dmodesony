import xbmc, xbmcaddon, xbmcgui, json, requests, base64

addon = xbmcaddon.Addon("service.auto3dmodesony")
TvIP = addon.getSetting("tvip")

reqUrl = 'http://%s/sony/accessControl' % TvIP
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

if TvIP == "0.0.0.0":
    xbmcgui.Dialog().ok(addon.getLocalizedString(30014), addon.getLocalizedString(30015))
else:
    r = requests.post(reqUrl, data = json.dumps(reqBody), headers = reqHeaders)
    pincode = xbmcgui.Dialog().input(addon.getLocalizedString(30013), type=xbmcgui.INPUT_NUMERIC)
    reqHeaders['Authorization'] = 'Basic '+base64.b64encode(':'+pincode)
    r = requests.post(reqUrl, data = json.dumps(reqBody), headers = reqHeaders)
    try:
        reqKey = str(r.headers['Set-Cookie'].split("=")[1].split(";")[0])
        addon.setSetting("cookie", reqKey)
        xbmc.log("[%s] %s" % ("SonyTV 3D AutoSwitch", "Cookie-auth-Key:" + reqKey))
    except:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30014), addon.getLocalizedString(30016))
