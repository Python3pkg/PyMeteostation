from pymlab import config
import time, json, requests
from requests.auth import HTTPBasicAuth

#### Sensor Configuration [START]#########################################
#barometer = {"name": "barometer", "type": "altimet01" , "channel": 0, }
#hum_temp = {"name": "hum_temp", "type": "sht25" , "channel": 1, }
#wind_direction = {"name": "wind_direction", "type": "mag01" , "channel": 1, }
#thermometer = {"name": "lts", "type": "lts01" , "channel": 2, }

#barometer = cfg.get_device("barometer")
#hum_temp = cfg.get_device("hum_temp")
#wind_direction = cfg.get_device("wind_direction")
#thermometer = cfg.get_device("thermometer")
#### Sensor Configuration [END]###########################################


class Meteostation:
    def __init__(self,configFileName):
        with open(configFileName) as f:
            JSONconfig = json.load(f)

        self.deviceNameList = JSONconfig["deviceNameList"]
        self.configBus = JSONconfig["configBus"]
        self.translationConfig = JSONconfig["translationConfig"]
        self.logFileName = JSONconfig["logFileName"]
	self.stationName = JSONconfig["stationName"]
	self.latitude = JSONconfig["latitude"]
	self.longitude = JSONconfig["longitude"]

        cfg = config.Config(i2c={"port":1}, bus=self.configBus)
        cfg.initialize()

        self.Devices = {}
        for device in self.deviceNameList:
            self.Devices[device] = cfg.get_device(device)

        time.sleep(0.5)

    def getData(self,requestList="all"):
        outputList = {}
        outputList["time"] = int(time.time())
        if requestList == "all":
            for device in self.Devices.keys():
                outputList[device] = self.__getSensorData(device)
        else:
            for request in requestList:
                outputList[request] = self.__getSensorData(request)

        return outputList

    def __getSensorData(self,sensorName):
        if sensorName == "hum_temp":
            self.Devices[sensorName].route()
            return {"0":self.Devices[sensorName].get_hum(),"1":self.Devices[sensorName].get_temp()}
        elif sensorName == "barometer":
            self.Devices[sensorName].route()
            data = self.Devices[sensorName].get_tp()
            return {"0":data[0],"1":data[1]/100}
        elif sensorName == "lts":
            self.Devices[sensorName].route()
            return list(self.Devices[sensorName].get_temp())

    def log(self,dataDict,logFileName=""):
        if logFileName == "":
            logFileName = self.logFileName
        try:
            with open(logFileName,"r") as f:
                pass
        except:
            self.generateLogFile(logFileName)

        try:
            with open(logFileName,"r") as f:
                savedData = json.load(f)

            with open(logFileName,"w") as f:
                savedData.append(dataDict)
                f.write(json.dumps(savedData))
        except:
            print "Logging failed"
            
    def generateLogFile(self,logFileName):
        defaultLog = []
        with open(logFileName,"w") as f:
            f.write(json.dumps(defaultLog))

    def sendData(self,username,password,sendDict):
	sendData = self.translateToPOST(sendDict)
        result = requests.post("http://openweathermap.org/data/post",auth=HTTPBasicAuth(username,password),data=sendData)
        JSONresult = result.json()
        if JSONresult["cod"] == "200":
            return (True,JSONresult)
        else:
            return  (False,JSONresult)

    def translateToPOST(self,sendDict):    # [ OWM.com name, sendDict name, sendDict name 2 ]
        payload = {}
        for itemKey in sendDict.keys():
            for transList in self.translationConfig:
                if transList[2] == "" and itemKey == transList[1]:
                    payload[transList[0]] = str(round(sendDict[itemKey],2))
                elif not transList[2] == "" and itemKey == transList[1]:
                    payload[transList[0]] = str(round(sendDict[itemKey][transList[2]],2))
	if self.stationName:
	    payload["name"] = str(self.stationName)
	if self.latitude and self.longitude:
	    payload["lat"] = str(self.latitude)
	    payload["long"] = str(self.longitude)
        return payload
