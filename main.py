# Imports
from pypresence import Presence
import time
import configparser
import os
from os import path
import json

# General
config = configparser.ConfigParser()
saveGamePath = path.expandvars(r'%LOCALAPPDATA%' + r'\UNDERTALE\undertale.ini')

# Discord Stuff
client_id = '123456789101112'
RPC = Presence(client_id)
RPC.connect()

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
    config.read(saveGamePath)

def getConfigData(section, dataname):
    return config[section][dataname]

def prepareData():
    global data_kills, data_roomName, data_roomArea, data_Name, data_LV, data_playtimeSeconds, data_playtimeHours, data_deaths

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

    RPC.update(
            large_image="undertale",
            details=data_roomName+" in "+data_roomArea,
            start=time.time()-int(data_playtimeSeconds),
            large_text="UNDERTALE",
            small_image=getAreaPicName(data_roomArea),
            small_text=data_roomArea,
            state="LV: "+data_LV+" with "+data_kills+" kills"
            )

def updatePresence():
    print("Updated Rich Presence")

    RPC.update(
            large_image="undertale",
            details=data_roomName+" in "+data_roomArea,
            start=startTime,
            large_text="UNDERTALE",
            small_image=getAreaPicName(data_roomArea),
            small_text=data_roomArea,
            state="LV: "+data_LV+" with "+data_kills+" kills"
            )

# Startup Discord Rich Presence
configLoad()
prepareData()
startUpdatePresence()

# Update Prodcedure
while True:
    time.sleep(10)
    configLoad()
    prepareData()
    updatePresence()
