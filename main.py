# ///////////////////////
# UndertaleDRP by AntonHei
# MIT License - Copyright (c) 2020 AntonHei
# ///////////////////////

# Imports
from pypresence import Presence
import time
import configparser
import os
from os import path
import json

# General
config = configparser.ConfigParser()
drpconfig = configparser.ConfigParser()
undertaleDRPConfig = path.expandvars('config.ini')
saveGamePath = path.expandvars(r'%LOCALAPPDATA%' + r'\UNDERTALE\undertale.ini')
undertaleDataPath = path.expandvars(r'data\{language}\undertale_data.json')
undertaleTranslationPath = path.expandvars(r'data\{language}\main_translations.json')

# UNDERTALE_DRP Data
config_areaBigLogoState = False
config_discordAppClientID = ""  # Will be changed automaticaly

# UNDERTALE Data
data_kills = ""
data_roomName = ""
data_roomArea = ""
data_Name = ""
data_LV = ""
data_playtimeSeconds = ""
data_playtimeHours = ""
data_deaths = ""

# Runtime Vars
startTime = ""
refreshInterval = 10
RPC = None
undertale_data = None
undertale_translations = None
areaPicNames = None
curDetails = None
curState = None

# Config Loadup
def drpConfigLoad():
    global undertaleDataPath, undertaleTranslationPath
    drpconfig.read(undertaleDRPConfig)

    # Important data loads directly after reading
    language = str(clearString(getDRPConfigData('UndertaleDRP', 'language')).split(".")[0])
    undertaleDataPath = undertaleDataPath.replace('{language}', language)
    undertaleTranslationPath = undertaleTranslationPath.replace('{language}', language)

def loadUndertaleDataJSON():
    global undertale_data, undertale_translations

    #UndertaleDRP Data
    with open(undertaleDataPath) as f:
        undertale_data = json.load(f)

    # UndertaleDRP Translations
    with open(undertaleTranslationPath) as f:
         undertale_translations = json.load(f)

def configLoad():
    config.read(saveGamePath)

def discordInit():
    global RPC
    client_id = config_discordAppClientID
    RPC = Presence(client_id)
    RPC.connect()

def getDRPConfigData(section, dataname):
    return drpconfig[section][dataname]

def getConfigData(section, dataname):
    return config[section][dataname]

def listToDict(lst):
    op = {i: lst[i] for i in range(0, len(lst))}
    return op

def prepareData():
    global data_kills, data_roomName, data_roomArea, data_Name, data_LV, data_playtimeSeconds, data_playtimeHours, data_deaths, config_areaBigLogoState, config_discordAppClientID, areaPicNames, refreshInterval

    # Getting the UndertaleDRP Config settings
    config_areaBigLogoState = str(clearString(getDRPConfigData('UndertaleDRP', 'areaBigLogo')).split(".")[0])
    config_discordAppClientID = str(clearString(getDRPConfigData('UndertaleDRP', 'discordAppClientID')).split(".")[0])
    refreshInterval = int(clearString(getDRPConfigData('UndertaleDRP', 'refreshInterval')).split(".")[0])

    # Getting the Data

    # Discord App Area Pics
    areaPicNames = listToDict(list(undertale_data['areaDiscordAppPicNames']))

    # Rooms
    curKills = str(clearString(getConfigData('General', 'Kills')).split(".")[0])
    curRoomINT = int(clearString(getConfigData('General', 'Room')).split(".")[0])
    curName = str(clearString(getConfigData('General', 'Name')).split(".")[0])
    curLV = str(clearString(getConfigData('General', 'Love')).split(".")[0])
    curPlaytimeINT = int(clearString(getConfigData('General', 'Time')).split(".")[0])
    curDeaths = str(clearString(getConfigData('General', 'Gameover')).split(".")[0])

    # Setting the Data
    data_kills = curKills
    data_roomName = undertale_data['rooms'][curRoomINT]['Name']
    data_roomArea = undertale_data['rooms'][curRoomINT]['Area']
    data_Name = curName
    data_LV = curLV
    data_playtimeSeconds = curPlaytimeINT / 30
    data_playtimeHours = str(round(float(((curPlaytimeINT/30)/60)/60), 2)) # Calculate Frames to Seconds then to Minutes to Hours and cut off after 2 decimal places
    data_deaths = curDeaths

def clearString(str):
    str = str.replace('"', '')
    return str

def getAreaPicName(areaname):
    return areaPicNames[0][areaname]

def convertToReadable(str):
    # Location
    str = str.replace("{room_Name}", data_roomName)
    str = str.replace("{room_Area}", data_roomArea)

    # Player
    str = str.replace("{player_LV}", data_LV)
    str = str.replace("{player_kills}", data_kills)
    str = str.replace("{player_deaths}", data_deaths)
    str = str.replace("{player_name}", data_Name)

    # General
    str = str.replace("{played_time}", data_playtimeHours)

    return str

def loadTranslations():
    global curDetails, curState

    # Loading Translations
    curDetails = convertToReadable(undertale_translations['discordUI'][0]['details'])
    curState = convertToReadable(undertale_translations['discordUI'][0]['state'])

def startUpdatePresence():
    global startTime
    print("Started Rich Presence")
    startTime = time.time()-int(data_playtimeSeconds)

    # Loading Translations
    loadTranslations()

    if(config_areaBigLogoState == "True"):
        RPC.update(
            details=curDetails,
            start=time.time()-int(data_playtimeSeconds),
            large_image=getAreaPicName(data_roomArea),
            large_text=data_roomArea,
            state=curState
        )
    else:
        RPC.update(
            details=curDetails,
            start=time.time() - int(data_playtimeSeconds),
            small_image=getAreaPicName(data_roomArea),
            small_text=data_roomArea,
            large_image="undertale",
            large_text="UNDERTALE",
            state=curState
        )

def updatePresence():
    print("Updated Rich Presence")

    # Loading Translations
    loadTranslations()

    if (config_areaBigLogoState == "True"):
        RPC.update(
            details=curDetails,
            start=startTime,
            large_image=getAreaPicName(data_roomArea),
            large_text=data_roomArea,
            state=curState
        )
    else:
        RPC.update(
            details=curDetails,
            start=startTime,
            small_image=getAreaPicName(data_roomArea),
            small_text=data_roomArea,
            large_image="undertale",
            large_text="UNDERTALE",
            state=curState
        )

# Startup Discord Rich Presence
drpConfigLoad()
configLoad()
loadUndertaleDataJSON()
prepareData()
discordInit()
startUpdatePresence()

# Update Prodcedure
while True:
    time.sleep(refreshInterval)
    configLoad()
    prepareData()
    updatePresence()
