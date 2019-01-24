'''
Created on Dec 5, 2018

@author: mark
'''

from cflib.crazyflie.log import LogConfig

'''
This module is a list of all the variables you may log with your CrazyFlie
'''
#Why not a class? https://stackoverflow.com/questions/5027400/constants-in-python-at-the-root-of-the-module-or-in-a-namespace-inside-the-modu

loggingVariables = "usr/local/lib/python3.6/dist-packages/cflib/crazyflie/log.py"
l4className = "LogConfig_line141"
l4funcName  = "add_variable_line164"
#self._lg_stab = LogConfig(name='Stabilizer', period_in_ms=1000)
##name - Complete name of the variable in the form group.name = stabilizer.roll
#self._lg_stab.add_variable('stabilizer.roll', 'float')


stabilizer  = ["stabilizer.roll", "stabilizer.pitch", "stabilizer.yaw"]
estimate    = ["estimate.x", "estimate.y", "estimate.z"]
 
#Add here all the possible logging groups available for the drone
dictionary = [*stabilizer, *estimate]

dictionary.insert(0, ["None"]) #Initial default value to display


class cluster():
    '''
    Defines a group of variables to log
    '''
    
    groupName = ""
    groupBaseName = "Group "
    groupCounter = 0
    cf = None
    vars2log = None
    
    #This is the final result to add to the drone
    logCluster = None
    
    MIN_LOGGING_PERIOD = 10 #minimum time (in milliseconds) for each log
    groupLoggingPeriod = MIN_LOGGING_PERIOD
    
    def __init__(self, crazyFlieOBJ, groupName, groupLoggingPeriod, *args):
        '''
        Add new variables to log and validate user input
        
        crazyFlieOBJ          = class Crazyflie Found at: cflib.crazyflie.__init__ representing the actual drone
        groupName             = name you want to give to this log group of variables
        groupLoggingPeriod    = time (in milliseconds) for the log
        *args                 = variables you wish to log
        '''
        
        #Must provide a crazyFlie object in order to get things to work
        if(crazyFlieOBJ != None):
            
            #Only proceed if submitted at least 1 variable to log
            if(len(args) != 0):
                self.cf = crazyFlieOBJ
                self.vars2log = args
                #self.checkArgs()
                
                self.validateInput(groupName, groupLoggingPeriod)
                self.addToLog()
            else:
                print("No variables provided! Impossible to continue")
        else:
            print("No CrazyFlie object provided! Impossible to continue")
         
       
            
            
    def validateInput(self, groupName, groupLoggingPeriod):
        '''
        Validate Group Name and Logging Period
        Save validated value to class variables
        '''
        
        self.groupCounter += 1
        
        #Validate Group Name
        if(groupName == ""):
            self.groupName = self.groupBaseName + str(self.groupCounter)
        else:
            self.groupName = str(groupName)
        #print(self.groupName)
            
        #Validate LoggingPeriod
        if(groupLoggingPeriod <= self.MIN_LOGGING_PERIOD):
            self.groupLoggingPeriod = self.MIN_LOGGING_PERIOD
        else:
            self.groupLoggingPeriod = groupLoggingPeriod
        #print(self.groupLoggingPeriod)
        
        
        
    def addToLog(self):
        '''
        Add the submitted variables (*args) to the self.logCluster
        '''
        
        logGroup = LogConfig(name = self.groupName, 
                            period_in_ms = self.groupLoggingPeriod) 
        
        for var2log in self.vars2log:
            logGroup.add_variable(str(var2log))
        
        self.logCluster = logGroup



    def getLogConfiguration(self):
        '''
        Just return the ultimate configuration object
        '''
        return self.logCluster


         
         
    def checkArgs(self):
        '''
        Only for debug purposes
        '''
        print("Hai immesso " + str(len(self.vars2log)) + " args")
        i = 1
        for v in self.vars2log:
            print(str(i) + ") - " + str(v))
            i += 1 
