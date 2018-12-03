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
    '''
    
    #Sets the path to save log files
    saveIn = "./Logs/"
    
    #Determines how to entitle each log file
    titleFormat = "%Y-%m-%d - %H:%M:%S"
    
    #Enables a unique name to each new log file
    fileAlreadyExists = 0 
    
    
    
    def createNewFile(self):
        '''
        Creates a new log file with a unique name
        '''
        title = self.makeTitle()
        global newLogFile
        try:
            newLogFile = open(title, 'x')
            
        except IOError:
            self.fileAlreadyExists += 1
            self.createNewFile()

        self.resetFAEcounter()
        self.myLogFile = newLogFile
    
    
    
    def makeDirectory(self):
        '''
        Creates any intermediary directory without raising exceptions whether they already exist
        '''
        os.makedirs(self.saveIn, exist_ok = True)
            


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
        
        
    def __init__(self):
        '''
        Constructor
        '''
        self.makeDirectory()
        self.createNewFile()
        self.writeNewLog()
        