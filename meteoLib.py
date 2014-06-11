from pymlab import config
import time, json, requests, sys, os


class Meteostation:
    def __init__(self,configFileName):
        with open(configFileName) as f:     #  ["configBus", "translationConfig", "logPath",
            self.settings = json.load(f)    #   "stationName", "latitude", "longitude", "altitude"]

        try:
            cfg = config.Config(i2c={"port":1}, bus=self.settings["busConfig"])
            cfg.initialize()

            self.NameTypeDict = self.__getTypes(self.settings["busConfig"])

            self.Devices = {}
            for device in self.__getNames(self.settings["busConfig"]):
                self.Devices[device] = cfg.get_device(device)
        except Exception, e:
            sys.exit("Initialization of I2c failed: "+str(e))

        time.sleep(0.5)

    def getData(self,requestList="all"):        # returns requested sensor data
        outputList = {}
        outputList["time"] = int(time.time())
        if requestList == "all":
            for device in self.Devices.keys():
                outputList[device] = self.__getSensorData(device,self.NameTypeDict[device])
        else:
            for request in requestList:
                outputList[request] = self.__getSensorData(request,self.NameTypeDict[device])

        return outputList

    def __getSensorData(self,sensorName,sensorType):       # must return list
        try:
            if sensorType == "sht25":
                self.Devices[sensorName].route()
                return [self.Devices[sensorName].get_hum(),self.Devices[sensorName].get_temp()]
            elif sensorType == "altimet01":     # returns atmospheric pressure readings corrected to sea level altitude.
                self.Devices[sensorName].route()
                data = self.Devices[sensorName].get_tp()
                return [data[0],data[1]/((1-((0.0065*self.settings["altitude"])/288.15))**5.255781292873008*100)]
        except Exception, e:
            print sensorName + " sensor error:",str(e)
            return ["error",str(e)]

    def log(self,dataDict,logFileName=""):      # logging function
        if logFileName == "":
            logFileName = time.strftime("%Y-%m-%d:%H-", time.localtime()) + "meteoData.log"
            FULLlogFileName = self.settings["logPath"] + logFileName

        if not os.path.exists(FULLlogFileName):
            self.__generateLogFile(logFileName,self.settings["logPath"])

        try:
            with open(FULLlogFileName,"r") as f:
                savedData = json.load(f)

            with open(FULLlogFileName,"w") as f:
                savedData.append(dataDict)
                f.write(json.dumps(savedData))
        except Exception, e:
            print "Logging failed:", str(e)
            
    def __generateLogFile(self,logFileName,logPath):      # generator of a log file
        defaultLog = []
        try:
            if not logPath == "" and not os.path.exists(logPath):
                os.makedirs(logPath)

            with open(logPath+logFileName,"w") as f:
                f.write(json.dumps(defaultLog))
        except Exception, e:
            print "Cannot generate log file:",str(e)

    def sendData(self,username,password,sendDict):      # sends data to openweathermap.com
        sendData = self.translateToPOST(sendDict)
        try:
            result = requests.post("http://openweathermap.org/data/post",auth=(username,password),data=sendData)
            JSONresult = result.json()
        except Exception, e:
            print "Network error:",str(e)
            JSONresult = {"message":str(e),"cod":"Network error","id":"0"}

        if JSONresult["cod"] == "200":
            return (True,JSONresult)
        else:
            JSONresult["id"] = "0"
            return (False,JSONresult)

    def translateToPOST(self,sendDict):    # translates sensor values to POST request format
        payload = {}
        for itemKey in sendDict.keys():
            if not itemKey == "time" and not sendDict[itemKey][0] == "error":
                for transList in self.settings["translationConfig"]:
                    if itemKey == transList[1]:
                        payload[transList[0]] = str(round(sendDict[itemKey][transList[2]],2))

        if not type(self.settings["stationName"]) == bool:
            payload["name"] = str(self.settings["stationName"])
        if not type(self.settings["latitude"]) == bool and not type(self.settings["longitude"]) == bool:
            payload["lat"] = str(self.settings["latitude"])
            payload["long"] = str(self.settings["longitude"])
        if not type(self.settings["altitude"]) == bool:
            payload["alt"] = str(self.settings["altitude"])
        return payload

    def __getNames(self,busConfig):  # recursively searches for all "name" dictionary keys and returns their values: ["name1", "name2", ...]
        names = []
        for item in busConfig:
            for key in item.keys():
                if key == "name":
                    names.append(item[key])
                if type(item[key]) == list:
                    names += self.__getNames(item[key])
        return names

    def __getTypes(self,busConfig):  # recursively searhes for all "name" and "type" dictionary keys and return their values: {name:type, ...}
        names = {}
        for item in busConfig:
            for key in item.keys():
                if key == "name":
                    names[item[key]] = item["type"]
                if type(item[key]) == list:
                    names = dict(names.items() + self.__getTypes(item[key]).items())
        return names
