'''
Created on Dec 3, 2018

@author: mark
'''
import LogData
from Connection import findMyDrone
import BaseLog as log
#import problemiRiscontrati
from variablesToLog import cluster as clusterLog

if __name__ == '__main__':

    
    #log_KWArgs = {}
    #log_KWArgs['path'] = ""
    #LogData.Log(**log_KWArgs)
    
    
    #===========================================================================
    # c = findMyDrone()
    # rangeDrones = range(len(c.drones))
    # for i in rangeDrones:
    #     print(i,") - ",c.drones[i][0])
    # print("Hey" +  str(len(c.drones)))
    #===========================================================================
    
    group1 = ["g1", "v11", "v12", "v13", "t11"]
    group2 = ["g2", "v21", "v22", "v23", "t21"]
    
    listOfGroups = [group1, group2]
    
    for group in listOfGroups:
        for entry in group:
            print("Entry: " + entry)
        print()
    
    
    if(1==14):
        c = findMyDrone()
        c.scanRadioChannel()
        drone = c.get_DroneURI()
        
        strangeError = True
        while strangeError:
            try:
                log.LoggingExample(drone)
                strangeError = False
            except TypeError:
                print("Drone found: " + drone +"\n")
                print("If nothing were displayed above then your drone signal might be low")
                print("Consider recharging your drone before using it")
            
        