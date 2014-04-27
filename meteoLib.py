from pymlab import config
import time, json, requests, sys


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
        self.altitude = JSONconfig["altitude"]

        try:
            cfg = config.Config(i2c={"port":1}, bus=self.configBus)
            cfg.initialize()
            
            self.Devices = {}
            for device in self.deviceNameList:
                self.Devices[device] = cfg.get_device(device)
        except:
            sys.exit("Initialization of I2c failed")

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

    def __getSensorData(self,sensorName):       # must return dict
        try:
            if sensorName == "hum_temp":
                self.Devices[sensorName].route()
                return {"0":self.Devices[sensorName].get_hum(),"1":self.Devices[sensorName].get_temp()}
            elif sensorName == "barometer":     # returns atmospheric preassure readings corrected to sea level altitude.
                self.Devices[sensorName].route()
                data = self.Devices[sensorName].get_tp()
                return {"0":data[0],"1":data[1]/((1-((0.0065*self.altitude)/288.15))**5.255781292873008*100)}
        except:
            print sensorName + " sensor read error"
            return {"0":"error","1":"error"}

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
        try:
            result = requests.post("http://openweathermap.org/data/post",auth=(username,password),data=sendData)
            JSONresult = result.json()
        except:
            JSONresult = {"message":"Network error","cod":"Network error","id":"0"}

        if JSONresult["cod"] == "200":
            return (True,JSONresult)
        else:
            JSONresult["id"] = "0"
            return (False,JSONresult)

    def translateToPOST(self,sendDict):    # translates sensor values to POST request format
        payload = {}
        for itemKey in sendDict.keys():
            if not itemKey == "time" and not sendDict[itemKey]["0"] == "error":
                for transList in self.translationConfig:
                    if transList[2] == "" and itemKey == transList[1]:
                        payload[transList[0]] = str(round(sendDict[itemKey]["0"],2))
                    elif not transList[2] == "" and itemKey == transList[1]:
                        payload[transList[0]] = str(round(sendDict[itemKey][transList[2]],2))

        if type(self.stationName) == str and len(self.stationName) > 0:
            payload["name"] = str(self.stationName)
        if not type(self.latitude) == bool and not type(self.longitude) == bool:
            payload["lat"] = str(self.latitude)
            payload["long"] = str(self.longitude)
        if not type(self.altitude) == bool:
            payload["alt"] = str(self.altitude)
        return payload
