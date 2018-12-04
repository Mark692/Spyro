'''
Created on Dec 3, 2018

@author: mark
'''

import time
import os


class Log():
    '''
    Creates a Logs directory in which save the log files.
    Each file is uniquely named according to titleFormat variable
    
    Optional parameters - **kwargs
    **path = (str) Choose the path where to save your logs
    '''
    
    #Sets the path to save log files
    saveIn = "./Logs/"
    
    #Determines how to entitle each log file
    titleFormat = "%Y-%m-%d - %H:%M:%S"
    
    #Enables a unique name to each new log file
    fileAlreadyExists = 0 
    
    
    
    def makeDirectory(self):
        '''
        Creates any intermediary directory without raising exceptions whether they already exist
        '''
        os.makedirs(self.saveIn, exist_ok = True)
    
    
    
    def createNewFile(self):
        '''
        Creates a new log file with a unique name
        '''
        title = self.makeTitle()
        global newLogFile #The "global" scope here will avoid errors when multiple 'IOError exceptions' occur (even though it's very difficult to happen)
        try:
            newLogFile = open(title, 'x') #'x' - create a new file and open it for writing
            
        except IOError:
            self.fileAlreadyExists += 1
            self.createNewFile()

        self.resetFAEcounter()
        self.myLogFile = newLogFile
            


    def makeTitle(self):
        '''
        Defines how to give a name to a new log file
        '''
        title = self.saveIn + time.strftime(self.titleFormat)   
        
        if(self.fileAlreadyExists == 0):
            return title
        
        return title + " (" + str(self.fileAlreadyExists) + ")"
        
        
        
    def resetFAEcounter(self):
        self.fileAlreadyExists = 0
        
        
        
    def writeNewLog(self):
        self.myLogFile.write("Mah, non saprei\n")
        self.myLogFile.write("L'ho creato in " + self.saveIn + "\n")
        
        
        
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
            if not self.saveIn is None:
                return self.sanitizeLogPath(self.saveIn) #In case it's read from file and it needs to be sanitized
        
        #Finally let's ensure to enter the specified directory
        if not userSelectedPath.endswith("/"):
            userSelectedPath += "/"
            
        #If the path is "/my/path/" it points to "ROOT/my/path/" 
        #and it will throw a Permission Error when trying to create and/or writing a new file
        if userSelectedPath.startswith("/"):
            userSelectedPath = "." + userSelectedPath
            
        self.saveIn = userSelectedPath
        
        
        
    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        self.sanitizeLogPath(kwargs['path'])
            
        self.makeDirectory()
        #self.createNewFile()
        #self.writeNewLog()
        