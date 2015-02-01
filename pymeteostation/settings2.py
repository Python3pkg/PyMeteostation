from ConfigParser import SafeConfigParser
from sys import exit

def getSettings(fileName):   # returns settings dictionary made of config file
	settings = {}
	parser = SafeConfigParser()
	try:
		parser.read(fileName)
	except Exception, e:
		exit("Unable to load configuration file. Error: "+str(e))

	raw_settings = {}									# load configuration from file to variable
	for section in parser.sections():
		raw_settings[section] = {}
		for option in parser.options(section):
			raw_settings[section][option] = parser.get(section,option)

	requiredSettings = {"Meteostation": ["username","password","uploadinterval","logpath"],
					   "I2C_Device": [], "Translation_Into_POST": []}

	for section in requiredSettings.keys():			# check if required sections and options are configured
		if section in raw_settings.keys():
			for option in requiredSettings[section]:
				if not option in raw_settings[section].keys():
					exit("Unable to find \'%s\' option" % (option))
		else:
			exit("Unable to find \'%s\' section" % (section))

	settings["Translation_Into_POST"] = []			# generate translation into POST config
	for option in raw_settings["Translation_Into_POST"].keys():
		if raw_settings["Translation_Into_POST"][option] == "":
			translationListPart = ['',0]
		else:
			try:
				translationListPart = getOptionList(raw_settings["Translation_Into_POST"][option])
				if len(translationListPart) != 2:
					print "Strange value set to option \'%s\'. Using default value." % (option)
					translationListPart = ['',0]
			except:
				print "Strange value set to option \'%s\'. Using default value." % (option)
				translationListPart = ['',0]
		settings["Translation_Into_POST"].append([option,translationListPart[0],int(translationListPart[1])])

	for option in raw_settings["Meteostation"].keys():
		try:
			settings[option] = float(raw_settings["Meteostation"][option])
		except:
			settings[option] = raw_settings["Meteostation"][option]
	
	settings["I2C_configuration"] = [getI2CConfig(raw_settings,"I2C_Device")]
	return settings
"""

	options = {}
	for sectionName in ["Meteostation","I2C_Device","Translation_Into_POST"]:
		if not parser.has_section(sectionName):
			exit("Unable to find \'%s\' section" % (sectionName))
		else:
			options[sectionName] = parser.options(sectionName)

	requiedOptions = ["username","password","uploadinterval","logpath"]
	missingOptions = requiedOptions
	missingOptionsString = ""
	for requiedOptionID in range(len(requiedOptions)):
		for option in options["Meteostation"]:
			if option == requiedOptions[requiedOptionID]:
				missingOptions[requiedOptionID] = ""
				break

	for missingOption in missingOptions:
		if missingOption != "":
			missingOptionsString += "\'"+missingOption+"\', "

	if len(missingOptionsString) != 0:
		exit("Unable to find %s option(s)." % (missingOptionsString[:len(missingOptionsString)-2]))

	possibleOptions = ["username","password","uploadinterval","logpath","stationname","latitude","longitude","altitude"]
	settings = {}
	try:
		for option in possibleOptions:
			if parser.has_option("Meteostation",option):
				try:
					settings[option] = float(parser.get("Meteostation",option))
				except ValueError:
					settings[option] = parser.get("Meteostation",option)
			else:
				settings[option] = ""
		if not settings["altitude"]:
			settings["altitude"] = 0
			
		settings["I2C_configuration"] = [getI2CConfig(parser,"I2C_Device")]
			
		settings["Translation_Into_POST"] = []
		for option in options["Translation_Into_POST"]:
			if parser.get("Translation_Into_POST",option) == "":
				translationListPart = ['',0]
			else:
				try:
					translationListPart = getOptionList(parser.get("Translation_Into_POST",option))
					if len(translationListPart) != 2:
						print "Strange value set to option \'%s\'. Using default value." % (option)
						translationListPart = ['',0]
				except:
					print "Strange value set to option \'%s\'. Using default value." % (option)
					translationListPart = ['',0]
			settings["Translation_Into_POST"].append([option,translationListPart[0],int(translationListPart[1])])
	except Exception, e:
		exit("Bad format of configuration file. Error: "+str(e))
	return settings
"""
def getI2CConfig(settings,section): # recursively generates I2C configuration from configuration file
	result = {}
	for option in settings[section].keys():
		if option == "children":
			children = getOptionList(settings[section][option])
			result[option] = []
			for child in children:
				result[option].append(getI2CConfig(settings,child))
		elif option == "address":
			result[option] = int(settings[section][option],base=16)
		elif option == "channel":
			result[option] = int(settings[section][option])
		else:
			result[option] = settings[section][option]
	return result

def getOptionList(string):
	lastPosition = 0
	optionList = []
	for letterPos in range(len(string)):
		if string[letterPos] == ";":
			optionList.append(string[lastPosition:letterPos])
			lastPosition = letterPos+1
	if lastPosition < len(string):
		optionList.append(string[lastPosition:len(string)])
	return optionList