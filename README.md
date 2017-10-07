![](https://raw.githubusercontent.com/semool/service.auto3dmodesony/master/icon.png)

##SonyTV 3D AutoSwitch

Switch your Sony 3D TV automaticly to 3D SBS/TAB Mode and back to 2D when the Kodi GUI Switch the Modes

#####Tested Models:
- Sony KDL-50W685A
- Sony KDL-50W805B
- Sony KDL-50W805C
- Sony KD-65X8507C
- Sony ??????????? - Select TV Model "Unknown" in Settings and set press UP/Down Options for SBS and Tab Mode manually

#####Authentication:
- Go to the Addon Settings, type in the TV's IP Adress and save the Settings
- Open the Settings again and select "Start Authentication with TV"
- Type in the 4 digit Code the TV will display and press OK
- When all was OK the "Cookie Authentication Key" was filled out automatically

#####When Kodi is installed directly on the TV (Android) and the remote is blocked when the TV show the Code, the Authentication Process is different:
- In the settings set TV IP to 127.0.0.1 and save
- Open the Settings again and select "Start Authentication with TV"
- Write down the 4 digit Key in a file named "kodiauth"
- Copy the file over FTP or whatever in Kodi temp dir (Android Path: /sdcard/Android/data/org.xbmc.kodi/files/.kodi/temp/)
- Now the Authentication will automatically finished