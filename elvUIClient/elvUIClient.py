#! /usr/bin/env python3


#    ElvUIMacClient
#    macOS client to update ElvUI Addon for World of Warcraft
#    Tim Medley bloaf on Turalyon bloaf@medley.us
#    v0.17
#    3/7/2018
#    // TODO:

import logging
import platform
import subprocess
import os
from os import system
import requests
from bs4 import BeautifulSoup
import json

# setup logging to a file for testing and debugging
# change loggingLevel variable to change the debug level
# maybe add an option in the gui to toggle this?
# // TODO: add logging enable/disable to the gui

loggingLevel = logging.INFO
logging.basicConfig(filename='elvUIMacClient.log', level=loggingLevel,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class ElvUIClientApp():
    ''' client to keep the ElvUI Addon updated on macOS '''

    def getMacOSVersion(self):
        # Get current macOS version
        rawMacOSVersion = platform.mac_ver()[0]
        major = rawMacOSVersion[0:2]
        minor = rawMacOSVersion[3:5]

        # Determine "Code Name", just because. WoW only currently supports
        # macOS 10.10 through 10.13 today, so thats all I captured.
        print('major ', major)
        print('minor ', minor)
        if minor == '10':
            codeName = 'Yosemite'
        elif minor == '11':
            codeName = 'El Capitan'
        elif minor == '12':
            codeName = 'Sierra'
        elif minor == '13':
            codeName = 'High Sierra'
        macOSVersion = codeName + ' ' + rawMacOSVersion
        logging.info('macOSVersion installed: {}'.format(macOSVersion))
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
            elvUIVersion = lines[2][12:17]

            return (elvUIInstalled, elvUIVersion)
        else:
            ElvUIInstalled = False

            return elvUIInstalled

    def getReleaseElvUIVersion(self):
        # get current elvUI release version
        # initial method is to use beautiful soup and scrape the current
        # version from the website https://www.tukui.org/download.php?ui=elvui
        # this wont scale, but sorta works
        #
        #// TODO: clean this up and maybe use the gitlabs or git modules

        elvUIReleaseURL = 'https://www.tukui.org/download.php?ui=elvui#version'
        elvUIWebPage = requests.get(elvUIReleaseURL)
        soup = BeautifulSoup(elvUIWebPage.text, 'html.parser')

        versionSection = soup.find("div", class_="tab-pane fade", id="version")
        elvUIReleaseVersionRaw = versionSection.text.strip()
        elvUIReleaseVersion = elvUIReleaseVersionRaw[32:37]
        return elvUIReleaseVersion

    def upgradeElvUI(self):
        # Get the latest elvUI addon from the tukui.org website
        # remove the existing elvUI and elvUI_Config folders
        # the nice thing to do is toss them in the trash
        # worst case we can just delete them
        #
        # when finished play a cute sound
        # system('afplay ~/ElvUIClientapp/client/sounds/jobsdone.mp3')
        pass

    def tukUIAPI(self):
        # access the tukUI.org web API
        # for user and rank recognition
        #
        # baseURL='https://www.tukui.org/api.php?'

        # tukUsername=input(
        #'''\n
        # We need to log into the https: / www.tukui.org website
        # Enter your Username:
        #''')

        # tukPassword=input('Enter your Password: ')

        pass


main = ElvUIClientApp()
wowVersion = main.getWoWVersion()
macVersion = main.getMacOSVersion()
elvUIInstalledVersion = main.getElvUIInstalledVersion()
elvUIReleaseVersion = main.getReleaseElvUIVersion()

print('macOS version: ', macVersion)
print('Application version: ', wowVersion)
print('Is ElvUI Installed? ', elvUIInstalledVersion[0])
print('ElvUI Installed version: ', elvUIInstalledVersion[1])

if elvUIInstalledVersion[1] == elvUIReleaseVersion:
    print('ElvUI is up to update',
          'ElvUI Release version: ', elvUIReleaseVersion)
else:
    print('ElvUI is out of date, you should upgrade it to', elvUIReleaseVersion)
