'''
Created on Jan 24, 2019

@author: mark
'''
from cflib.crazyflie import Commander, Crazyflie

#===============================================================================
# Esempi di utilizzo per la classe Crazyflie
#
# crazyOMG = Crazyflie().open_link("Link URI")
# crazyOMG = Crazyflie().close_link()
#===============================================================================

#===============================================================================
# Esempi di utilizzo per la classe Commander
#
# crazyflieOBJ = Crazyflie()
# commander = Commander(crazyflieOBJ)
# flightType1 = commander.send_setpoint(self, roll, pitch, yaw, thrust)
# flightType2 = commander.send_velocity_world_setpoint(self, vx, vy, vz, yawrate)
# flightType3 = commander.send_zdistance_setpoint(self, roll, pitch, yawrate, zdistance)
# flightType4 = commander.send_hover_setpoint(self, vx, vy, yawrate, zdistance)
#===============================================================================


flightTypes = [
                "None",
                "send_setpoint",
                "send_velocity_world_setpoint",
                "send_zdistance_setpoint",
                "send_hover_setpoint"
              ]



flightVars = [
                ["roll",     "deg"],        #0
                ["pitch",    "deg"],        #1
                ["yaw",      "deg"],        #2
                ["thrust",   "[0, 65535]"], #3
                ["vx",       "m/s"],        #4
                ["vy",       "m/s"],        #5
                ["vz",       "m/s"],        #6
                ["yawrate",  "deg/s"],      #7
                ["zdistance","m"]           #8
              ]