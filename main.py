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
RPC = None

# Others
areaPicNames = {
    "Ruinen": "ruins",
    "Snowdin": "snowdin",
    "Fehler": "error",
    "Wasserfall": "waterfall",
    "Hotland": "hotland",
    "CORE": "core",
    "Neues Zuhause": "newhome",
    "Wahres Labor": "truelab",
    "Geheim": "secret"
}

# JSON Init
with open('undertale_data.json') as f:
    undertale_data = json.load(f)

# Config Loadup
def configLoad():
    drpconfig.read(undertaleDRPConfig)
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

def prepareData():
    global data_kills, data_roomName, data_roomArea, data_Name, data_LV, data_playtimeSeconds, data_playtimeHours, data_deaths, config_areaBigLogoState, config_discordAppClientID

    # Getting the UndertaleDRP Config settings
    config_areaBigLogoState = str(clearString(getDRPConfigData('UndertaleDRP', 'areaBigLogo')).split(".")[0])
    config_discordAppClientID = str(clearString(getDRPConfigData('UndertaleDRP', 'discordAppClientID')).split(".")[0])

    # Getting the Data
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
    return areaPicNames.get(areaname)

def startUpdatePresence():
    global startTime
    print("Started Rich Presence")
    startTime = time.time()-int(data_playtimeSeconds)

    if(config_areaBigLogoState == "True"):
        RPC.update(
            details=data_roomName+" in "+data_roomArea,
            start=time.time()-int(data_playtimeSeconds),
            large_image=getAreaPicName(data_roomArea),
            large_text=data_roomArea,
            state="LV: "+data_LV+" with "+data_kills+" kills"
        )
    else:
        RPC.update(
            details=data_roomName + " in " + data_roomArea,
            start=time.time() - int(data_playtimeSeconds),
            small_image=getAreaPicName(data_roomArea),
            small_text=data_roomArea,
            large_image="undertale",
            large_text="UNDERTALE",
            state="LV: " + data_LV + " with " + data_kills + " kills"
        )

def updatePresence():
    print("Updated Rich Presence")

    if (config_areaBigLogoState == "True"):
        RPC.update(
            details=data_roomName + " in " + data_roomArea,
            start=startTime,
            large_image=getAreaPicName(data_roomArea),
            large_text=data_roomArea,
            state="LV: " + data_LV + " with " + data_kills + " kills"
        )
    else:
        RPC.update(
            details=data_roomName + " in " + data_roomArea,
            start=startTime,
            small_image=getAreaPicName(data_roomArea),
            small_text=data_roomArea,
            large_image="undertale",
            large_text="UNDERTALE",
            state="LV: " + data_LV + " with " + data_kills + " kills"
        )

# Startup Discord Rich Presence
configLoad()
prepareData()
discordInit()
startUpdatePresence()

# Update Prodcedure
while True:
    time.sleep(10)
    configLoad()
    prepareData()
    updatePresence()
