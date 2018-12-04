'''
Created on Dec 3, 2018

@author: mark
'''

import time
import os


class Log():
    '''
    Creates a Logs directory in which save the log files.
    Each file is uniquely named according to TITLE_FORMAT variable
    
    Optional parameters - **kwargs
    **path = (str) Choose the path where to save your logs
    '''
    
    #Sets the path to save log files
    SAVE_IN = "./Logs/"
    
    #Determines how to entitle each log file
    TITLE_FORMAT = "%Y-%m-%d - %H:%M:%S"
    
    #Enables a unique name to each new log file
    FILE_ALREADY_EXISTS = 0 
    
    
    
    def makeDirectory(self):
        '''
        Creates any intermediary directory without raising exceptions whether they already exist
        '''
        os.makedirs(self.SAVE_IN, exist_ok = True)
    
    
    
    def createNewFile(self):
        '''
        Creates a new log file with a unique name
        '''
        title = self.makeTitle()
        global newLogFile #The "global" scope here will avoid errors when multiple 'IOError exceptions' occur (even though it's very difficult to happen)
        try:
            newLogFile = open(title, 'x') #'x' - create a new file and open it for writing
            
        except IOError:
            self.FILE_ALREADY_EXISTS += 1
            self.createNewFile()

        self.FILE_ALREADY_EXISTS = 0
        self.myLogFile = newLogFile
            


    def makeTitle(self):
        '''
        Defines how to give a name to a new log file
        '''
        title = self.SAVE_IN + time.strftime(self.TITLE_FORMAT)   
        
        if(self.FILE_ALREADY_EXISTS == 0):
            return title
        
        return title + " (" + str(self.FILE_ALREADY_EXISTS) + ")"
        
        
        
    def writeNewLog(self, data):
        self.myLogFile.write(data + "\n")
        
        
        
    def sanitizeLogPath(self, userSelectedPath):
        '''
        Checks the user selected path, 
        sanitizes it from invalid characters, 
        sets it as destination path for the actual log
        '''
            
        #Sanitize the path by removing unwanted characters
        validChars = (' ', '.', '_', '/')
        userSelectedPath = "".join(userPathChar for userPathChar in userSelectedPath if userPathChar.isalnum() or userPathChar in validChars)
        
        #Trim initial spaces
        while userSelectedPath.startswith(" "):
            userSelectedPath = userSelectedPath[1:]
            
        if userSelectedPath is None or userSelectedPath == "":
            if not self.SAVE_IN is None:
                return self.sanitizeLogPath(self.SAVE_IN) #In case it's read from file and it needs to be sanitized
        
        #Finally let's ensure to enter the specified directory
        if not userSelectedPath.endswith("/"):
            userSelectedPath += "/"
            
        #If the path is "/my/path/" it points to "ROOT/my/path/" 
        #and it will throw a Permission Error when trying to create and/or writing a new file
        if userSelectedPath.startswith("/"):
            userSelectedPath = "." + userSelectedPath
            
        self.SAVE_IN = userSelectedPath
        
        
        
    def cf_log(self):
        '''
        Kinda useless right now. 
        This is just a (quick) list of locations/directories where to find information about CF logging parameters and structs
        '''
        
        parameters2Log = "crazyflie-firmware/" + "src/" + "modules/" + "src/" + "stabilizer.c"
        #LOG_GROUP_START(SomeNameToUse)
        #LOG_ADD(varType, clientDisplayedName, &actualVariableReference)
        #LOG_GROUP_STOP(SomeNameToUse)
        
        logStructDefinition = "crazyflie-firmware/" + "src/" + "modules/" + "interface/" + "log.h"
        ##define LOG_GROUP_START(NAME)  \
        #static const struct log_s __logs_##NAME[] __attribute__((section(".log." #NAME), used)) = { \
        #LOG_ADD_GROUP(LOG_GROUP | LOG_START, NAME, 0x0)
        ##define LOG_GROUP_STOP(NAME) \
        #LOG_ADD_GROUP(LOG_GROUP | LOG_STOP, stop_##NAME, 0x0) \
        #};
        #Nota 1 - "\" alla fine di ciascuna riga -> https://stackoverflow.com/questions/19405196/what-does-a-backslash-in-c-mean
        #Nota 2 - "##" corrisponde alla concatenazione di due parametri all'interno di una struct -> https://stackoverflow.com/questions/6503586/what-does-in-a-define-mean
        
        transferCvars2Python = "https://stackoverflow.com/questions/38944172/how-to-pass-variable-value-from-c-to-python"
        #cython = "https://cython.org/"
        c2python = "https://stackoverflow.com/questions/145270/calling-c-c-from-python"
        wrapC_intoPython = "https://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html"
        lastHope_butAlsoNot = "https://docs.python-guide.org/scenarios/clibs/"
        
        
        
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        self.sanitizeLogPath(kwargs['path'])
        self.makeDirectory()
        
        self.createNewFile()
        self.writeNewLog(args)
        