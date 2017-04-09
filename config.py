import ConfigParser
import os.path


class ConfigReader:
    def __init__(self):
        pass

    def setfile(self, cfgfile):
        self.configParser = ConfigParser.ConfigParser()
        self.configParser.read(os.path.join(os.path.dirname(__file__), "config", cfgfile))

    def __read(self, moduleName, configName):
        configValue = "";
        try:
            configValue = self.configParser.get(moduleName, configName)
        except ConfigParser.NoSectionError:
            return ""
        except ConfigParser.NoOptionError:
            return ""
        return configValue

    def read(self, cfgfile, moduleName, configName):
        self.setfile(cfgfile)
        return self.__read(moduleName, configName)

    def __readAll(self, moduleName):
        moduleValues = ()
        try:
            moduleValues = self.configParser.items(moduleName)
        except ConfigParser.NoSectionError:
            return moduleValues
        except ConfigParser.NoOptionError:
            return moduleValues
        return moduleValues

    def readAll(self, cfgfile, moduleName):
        self.setfile(cfgfile)
        return self.__readAll(moduleName)

    def __readAsDic(self, moduleName):
        cfgItems = ()
        try:
            cfgItems = self.configParser.items(moduleName)
        except ConfigParser.NoSectionError:
            return {}
        except ConfigParser.NoOptionError:
            return {}
        cfgDic = {}
        for index in range(len(cfgItems)):
            cfgDic[cfgItems[index][0]] = cfgItems[index][1]
        return cfgDic

    def readAsDic(self, cfgfile, moduleName):
        self.setfile(cfgfile)
        return self.__readAsDic(moduleName)
