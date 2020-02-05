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
import linecache

# General
config = configparser.ConfigParser()
file0 = configparser.ConfigParser()
drpconfig = configparser.ConfigParser()
undertaleDRPConfig = path.expandvars('config.ini')
saveGamePath = path.expandvars(r'%LOCALAPPDATA%' + r'\UNDERTALE\undertale.ini')
file0GamePath = path.expandvars(r'%LOCALAPPDATA%' + r'\UNDERTALE\file0')
undertaleDataPath = path.expandvars(r'data\{language}\undertale_data.json')
undertaleTranslationPath = path.expandvars(r'data\{language}\main_translations.json')

# UNDERTALE_DRP Data
config_showCurrentRoute = True
config_discordAppClientID = ""

# UNDERTALE Data
data_kills = ""
data_roomName = ""
data_roomArea = ""
data_roomAreaCodeName = ""
data_Name = ""
data_LV = ""
data_playtimeSeconds = ""
data_playtimeHours = ""
data_deaths = ""

# file0 Data
player_kills_ruins = None
player_kills_snowdin = None
player_kills_waterfall = None
player_kills_hotland = None

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

def getfile0Line(line):
    # Decrement with 1 because arrays start at 0
    line -= 1
    try:
        return open(file0GamePath, "r").readlines()[line]
    except:
        return 0

def listToDict(lst):
    op = {i: lst[i] for i in range(0, len(lst))}
    return op

def prepareData():
    global data_kills, data_roomName, data_roomArea, data_roomAreaCodeName, data_Name, data_LV, data_playtimeSeconds, data_playtimeHours, data_deaths, config_showCurrentRoute, config_discordAppClientID, areaPicNames, refreshInterval

    # Getting the UndertaleDRP Config settings
    config_showCurrentRoute = str(clearString(getDRPConfigData('UndertaleDRP', 'showRoute')).split(".")[0])
    config_discordAppClientID = str(clearString(getDRPConfigData('UndertaleDRP', 'discordAppClientID')).split(".")[0])
    refreshInterval = int(clearString(getDRPConfigData('UndertaleDRP', 'refreshInterval')).split(".")[0])

    # Getting the Data
    # Area kills
    loadAreaKills()

    # Discord App Area Pics
    areaPicNames = listToDict(list(undertale_data['areaDiscordAppPicNames']))

    # Rooms
    curKills = str(clearString(getConfigData('General', 'Kills')).split(".")[0])
    curRoomINT = int(clearString(getConfigData('General', 'Room')).split(".")[0])
    curName = str(clearString(getConfigData('General', 'Name')).split(".")[0])
    curLV = str(clearString(getConfigData('General', 'Love')).split(".")[0])
    curPlaytimeINT = int(clearString(getConfigData('General', 'Time')).split(".")[0])
    try:
        curDeaths = str(clearString(getConfigData('General', 'Gameover')).split(".")[0])
    except:
        curDeaths = "0"


    # Setting the Data
    data_kills = curKills
    data_roomName = undertale_data['rooms'][curRoomINT]['Name']
    data_roomArea = undertale_data['rooms'][curRoomINT]['Area']
    data_roomAreaCodeName = undertale_data['rooms'][curRoomINT]['Area_codename']
    data_Name = curName
    data_LV = curLV
    data_playtimeSeconds = curPlaytimeINT / 30
    data_playtimeHours = str(round(float(((curPlaytimeINT/30)/60)/60), 2)) # Calculate Frames to Seconds then to Minutes to Hours and cut off after 2 decimal places
    data_deaths = curDeaths

def loadAreaKills():
    #file0 is being used
    global player_kills_ruins, player_kills_snowdin, player_kills_waterfall, player_kills_hotland
    player_kills_ruins = str(getfile0Line(233))
    player_kills_snowdin = str(getfile0Line(234))
    player_kills_waterfall = str(getfile0Line(235))
    player_kills_hotland = str(getfile0Line(236))

def clearString(str):
    str = str.replace('"', '')
    return str

def getAreaPicName(areaname):
    return areaPicNames[0][areaname]

def convertToReadable(str):
    # Location
    str = str.replace("{room_name}", data_roomName)
    str = str.replace("{room_area}", data_roomArea)
    str = str.replace("{room_area_code_name}", data_roomAreaCodeName)

    # Player
    str = str.replace("{player_lv}", data_LV)
    str = str.replace("{player_kills}", data_kills)
    str = str.replace("{player_deaths}", data_deaths)
    str = str.replace("{player_name}", data_Name)

    # Area Kills
    str = str.replace("{player_kills_ruins}", player_kills_ruins)
    str = str.replace("{player_kills_snowdin}", player_kills_snowdin)
    str = str.replace("{player_kills_waterfall}", player_kills_waterfall)
    str = str.replace("{player_kills_hotland}", player_kills_hotland)

    # General
    str = str.replace("{played_time}", data_playtimeHours)

    return str

def loadTranslations():
    global curDetails, curState

    # Loading Translations
    curDetails = convertToReadable(undertale_translations['discordUI'][0]['details'])
    curState = convertToReadable(undertale_translations['discordUI'][0]['state'])

# Routes: 0 - Neutral; 1 - Genocide
def caluclateCurrentRoute():
    loadAreaKills()
    ruinsNeededKills = 20
    snowdinNeededKills = 16
    waterfallNeededKills = 18
    hotlandNeededKills = 40

    if (data_roomAreaCodeName == "ruins" and int(player_kills_ruins) >= ruinsNeededKills):
        return 1
    if (data_roomAreaCodeName == "snowdin" and int(player_kills_snowdin) >= snowdinNeededKills):
        return 1
    if (data_roomAreaCodeName == "waterfall" and int(player_kills_waterfall) >= waterfallNeededKills):
        return 1
    if (data_roomAreaCodeName == "hotland" and int(player_kills_hotland) >= hotlandNeededKills):
        return 1
    return 0

def updateRPCWithRoute():
    if (caluclateCurrentRoute() == 0):
        RPC.update(
            details=curDetails,
            start=time.time() - int(data_playtimeSeconds),
            large_image=getAreaPicName(data_roomArea),
            large_text=data_roomArea,
            small_image="sans_neutral",
            small_text="Neutral Run",
            state=curState
        )
    # If Route is Genocide
    if (caluclateCurrentRoute() == 1):
        RPC.update(
            details=curDetails,
            start=time.time() - int(data_playtimeSeconds),
            large_image=getAreaPicName(data_roomArea),
            large_text=data_roomArea,
            small_image="sans_genocide",
            small_text="Genocide Run",
            state=curState
        )

def updateRPC(calcNewTime):
    #If time should be calculated or should continue
    if(calcNewTime == True):
        if (config_showCurrentRoute == "True"):
            updateRPCWithRoute()
        else:
            RPC.update(
                details=curDetails,
                start=time.time() - int(data_playtimeSeconds),
                large_image=getAreaPicName(data_roomArea),
                large_text=data_roomArea,
                state=curState
            )
    else:
        if (config_showCurrentRoute == "True"):
            updateRPCWithRoute()
        else:
            RPC.update(
                details=curDetails,
                start=startTime,
                large_image=getAreaPicName(data_roomArea),
                large_text=data_roomArea,
                state=curState
            )

def startUpdatePresence():
    global startTime
    print("Started Rich Presence")
    startTime = time.time()-int(data_playtimeSeconds)

    # Loading Translations
    loadTranslations()

    # Updates RPC with calculating a new Time
    updateRPC(True)

def updatePresence():
    print("Updated Rich Presence")

    # Loading Translations
    loadTranslations()

    # Updates RPC without calculating a new Time
    # Otherwise the Time would everytime reset to the time till the last save
    updateRPC(False)

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
