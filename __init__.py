'''
Created on Dec 3, 2018

@author: mark
'''
import LogData
from Connection import findMyDrone
import BaseLog as log
#import problemiRiscontrati
from variablesToLog import cluster as clst

if __name__ == '__main__':

    
    #log_KWArgs = {}
    #log_KWArgs['path'] = ""
    #LogData.Log(**log_KWArgs)
    
    
    
    if(1==1):
        c = findMyDrone()
        drone = c.droneURI
        
        strangeError = True
        while strangeError:
            try:
                log.LoggingExample(drone)
                strangeError = False
            except TypeError:
                print("Drone found: " + drone +"\n")
                print("If nothing were displayed above then your drone signal might be low")
                print("Consider recharging your drone before using it")
            
        