
"""
Simple example that connects to the first Crazyflie found, logs the Stabilizer
and prints it to the console. After 10s the application disconnects and exits.
"""
import logging
import time
import Connection
import cflib.crtp  as radioChannel # noqa
from variablesToLog import cluster as clst

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie import Crazyflie
from threading import Timer
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)



class LoggingExample:
    """
    Simple logging example class that logs the Stabilizer from a supplied
    link uri and disconnects after 5s.
    """

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        if(link_uri != ""):
            self._cf = Crazyflie(rw_cache='./cache')
            
            # Connect some callbacks from the Crazyflie API
            self._cf.connected.add_callback(self._connected)
            self._cf.disconnected.add_callback(self._disconnected)
            self._cf.connection_failed.add_callback(self._connection_failed)
            self._cf.connection_lost.add_callback(self._connection_lost)
    
            print('Connecting to %s' % link_uri)
    
            # Try to connect to the Crazyflie
            self._cf.open_link(link_uri)
    
            # Variable used to keep main loop occupied until disconnect
            self.is_connected = True
            
        else:
            print("No drone provided. Going back to scan the radio channel!\n")
            return Connection.findMyDrone()





    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected to %s' % link_uri)

        
        toLog = clst(self._cf, "", -54, "stabilizer.roll", "stabilizer.yaw")
        logGroup = toLog.getLogConfiguration()
        
        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        try:
            self._cf.log.add_config(logGroup)

            # This callback will receive the data
            logGroup.data_received_cb.add_callback(self._stab_log_data)

            # This callback will be called on errors
            logGroup.error_cb.add_callback(self._stab_log_error)

            # Start the logging
            logGroup.start()
        except KeyError as e:
            print('Could not start log configuration,'
                  '{} not found in TOC'.format(str(e)))
        except AttributeError:
            print('Could not add Stabilizer log logCluster, bad configuration.')
                
                
                
        if(1==3):
            # The definition of the logconfig can be made before connecting
            self._lg_stab = LogConfig(name='Lo chiamo come cavolo mi pare', period_in_ms=1000)
            #name - Complete name of the variable in the form group.name = stabilizer.roll
            self._lg_stab.add_variable('stabilizer.roll')
            self._lg_stab.add_variable('acc.x')
            #self._lg_stab.add_variable('stabilizer.yaw', 'float')
    
            # Adding the configuration cannot be done until a Crazyflie is
            # connected, since we need to check that the variables we
            # would like to log are in the TOC.
            try:
                self._cf.log.add_config(self._lg_stab)
    
                # This callback will receive the data
                self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
    
                # This callback will be called on errors
                self._lg_stab.error_cb.add_callback(self._stab_log_error)
    
                # Start the logging
                self._lg_stab.start()
            except KeyError as e:
                print('Could not start log configuration,'
                      '{} not found in TOC'.format(str(e)))
            except AttributeError:
                print('Could not add Stabilizer log logCluster, bad configuration.')
    
    
    
            #part 2
            # The definition of the logconfig can be made before connecting
            self._lg_stab2 = LogConfig(name='prova 2', period_in_ms=700)
            #name - Complete name of the variable in the form group.name = stabilizer.roll
            self._lg_stab2.add_variable('stabilizer.yaw', 'float')
            self._lg_stab2.add_variable('acc.z', 'float')
            #self._lg_stab2.add_variable('stabilizer.yaw', 'float')
    
            # Adding the configuration cannot be done until a Crazyflie is
            # connected, since we need to check that the variables we
            # would like to log are in the TOC.
            try:
                self._cf.log.add_config(self._lg_stab2)
    
                # This callback will receive the data
                self._lg_stab2.data_received_cb.add_callback(self._stab_log_data)
    
                # This callback will be called on errors
                self._lg_stab2.error_cb.add_callback(self._stab_log_error)
    
                # Start the logging
                self._lg_stab2.start()
            except KeyError as e:
                print('Could not start log configuration,'
                      '{} not found in TOC'.format(str(e)))
            except AttributeError:
                print('Could not add Stabilizer log logCluster, bad configuration.')

        

    def _stab_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print('Error when logging %s: %s' % (logconf.name, msg))

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        print('[%d][%s]: %s' % (timestamp, logconf.name, data))

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the speficied address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.is_connected = False
        
        
    
        
    def disconnectDrone(self):
        '''
        Disconnect the drone
        '''
        self.drone.close_link()
        
        
    def delayedDisconnectDrone(self, delay):
        '''
        Disconnect the drone after a delay (in seconds)
        '''
        Timer(delay, self.drone.close_link).start()


if __name__ == '__main__':
    
    # Initialize the low-level drivers (don't list the debug drivers)
    radioChannel.init_drivers(enable_debug_driver=False)
    
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    availableDrones = radioChannel.scan_interfaces()
    numberDronesFound = int(len(availableDrones[0]) / 2)
    #numberDronesFound = availableDrones.__len__()
    
    
    myDrone = LoggingExample("")
    myDrone.is_connected = False

    #Prendi in input i droni disponibili, mostrali, fai scegliere a quale connettersi
    
    print('Crazyflies found:', numberDronesFound)
    
    for i in range(numberDronesFound):
        
        print(i,") - ",availableDrones[i][0])

        if numberDronesFound > 0:
            chosen = input("Choose the Drone you want to connect to\n")

        uriDrone = availableDrones[0][int(chosen)]
        myDrone = LoggingExample(uriDrone)
        
        if numberDronesFound == 0:
            print('No Crazyflies found, cannot run example')


    # The Crazyflie lib doesn't contain anything to keep the application alive,
    # so this is where your application should do something. In our case we
    # are just waiting until we are disconnected.


    timeWait = 0.1
    range1 = 5
    print("Il drone a cui sono connesso è: ", uriDrone)

    with SyncCrazyflie(uriDrone, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        #.param -> /usr/local/lib/python3.6/dist-packages/cflib/crazyflie/param.py
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)

        for y in range(range1):
            cf.commander.send_hover_setpoint(0, 0, 0, y/5) #vx, vy, yawRate, zDistance
            time.sleep(timeWait)

        for y in range(range1):
            cf.commander.send_hover_setpoint(0, 0, 0, (range1 - y) / 45)
            time.sleep(timeWait)

        cf.commander.send_stop_setpoint()







