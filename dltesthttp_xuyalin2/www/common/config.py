#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser

class config:

    def __init__(self, ini_file='../../config/env.ini'):
        ini_file='../../config/env.ini'
        configEnv = configparser.ConfigParser()
        configEnv.read(ini_file)
        self.envName = configEnv['ENV']['env']
        self.confighttp = self.getConfig(envName=self.envName, iniName='../../config/http_config.ini')
        self.configServer = self.getConfig(envName=self.envName, iniName='../../config/server_config.ini')
        self.configDB = self.getConfig(envName=self.envName, iniName='../../config/db_config.ini')



    def getConfig(self, envName, iniName):
        config = configparser.ConfigParser()
        config.read(iniName)
        keys = config.options(envName)
        values = []
        for i in range(0, len(keys)):
            values.append(config.get(envName, keys[i]))
        from other import Dict
        return Dict(keys, values)

