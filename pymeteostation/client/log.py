import os, json, time

def makeLog(dataDict,settings):      # logging function
	logFileName = time.strftime("%Y-%m-%d:%H-", time.localtime()) + "meteoData.log"
	logFilePath = settings["logpath"] + time.strftime("%Y/", time.localtime()) + time.strftime("%m/", time.localtime()) + time.strftime("%d/", time.localtime())

	if not os.path.exists(logFilePath+logFileName):
		generateLogFile(logFileName, logFilePath)

	try:
		with open(logFilePath+logFileName,"r") as f:
			savedData = json.load(f)

		with open(logFilePath+logFileName,"w") as f:
			savedData.append(dataDict)
			f.write(json.dumps(savedData))

	except Exception, e:
		print "Logging failed:", str(e)


def generateLogFile(logFileName,logPath):      # generator of a log file
	defaultLog = []
	try:
		if not logPath == "" and not os.path.exists(logPath):
			os.makedirs(logPath)

		with open(logPath+logFileName,"w") as f:
			f.write(json.dumps(defaultLog))
	except Exception, e:
		print "Cannot generate log file:",str(e)