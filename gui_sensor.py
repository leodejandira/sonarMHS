

import matplotlib as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import wx
import configparser
import pathlib
import time
import serial
import xlsxwriter

config = configparser.ConfigParser()
file = pathlib.Path("configure_value.ini")
if file.exists():
    config.read('configure_value.ini')
else:
    config['constants'] = { 'gravity':'9.8',
                            'elasticconstant':'35.6',
                            'equilibrepoint':'0.39',
                            'mass':'1',
                            'port':'/dev/ttyUSB0'}
    with open ('configure_value.ini', 'w') as configfile:
        config.write(configfile)

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Globals °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#


#collected data
position = []
instant = []
SonarColletctedData = []
velocity = []
epg = []
epe = []
ec = []
totalEnergy = []


################################################################################# Define top panel ########################################################################################


class TopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent) 

#----------------Add figure Canvas layout----------------#

#import canvas figure layout
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
#configure the canvas pic
        self.sizer = wx.BoxSizer(wx.VERTICAL) 
        self.sizer.Add(self.canvas, 1, wx.EXPAND) 
        self.SetSizer(self.sizer) 
        self.axes.set_title("Energy Graphic") 
        self.axes.set_xlabel("Time(s)") 
        self.axes.set_ylabel("Energy(j)") 


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Canvas in figure °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#

    def draw(self, instant, epe, epg, ec, totalEnergy):
        #print(epe)
        #print(epg)
        #print(ec)
        #print(totalEnergy)
        #print(instant)
        a=[]
        b=[]
        c=[]
        d=[]
        f=[]

        for z in range(0,len(epe)):
            a.append(epe[z])
            b.append(epg[z])
            c.append(ec[z])
            d.append(totalEnergy[z])
            f.append(instant[z])
            time.sleep(0.03)
            self.axes.clear()
            self.axes.plot(f, a, '-o')
            self.axes.plot(f, b, '-o')
            self.axes.plot(f, c, '-o')
            self.axes.plot(f, d, '-o')
            self.canvas.draw()






        #self.axes.clear()
        #self.axes.plot(instant, epe, '-o')
        #self.axes.plot(instant, epg, '-o')
        #self.axes.plot(instant, ec, '-o')
        #self.axes.plot(instant, totalEnergy, '-o')
#
        #self.canvas.draw()

        #time = data.tp() 
        #elastic = data.epe()
        #gravitational = data.epg() 
        #self.axes.plot(time, elastic) 
        #self.axes.plot(time, gravitational) 


################################################################################# Define bottom panel ########################################################################################

class BottomPanel(wx.Panel):
    def __init__(self, parent, top, config):
        wx.Panel.__init__(self, parent = parent)

        self.graph = top
        

        splitter = wx.SplitterWindow(self)
        rightP = BottomRightPanel(splitter)
        leftP = BottomLeftPanel(splitter, config, top, rightP) 
        
        splitter.SplitVertically(leftP, rightP)
        splitter.SetMinimumPaneSize(800)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        splitter.SetMinimumPaneSize(320)

################################################################################# Define bottom Leftpanel #################################################################################


class BottomLeftPanel(wx.Panel):
    def __init__(self, parent, config, top, right):
        self.right = right
        self.top = top

        #config = configparser.ConfigParser()
        #config.read('configure_value.ini')

        wx.Panel.__init__(self, parent = parent)
#tittle bottom left panel and basic config
        self.tittle1 = wx.StaticText(self, label="Settings", pos = (145,5)) 
        self.SetBackgroundColour("light grey")
        #labelChannels = wx.StaticText(self, -1, label = "Preview", pos = (100,50)) 
        #labelChannels = wx.StaticText(self, -1, label = "Constants", pos = (320,50)) 

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Start  and check buton °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#

#Start button
        self.togglebuttonStart = wx.ToggleButton(self, id = -1, label = "Start", pos = (230, 30)) 
        self.togglebuttonStart.Bind(wx.EVT_TOGGLEBUTTON, self.showGraphic) 
#Check box
   #     self.check1 = wx.CheckBox(self, -1, label = "Show graphic",  pos = (10,80))
    #    self.Bind(wx.EVT_CHECKBOX, self.onChecked) 


#        self.check2 = wx.CheckBox(self, -1, label = "Show collected data",  pos = (10,120))
#        self.Bind(wx.EVT_CHECKBOX, self.onChecked)  
#
#        self.check3 = wx.CheckBox(self, -1, label = "Show energy data",  pos = (10,160)) 
#        self.Bind(wx.EVT_CHECKBOX, self.onChecked)         


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Show graph  Buttons °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#


        self.button = wx.Button(self, id = -1, label = "Graphic", pos = (230, 150)) 
        self.button.Bind(wx.EVT_BUTTON, self.graphShow)

        self.button = wx.Button(self, id = -1, label = "Export", pos = (230, 90)) 
        self.button.Bind(wx.EVT_BUTTON, self.excelImport)



 #°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Send Buttons °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#
#Serial port
        self.tittle1 = wx.StaticText(self, label="Serial port", pos = (10,30))
        self.textboxSampleTime5 = wx.TextCtrl(self, -1, config.get('constants', 'port'), pos = (80,30), size = (58, -1))
        self.buttonSend = wx.Button(self, -1, "Send", pos = (145,30), size = (50, -1))
        self.buttonSend.Bind(wx.EVT_BUTTON, self.onSend(5, self.textboxSampleTime5, config))


        
#Gravity 
        self.tittle1 = wx.StaticText(self, label="Gravity value", pos = (10,60))
        self.textboxSampleTime2 = wx.TextCtrl(self, -1, config.get('constants', 'gravity'), pos = (80,60), size = (58, -1)) 
        self.buttonSend = wx.Button(self, -1, "Send", pos = (145,60), size = (50, -1))
        self.buttonSend.Bind(wx.EVT_BUTTON, self.onSend(2, self.textboxSampleTime2, config))
#Elastic constant
        self.tittle1 = wx.StaticText(self, label="Elastic Const.", pos = (10,90))
        self.textboxSampleTime3 = wx.TextCtrl(self, -1, config.get('constants', 'elasticconstant'), pos = (80,90), size = (58, -1)) 
        self.buttonSend = wx.Button(self, -1, "Send", pos = (145,90), size = (50, -1))
        self.buttonSend.Bind(wx.EVT_BUTTON, self.onSend(3, self.textboxSampleTime3, config))
#Object Mass     
        self.tittle1 = wx.StaticText(self, label="Object mass", pos = (10,120))
        self.textboxSampleTime4 = wx.TextCtrl(self, -1, config.get('constants', 'mass'), pos = (80,120), size = (58, -1)) 
        self.buttonSend = wx.Button(self, -1, "Send", pos = (145,120), size = (50, -1))
        self.buttonSend.Bind(wx.EVT_BUTTON, self.onSend(4, self.textboxSampleTime4, config))
#balance position
        self.tittle1 = wx.StaticText(self, label="Balance pos.", pos = (10,150))
        self.textboxSampleTime1 = wx.TextCtrl(self, -1, config.get('constants', 'equilibrePoint'), pos = (80,150), size = (58, -1)) 
        self.buttonSend = wx.Button(self, -1, "Send", pos = (145,150), size = (50, -1))
        self.buttonSend.Bind(wx.EVT_BUTTON, self.onSend(1, self.textboxSampleTime1, config))


        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.dataCollect, self.timer)

#        self.timer_check = 0


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Timer functions °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#
   
    def dataCollect(self, event):
#            print(self.timer_check)
#            self.timer_check += 0.050
#        self.serial_arduino.write('').decode('utf-8').replace("\r\n","")

        i   = 0
        ms  = ['ms']
        cm  = ['cm']
        tp = ['tp']
        tmp = self.serial_arduino.readline().decode('utf-8').replace("\r\n","")
        x = tmp.split(",")
        if len(x) == 3: #cancela arreys que não tenham tres linhas 
            if float(x[1]) <= 50:
                ms.append(x[0])
                cm.append(x[1])
                tp.append(x[2])
                SonarColletctedData.append(x)
                position.append(x[1])
                instant.append(x[2])
        print(position)

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Show plot °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#
    def graphShow (self, event):
        self.top.draw(instant, epe, epg, ec, totalEnergy)
        #for n in range (0, len(position)):
        #    self.right.boxInstant.WriteText("{} \n".format(instant[n]))
        for n in range (0, len(velocity)):
            self.right.boxTotal.WriteText("{} \n".format(totalEnergy[n]))

        for n in range (0, len(epg)):
            self.right.boxGrav.WriteText("{} \n".format(epg[n]))
        for n in range (0, len(epe)):
            self.right.boxElast.WriteText("{} \n".format(epe[n]))
        for n in range (0, len(ec)):
            self.right.boxCinet.WriteText("{} \n".format(ec[n]))

#realizar a ciração de tres caixas, cada uma com um valor dos dados coletados


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° check functions °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#
  

    def onChecked(self, event):
        cb = event.GetEventObject()
        print("{} is clicked".format(cb.GetLabel()))
        if cb.Value == True:
            print("To marcado")
        else:
            print("Num to mais")

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Send functions °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#

    def onSend(self, constants, data, config):
        def OnClick(event):
            if constants == 1 : 
                config.set('constants', 'equilibrePoint', data.GetValue())
            if constants == 2 : 
                config.set('constants', 'gravity', data.GetValue())
            if constants == 3 : 
                config.set('constants', 'elasticconstant', data.GetValue())
            if constants == 4 : 
                config.set('constants', 'mass', data.GetValue())
            if constants == 5 : 
                config.set('constants', 'port', data.GetValue())            
            configfile = open('configure_value.ini', 'w')
            config.write(configfile, space_around_delimiters=False)
            configfile.close()
        return OnClick

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Start functions °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#

    def showGraphic(self, event):
           

        val = self.togglebuttonStart.GetValue()
        if (val == True):
            self.togglebuttonStart.SetLabel("Started")
            self.timer.Start(50)
            
        else:
            self.togglebuttonStart.SetLabel("Stoped")
            self.timer.Stop()
            #workbook = xlsxwriter.Workbook('SensorData.xlsx')
            #worksheet = workbook.add_worksheet() 
            #row = 0 #
            #for indice, valor in enumerate(SonarColletctedData):
            #    worksheet.write_column(row, indice, valor)
            #workbook.close()

            def epgf(position):    
                return float(config.get('constants', 'mass')) * float(config.get('constants', 'gravity')) * (0.01*float(position))

            def epef(position):    
                return 0.5 * float(config.get('constants', 'elasticconstant')) * ((0.01*float(position)) - float(config.get('constants', 'equilibrePoint')))**2
            
            def velocf(position,deltaposition):
                return ((0.01*float(position)) - (0.01* float(deltaposition)))/0.050
                

            for z in range(0, len(position)):
                epg.append(epgf(position[z]))
                epe.append(epef(position[z]))
                
                if z == 0:
                    velocity.append(0)
                else:
                    velocity.append(velocf(position[z], position[z-1]))
                
            def velocf(velocity):
                return (0.5 * float(velocity) * (float(config.get('constants', 'mass'))**2))

            for z in range(0, len(position)):
                ec.append(velocf(velocity[z]))   
                    
            def totalf(epg, epe, ec):
                return epg + epe + ec

            for z in range (0, len(epg)):
                totalEnergy.append(totalf(epg[z], epe[z], ec[z]))              
            
            #print(totalEnergy)
            #print(totalEnergy)
            
        
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Serial conection °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#

        self.serial_arduino = serial.Serial(config.get('constants', 'port'), 9600, timeout = 2)

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° Excel import °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°#

    def excelImport(self, event):  
        positionSI = []
        for item in position:
            positionSI.append(float(item)*0.01)

        workbook = xlsxwriter.Workbook('SensorData.xlsx')
        worksheet = workbook.add_worksheet() 
        #row = 0 #
        for indice, valor in enumerate(position):
            worksheet.write_column(1, 0, instant)
            worksheet.write_column(1, 1, positionSI)
            worksheet.write_column(1, 2, velocity)
        #for indice, valor in enumerate(SonarColletctedData):
        #    worksheet.write_column(row, indice, valor)
        workbook.close()

#        while (conection == 1):
#            if (self.serial_arduino.inWaiting()>0):
#                myData = self.serial_arduino.readline().decode('utf-8').replace("\r\n","") 
#                print (myData)   


            
#        self.serial_arduino.write('\r\n')
#        response = self.serial_arduino.readline()       
#        print(response)

################################################################################# Define bottom Rightpanel #################################################################################

class BottomRightPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent)

        
        self.SetBackgroundColour("light yellow")
        #self.tittle1 = wx.StaticText(self, label="colectted data", pos = (230,10))
        #self.tittle1 = wx.StaticText(self, label="calculed energy data", pos = (750,10))

#show collected data

        #self.tittle1 = wx.StaticText(self, label="Instant", pos = (90,30))
        #self.boxInstant = wx.TextCtrl(self,5, "",wx.Point(30,60), wx.Size(160,280),\
        #        wx.TE_MULTILINE |  wx.TE_READONLY)
        #self.tittle1 = wx.StaticText(self, label="Position", pos = (250,30))
        #self.boxPosition = wx.TextCtrl(self,5, "",wx.Point(200,60), wx.Size(160,280),\
        #        wx.TE_MULTILINE |  wx.TE_READONLY)

#show collected data calcul      200

        self.tittle1 = wx.StaticText(self, label="Grav. Potential Energy", pos = (50,10))
        self.boxGrav = wx.TextCtrl(self,5, "",wx.Point(30,30), wx.Size(160,160),\
                wx.TE_MULTILINE |  wx.TE_READONLY)
        self.tittle1 = wx.StaticText(self, label="Elast. Potential Energy", pos = (230,10))
        self.boxElast = wx.TextCtrl(self,5, "",wx.Point(200,30), wx.Size(160,160),\
                wx.TE_MULTILINE |  wx.TE_READONLY)
        self.tittle1 = wx.StaticText(self, label="Cinetic Enerhy", pos = (410,10))
        self.boxCinet = wx.TextCtrl(self,5, "",wx.Point(370,30), wx.Size(160,160),\
                wx.TE_MULTILINE |  wx.TE_READONLY) 
        self.tittle1 = wx.StaticText(self, label="Total Energy", pos = (590,10))
        self.boxTotal = wx.TextCtrl(self,5, "",wx.Point(540,30), wx.Size(160,160),\
                wx.TE_MULTILINE |  wx.TE_READONLY) 


############################################################################## Build MAin frame for each object ############################################################################

class Main(wx.Frame):
    def __init__ (self):
        wx.Frame.__init__(self, parent = None, title = "Vertical Simple Harmonic Motion", size = (1200,700))

        splitter = wx.SplitterWindow(self)
        top = TopPanel(splitter)
        bottom = BottomPanel(splitter, top, config)
        splitter.SplitHorizontally(top, bottom)
        splitter.SetMinimumPaneSize(450)
        #drop draw function
        #top.draw(epe) 

    


################################################################################# Show ###################################################################################################


if __name__ == "__main__" :
    app = wx.App()
    frame = Main()
    frame.Show()
    app.MainLoop()