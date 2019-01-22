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
drones = connection.get_dronesList()

 
 
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
    txt_logGroups = "Set your log groups"
    
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
        while len(drones) == 0:
            time.sleep(1)
            drones = connection.get_dronesList()
            #lookingForDrones_text += "."
            #label.configure(text = lookingForDrones_text)
        
        
        print("E' già buono che tu sia arrivato qui ma...")
        if len(drones) != 0:
            print("Qua devi arrivare!")
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
        self.selectedDrone = str(self.selected.get()) #https://www.tutorialspoint.com/python/tk_radiobutton.htm
        
        if self.selectedDrone == "" or self.selectedDrone == None:
            controller.showPage(root, droneScan)
        else:
            print("Hai selezionato: " + self.selectedDrone) #Status bar in basso in cui compare il drone selezionato?
            log.LoggingExample(self.selectedDrone)
            
            controller.showPage(root, welcomeConnected)
            
    
class welcomeConnected(tk.Frame):
    '''
    tk.Frame - Frame used to host the initial page after connecting to a drone
    '''
    
    lg_Text = "YOU ARE CONNECTED!!"
    LARGE_FONT0 = ("Verdana", 14)
    txt_logGroups = "Set your log groups"
    txt_flightPoints = "Set your flight points"
    
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        label = ttk.Label(self,
                         text=self.lg_Text,
                         font=self.LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")

        
        button1 = ttk.Button(self,
                           text=self.txt_logGroups,
                           command=lambda: controller.showPage(root, logGroups))
        button1.grid()
        
        button1 = ttk.Button(self,
                           text=self.txt_flightPoints,
                           command=lambda: controller.showPage(root, flightPoints))
        button1.grid()


    
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
                         font=self.LARGE_FONT0)
        label.grid(row=0, column=0, sticky="nsew")
        
        goTo_FlightPoints = tk.Button(self,
                           text=self.txt_FlightPoints,
                           command=lambda: controller.showPage(root, flightPoints))
        goTo_FlightPoints.grid()
        
    
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
