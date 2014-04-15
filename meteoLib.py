from pymlab import config
import time, json, requests


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

    def getData(self,requestList="all"):        # returns requested sensor data
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

    def log(self,dataDict,logFileName=""):      # logging function
        if logFileName == "":
            logFileName = self.logFileName
            
        logFileName = time.strftime("%d-%m-%Y:%H-", time.localtime()) + logFileName

        try:
            with open(logFileName,"r") as f:
                pass
        except:
            self.__generateLogFile(logFileName)

        try:
            with open(logFileName,"r") as f:
                savedData = json.load(f)

            with open(logFileName,"w") as f:
                savedData.append(dataDict)
                f.write(json.dumps(savedData))
        except:
            print "Logging failed"
            
    def __generateLogFile(self,logFileName):      # generator of a log file
        defaultLog = []
        try:
            with open(logFileName,"w") as f:
                f.write(json.dumps(defaultLog))
        except:
            print "Cannot generate log file"

    def sendData(self,username,password,sendDict):      # sends data to openweathermap.com
        sendData = self.translateToPOST(sendDict)
        result = requests.post("http://openweathermap.org/data/post",auth=(username,password),data=sendData)
        JSONresult = result.json()
        if JSONresult["cod"] == "200":
            return (True,JSONresult)
        else:
            return  (False,JSONresult)

    def translateToPOST(self,sendDict):    # translates sensor values to POST request format
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
