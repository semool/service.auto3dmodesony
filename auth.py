import xbmc, xbmcaddon, xbmcgui, xbmcvfs, json, requests, base64, time

addon = xbmcaddon.Addon("service.auto3dmodesony")
addonName = addon.getAddonInfo("name")
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
elif TvIP == "127.0.0.1":
    dialog = xbmcgui.DialogProgressBG()
    dialog.create(addon.getLocalizedString(30017), addon.getLocalizedString(30018))
    r = requests.post(reqUrl, data = json.dumps(reqBody), headers = reqHeaders)
    Ok = False
    abort_after = 50
    start = time.time()
    while True:
        delta = time.time() - start
        x = delta * 2
        dialog.update(int(x))
        if delta >= abort_after:
            break
        if (xbmcvfs.exists("special://temp/kodiauth")):
            time.sleep(1)
            pinfile = xbmcvfs.File("special://temp/kodiauth")
            pincode = pinfile.read().rstrip()
            xbmcvfs.delete("special://temp/kodiauth")
            xbmc.log("[%s] %s" % (addonName, "Pincode in File: " + pincode),level=xbmc.LOGNOTICE)
            Ok = True
            break
    dialog.close()
    if Ok == True:
        reqHeaders['Authorization'] = 'Basic '+base64.b64encode(':'+pincode)
        r = requests.post(reqUrl, data = json.dumps(reqBody), headers = reqHeaders)
        try:
            reqKey = str(r.headers['Set-Cookie'].split("=")[1].split(";")[0])
            addon.setSetting("cookie", reqKey)
            xbmc.log("[%s] %s" % (addonName, "Cookie-auth-Key: " + reqKey),level=xbmc.LOGNOTICE)
        except:
            xbmcgui.Dialog().ok(addon.getLocalizedString(30014), addon.getLocalizedString(30016))
    else:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30014), addon.getLocalizedString(30016))
else:
    r = requests.post(reqUrl, data = json.dumps(reqBody), headers = reqHeaders)
    pincode = xbmcgui.Dialog().input(addon.getLocalizedString(30013), type=xbmcgui.INPUT_NUMERIC)
    reqHeaders['Authorization'] = 'Basic '+base64.b64encode(':'+pincode)
    r = requests.post(reqUrl, data = json.dumps(reqBody), headers = reqHeaders)
    try:
        reqKey = str(r.headers['Set-Cookie'].split("=")[1].split(";")[0])
        addon.setSetting("cookie", reqKey)
        xbmc.log("[%s] %s" % (addonName, "Cookie-auth-Key: " + reqKey),level=xbmc.LOGNOTICE)
    except:
        xbmcgui.Dialog().ok(addon.getLocalizedString(30014), addon.getLocalizedString(30016))
