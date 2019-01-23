'''
Created on Oct 24, 2018
This module is dedicated to set up pages to display

@author: mark
'''
# Base graphics
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
from tkinter import ttk  # Sort of CSS for TKinter
import tkinter as tk  # Base graphics
from Connection import findMyDrone
from tkinter import StringVar, Radiobutton
import time
import threading
import BaseLog as log


# Matplotlib graphs

LARGE_FONT0 = ("Verdana", 12)
LARGE_FONT1 = ("Arial", 8)
LARGE_FONT2 = ("Times New Roman", 14)
LARGE_FONTg = ("Verdana", 22)

welcomePageLabel = "This is our Home. Forever."
welcomePageButton = "Go back home"

liveGraphLabel = "This log is amazing!"
liveGraphButton = "Live Graph!"

staticGraphLabel = "Just some boring data..."
staticGraphButton = "Look at our data"

elapsedTime = 0
connection = findMyDrone()
connection.gui_scanForDrones()
drones = connection.get_dronesList()
selectedDrone = ""

logGroups_EntryButtons = []
logGroups_Values = []

flightPointsList = []
 
def buttMessage(str2print):
    print(str2print)
    
    
class WelcomePage(tk.Frame):
    '''
    tk.Frame - Frame used to host the WelcomePage
    '''
    
    LARGE_FONT2 = ("Times New Roman", 14)
    txt_logGroups = "Log Groups"
    txt_flightPoints = "Flight Points"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=welcomePageLabel,
                         font=LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")
        
        buttonSCAN = ttk.Button(self,
                           text="Scan for drones!",
                           #command=lambda: self.findDrones(root, controller))
                           command=lambda: controller.showPage(root, droneScan))
        
        buttonSCAN.grid()
        
        
    def findDrones(self, root, controller):
        '''
        Scan the radio channel looking for drones
        '''
        drones = findMyDrone()
        self.drones = drones.get_dronesList()
        #print("Hooray!")
        controller.showPage(root, droneScan)
        
        
class droneScan(tk.Frame):
    '''
    tk.Frame - Frame used to host the drones available at the moment
    '''
    
    lg_Text = "Choose a drone to connect to"
    LARGE_FONT0 = ("Verdana", 18)
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.grid(row=0, column=0)
        
        
        #Scan the radio channel looking for drones
        #connection = findMyDrone()
        global drones
        drones = connection.get_dronesList()
        
        lookingForDrones_text = "This is what I've found so far"
        label = ttk.Label(self,
                     text=lookingForDrones_text,
                     font=self.LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")
   

        #=======================================================================
        # global elapsedTime
        # print(elapsedTime)
        # if len(drones) == 0:
        #     time.sleep(1)
        #     elapsedTime += 1
        #     print(elapsedTime)
        #     if elapsedTime > 2:
        #         drones = ["Ahahahaah funziona?!"]
        #     else:
        #         droneScan(root, controller) #Sadly I have to call this class again in order to load and display it
        #=======================================================================
       
        global elapsedTime
        while len(drones) == 0:
            time.sleep(1)
            connection.gui_scanForDrones()
            drones = connection.get_dronesList()
        
        
        if len(drones) != 0:
            self.selected = tk.StringVar()
            self.selected.set(drones[0][0]) #Set as "selected" the first drone found
            for d in drones:
                ttk.Radiobutton(self, 
                               text = d[0],
                               variable = self.selected,
                               value = d[0]).grid()
                
            btn_ConnectToDrone = ttk.Button(self,
                               text="Connect!",
                               command=lambda: self.connectAction(root, controller))
            btn_ConnectToDrone.grid()
        
        
    def connectAction(self, root, controller):
        '''
        Based on the selected drone, chose the following action.
        It may restart the scan if the drone has lost connection,
        It may proceed to the real welcome page if the drone is correctly connected
        '''
        #https://likegeeks.com/python-gui-examples-tkinter-tutorial/
        global selectedDrone
        selectedDrone = str(self.selected.get()) #https://www.tutorialspoint.com/python/tk_radiobutton.htm
        
        if selectedDrone == "" or selectedDrone == None:
            controller.showPage(root, droneScan)
        else:
            #print("Hai selezionato: " + selectedDrone) #Status bar in basso in cui compare il drone selezionato?
            #log.LoggingExample(selectedDrone)
            
            controller.showPage(root, welcomeConnected)
            
    
class welcomeConnected(tk.Frame):
    '''
    tk.Frame - Frame used to host the initial page after connecting to a drone
    '''
    
    global selectedDrone
    lg_Text = "You are connected to " + selectedDrone
    LARGE_FONT0 = ("Verdana", 14)
    txt_logGroups = "Set your log groups"
    txt_flightPoints = "Set your flight points"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")

        
        #START LOGGING ONLY
        button1 = ttk.Button(self,
                           text=self.txt_logGroups,
                           command=lambda: controller.showPage(root, logGroups)) #QUI DOVRÀ CAMBIARE IL COMMAND IN LOG_THIS
        button1.grid()
        
        #START FLIGHT ONLY
        button1 = ttk.Button(self,
                           text=self.txt_flightPoints,
                           command=lambda: controller.showPage(root, flightPoints)) #QUI DOVRÀ CAMBIARE IL COMMAND IN FLIGHT_TO
        button1.grid()

        #UN ALTRO BUTTON PER 
        #START LOG AND FLIGHT!

    
class flightPoints(tk.Frame):
    '''
    tk.Frame - Frame used to host the log groups
    '''
    
    lg_Text = "Your flight destinations"
    LARGE_FONT0 = ("Verdana", 14)
    txt_logGroups = "Set your log groups"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")
        
        goTo_LogGroups = ttk.Button(self,
                           text=self.txt_logGroups,
                           command=lambda: controller.showPage(root, logGroups))
        goTo_LogGroups.grid()
        
    
    
class logGroups(tk.Frame):
    '''
    tk.Frame - Frame used to host the log groups
    '''
    
    lg_Text = "Your logging groups"
    LARGE_FONT0 = ("Verdana", 12)
    txt_FlightPoints = "Set Flight"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0,
                         justify="right")
        label.grid(row=0, column=0, columnspan = 10, sticky="EW")
        
        
        #Separator
        horizontalSeparator = ttk.Label(self,
                              text = "")
        horizontalSeparator.grid(column = 0, columnspan = 10)
        

        global logGroups_Values
        totalGroups = len(logGroups_Values)
        
        if totalGroups != 0:
            for lg in range(totalGroups):
                self.addLogGroup(idGroup = lg, 
                                 name  = logGroups_Values[lg][0],
                                 var1d = logGroups_Values[lg][1],
                                 var2d = logGroups_Values[lg][2],
                                 var3d = logGroups_Values[lg][3],
                                 var4d = logGroups_Values[lg][4],
                                 var5d = logGroups_Values[lg][5],
                                 var6d = logGroups_Values[lg][6],
                                 time  = logGroups_Values[lg][7]
                                 )
        else:
            self.addLogGroup(totalGroups)
        
        #=======================================================================
        # horizontalSeparator2 = ttk.Label(self,
        #                       text = "")
        # horizontalSeparator2.grid(column = 0, columnspan = 10)
        #=======================================================================
        
        self.addNewGroupButton(root, controller)
        
        
    def addLogGroup(self, idGroup, name = "", var1d = "", var2d = "", var3d = "", var4d = "", var5d = "", var6d = "", time = 10): #FIX IT TO BE A DEFAULT-PARAMS FUNCTION
        global logGroups_EntryButtons
        groupID = idGroup +1
        totalRowInEachGroup = 6 #Each group has 6 rows
        firstRowIndex = len(logGroups_EntryButtons) * totalRowInEachGroup +2 #Newly added groups will be displayed below according to this index
        
        #Group
        groupRowIndex = firstRowIndex +1
        if name == "" or name == None:
            groupText = "Group #" + str(groupID)
        else:
            groupText = name
        groupName = ttk.Entry(self)
        groupName.insert(0, groupText)
        groupName.grid(row = groupRowIndex, column = 0, columnspan = 2, sticky="EW")
        
        
        #Separator
        horizontalSeparator = ttk.Label(self,
                              text = "")
        horizontalSeparator.grid(row = groupRowIndex+1, column = 0, columnspan = 10)
        
        
        #Log period
        logRowIndex = groupRowIndex +2
        logPeriod = ttk.Label(self,
                              text = "Log period: ")
        logPeriod.grid(row = logRowIndex, column = 0, sticky="E")
        
        logEntry = ttk.Entry(self)
        try:
            if int(time) <= 10:
                basePeriod = "10"
            else:
                basePeriod = time
        except:
            basePeriod = "10"
            
        logEntry.insert(0, basePeriod)
        logEntry.grid(row = logRowIndex, column = 1)
        
        ms = ttk.Label(self,
                              text = "ms")
        ms.grid(row = logRowIndex, column = 2, sticky="W")
        
        
        #Vars 1, 2 and 3
        loggableVariables = ["None", "stabilizer.roll", "stabilizer.yaw", "stabilizer.pitch", "estimate.x", "estimate.y"]
        varDefault = loggableVariables[0][0]
        
        vars123RowIndex = groupRowIndex #Horizontally aligned with the Group Name
        var1Label = ttk.Label(self,
                        text = "    Var #1: ")
        var1Label.grid(row = vars123RowIndex, column = 3)
        
        var1_Value = tk.StringVar()
        if var1d == "":
            var1_Value.set(varDefault)
        else:
            var1_Value.set(var1d)
        var1Entry = ttk.OptionMenu(self,
                                   var1_Value, 
                                   loggableVariables)
        var1Entry.grid(row = vars123RowIndex, column = 4, columnspan = 1)
        

        var2Label = ttk.Label(self,
                        text = "    Var #2: ")
        var2Label.grid(row = vars123RowIndex, column = 6)
        
        var2_Value = tk.StringVar()
        if var2d == "":
            var2_Value.set(varDefault)
        else:
            var2_Value.set(var2d)
        var2Entry = ttk.OptionMenu(self,
                                   var2_Value, 
                                   loggableVariables)
        var2Entry.grid(row = vars123RowIndex, column = 7, columnspan = 1)
        
        
        var3 = ttk.Label(self,
                        text = "    Var #3: ")
        var3.grid(row = vars123RowIndex, column = 9)
        
        var3_Value = tk.StringVar()
        if var3d == "":
            var3_Value.set(varDefault)
        else:
            var3_Value.set(var3d)
        var3Entry = ttk.OptionMenu(self,
                                   var3_Value, 
                                   loggableVariables)
        var3Entry.grid(row = vars123RowIndex, column = 10, columnspan = 1)
        
        
        #Vars 4, 5, and 6
        vars456RowIndex = logRowIndex #Horizontally aligned with the Log Period
        var4 = ttk.Label(self,
                        text = "    Var #4: ")
        var4.grid(row = vars456RowIndex, column = 3)
        
        var4_Value = tk.StringVar()
        if var4d == "":
            var4_Value.set(varDefault)
        else:
            var4_Value.set(var4d)
        var4Entry = ttk.OptionMenu(self,
                                   var4_Value, 
                                   loggableVariables)
        var4Entry.grid(row = vars456RowIndex, column = 4, columnspan = 1)
        
        
        var5 = ttk.Label(self,
                        text = "    Var #5: ")
        var5.grid(row = vars456RowIndex, column = 6)
        
        var5_Value = tk.StringVar()
        if var5d == "":
            var5_Value.set(varDefault)
        else:
            var5_Value.set(var5d)
        var5Entry = ttk.OptionMenu(self,
                                   var5_Value, 
                                   loggableVariables)
        var5Entry.grid(row = vars456RowIndex, column = 7, columnspan = 1)
        
        
        var6 = ttk.Label(self,
                        text = "    Var #6: ")
        var6.grid(row = vars456RowIndex, column = 9)
        
        var6_Value = tk.StringVar()
        if var6d == "":
            var6_Value.set(varDefault)
        else:
            var6_Value.set(var6d)
        var6Entry = ttk.OptionMenu(self,
                                   var6_Value, 
                                   loggableVariables)
        var6Entry.grid(row = vars456RowIndex, column = 10, columnspan = 1)
        
        
        horizontalSeparator2 = ttk.Label(self,
                              text = "")
        horizontalSeparator2.grid(column = 0, columnspan = 10)
        
        horizontalSeparator3 = ttk.Label(self,
                              text = "")
        horizontalSeparator3.grid(column = 0, columnspan = 10)
        
        #Add the current entries to the global list of Logging Groups
        logGroups_EntryButtons.append([groupName, var1_Value, var2_Value, var3_Value, var4_Value, var5_Value, var6_Value, logEntry])
        
        
        #ADD A RESET(id)  BUTTON?
        #ADD A DELETE(id) BUTTON?
        
    def addNewGroupButton(self, root, controller):
        
        addNewGroup = ttk.Button(self,
                                 text = "Add a new group of variables to log!",
                                 command = lambda: self.addNewGroupHere(root, controller))
        addNewGroup.grid(column = 4, columnspan = 3)
        
        
    def addNewGroupHere(self, root, controller):
        
        global logGroups_EntryButtons
        
        self.addLogGroup(len(logGroups_EntryButtons))
        self.saveLogGroupState()
        controller.showPage(root, logGroups)
        
        
    def saveLogGroupState(self):
        '''
        Save the current values of logGroup_EntryButtons into the global list logGroups_Values
        New instantiations of "addLogGroup" can thus be made by looking at logGroups_Values 
            so to set the user-selected values back to the form
        Source: https://snakify.org/en/lessons/two_dimensional_lists_arrays/
        '''
        global logGroups_EntryButtons
        global logGroups_Values
        logGroups_Values = []
        for id_group in range(len(logGroups_EntryButtons)):
            appendThis = []
            for id_entry in range(len(logGroups_EntryButtons[id_group])):
                appendThis.append(logGroups_EntryButtons[id_group][id_entry].get())
            logGroups_Values.append(appendThis)
            
        logGroups_EntryButtons = []
                
        
    def addDefaultGroup(self):
        None
        
    def loadLogGroups(self):
        None
        
        
        #=======================================================================
        # goTo_FlightPoints = tk.Button(self,
        #                    text=self.txt_FlightPoints,
        #                    command=lambda: controller.showPage(root, flightPoints))
        # goTo_FlightPoints.grid()
        #=======================================================================
        
    
class PageOne(tk.Frame):
    '''
    tk.Frame - Frame used to host the WelcomePage
    '''

    page1Label = "Stupid lonely page"
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.page1Label,
                         font=LARGE_FONT1)
        label.grid(row=0, column=0, sticky="nsew")
        
        button11 = ttk.Button(self,
                           text=welcomePageButton,
                           command=lambda: controller.showPage(root, WelcomePage))
                            # command - used to pass functions
                            # lambda - creates a quick throwaway function
        button11.grid()
        
           
   
"""  
   
   
# Check for this code under "class PageThree(tk.Frame):"
# https://pythonprogramming.net/embedding-live-matplotlib-graph-tkinter-gui/?completed=/how-to-embed-matplotlib-graph-tkinter-gui/        
class LiveGraph(tk.Frame):
    '''
    tk.Frame - Frame used to host the WelcomePage
    '''

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=liveGraphLabel,
                         font=LARGE_FONT2)
        label.pack(pady=10, padx=10)
        
        button12 = ttk.Button(self,
                           text=welcomePageButton,
                           command=lambda: controller.show_frame(WelcomePage))
                            # command - used to pass functions
                            # lambda - creates a quick throwaway function
        button12.pack()
        
        button22 = ttk.Button(self,
                           text=page1Button,
                           command=lambda: controller.show_frame(PageOne))
        button22.pack()
        
        button2g = ttk.Button(self,
                           text=staticGraphButton,
                           command=lambda: controller.show_frame(StaticGraph))
        button2g.pack()
        
        canvas = FigureCanvasTkAgg(anime.myFigure, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    
# Created for https://pythonprogramming.net/how-to-embed-matplotlib-liveGraph-tkinter-gui/
# Created for https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
class StaticGraph(tk.Frame):
    '''
    tk.Frame - Frame used to host the WelcomePage
    '''

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=staticGraphLabel,
                         font=LARGE_FONTg)
        label.pack(pady=10, padx=10)
        
        button1g = ttk.Button(self,
                           text=welcomePageButton,
                           command=lambda: controller.show_frame(WelcomePage))
                            # command - used to pass functions
                            # lambda - creates a quick throwaway function
        button1g.pack()
        
        button1 = ttk.Button(self,
                           text=page1Button,
                           command=lambda: controller.show_frame(PageOne))
                            # command - used to pass functions
                            # lambda - creates a quick throwaway function
        button1.pack()
        
        button2 = ttk.Button(self,
                           text=liveGraphButton,
                           command=lambda: controller.show_frame(LiveGraph))
        button2.pack()
        
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)  # f.add_subplot(ijk): i-th plot, j rows, k columns
        
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        y = [5, 6, 1, 3, 8, 9, 3, 5]   
        a.plot(x, y)
        # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
            
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)    
        
"""
