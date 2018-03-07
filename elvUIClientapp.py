
#! /usr/bin/env python3


#    ElvUIMacClient
#    macOS client to update ElvUI Addon for World of Warcraft
#    Tim Medley bloaf on Turalyon bloaf@medley.us
#    v0.15
#    3/7/2018
#    next steps:


import platform
import subprocess
import os
from os import system


class ElvUIClientApp():
    ''' client to keep the ElvUI Addon updated on macOS '''

    def getMacOSVersion(self):
        # Get current macOS version
        macOSVersion = platform.mac_ver()[0]
        return macOSVersion

    def getWoWVersion(self):
        # Grab the app version via the mac terminal command

        appDirectory = '/Applications/World\ of\ Warcraft/'
        appName = 'World\ of\ Warcraft.app'
        appLocation = appDirectory + appName

        macProcess = subprocess.Popen(
            'mdls -name kMDItemVersion ' + appLocation,
            stdout=subprocess.PIPE,
            stderr=None,
            shell=True
        )
        wowVersionRaw = macProcess.communicate()

        # convert to a string
        wowVersion = str(wowVersionRaw)
        return wowVersion[21:27]

    def getElvUIInstalledVersion(self):
        # verify elvUI is installed and get that versions
        elvDirectory = '/Applications/World of Warcraft/Interface/AddOns/ElvUI'
        elvToc = 'elvui.toc'
        elvLocation = elvDirectory + '/' + elvToc
        elvUIInstalled = ''

        if os.path.exists(elvDirectory):

            elvUIInstalled = True
            # get elvUI version from the elvui.toc file
            lines = []
            with open(elvLocation, 'rt') as elvFile:
                for line in elvFile:
                    lines.append(line)
            elvUIVersion = lines[2][12:18]

            return (elvUIInstalled, elvUIVersion)
        else:
            ElvUIInstalled = False

            return elvUIInstalled

    def getReleaseElvUIVersion():
        # get current elvUI release version
        pass

    def upgradeElvUI():
        # when finished play a cute sound
        # system('afplay ~/ElvUIClientapp/client/sounds/jobsdone.mp3')
        pass


main = ElvUIClientApp()
wowVersion = main.getWoWVersion()
macVersion = main.getMacOSVersion()
elvUIVersion = main.getElvUIInstalledVersion()


print('macOS version: ', macVersion)
print('Application version: ', wowVersion)
print('Is ElvUI Installed? ', elvUIVersion[0])
print('ElvUI Installed version: ', elvUIVersion[1])
