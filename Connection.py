'''
Created on Dec 4, 2018

@author: mark
'''

import cflib.crtp as radioChannel
import BaseLog
import time

class findMyDrone():
    '''
    Scans the radio channel and connects to a selected drone
    '''
    
    def __init__(self):
        '''
        Scans the radio channel and connects to a selected drone
        '''
        self.initializeDrivers()
        self.scanRadioChannel()
        #self.connectAndLog()
        
        
        
    def initializeDrivers(self):
        '''
        Initialize the low-level drivers (don't list the debug drivers)
        '''
        radioChannel.init_drivers(enable_debug_driver=False)
        
        
        
    def scanRadioChannel(self):
        '''
        Scan the radio channel looking for drones.
        If no drones are found, restarts the scan. Until the end of time.
        '''
        print('Scanning interfaces for Crazyflies...')
        
        numberDronesFound = 0
        restartScanIn = 1 #seconds
        while(numberDronesFound == 0):
            availableDrones = radioChannel.scan_interfaces() 
            availableDrones = self.removeDuplicatedDrones(availableDrones)
    
            numberDronesFound = len(availableDrones)
            if numberDronesFound == 0:
                print('No Crazyflies found, restarting scan...\n')
                time.sleep(restartScanIn)
            #   return self.scanRadioChannel()
        
        else:
            #Select all available drones, display them, let the user choose which to connect to
            print('Crazyflies found:', numberDronesFound)
            
            droneList = range(numberDronesFound)
            for i in droneList:
                print(i,") - ",availableDrones[i][0])

            try:
                chosen = int(input("Choose the Drone you want to connect to\n"))
            except ValueError:
                print("I know you can do better than that :)\n")
                return self.scanRadioChannel()
                
            if chosen not in droneList: #Now we need to check whether the input refers to a valid listed drone
                print("Bad choice indeed... I'll give you a second chance\n")
                return self.scanRadioChannel()
                    
            #Set the URI into the class variable droneURI
            if(availableDrones[0][int(chosen)] != "" or availableDrones[0][int(chosen)] != None):
                self.droneURI = availableDrones[0][int(chosen)]
            else:
                numberDronesFound = 0
                
                
    def connectAndLog(self):
        '''
        Connects to a drone via its URI and starts logging data
        '''
        BaseLog(self.droneURI)
    
    
                
    def removeDuplicatedDrones(self, dronesArray):
        '''
        Deletes unwanted duplicates from the available drones on the radio channel
        '''
        if len(dronesArray) == 1:
            return dronesArray
        
        sanitizeDrones = []
        unique = []
        for drone in dronesArray:
            if drone not in unique:
                sanitizeDrones.append(drone)
                unique.append(drone)
        return sanitizeDrones
                
                
                
                
                
                
                
                
                
                
                
                
                