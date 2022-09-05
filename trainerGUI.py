from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.dropdown import DropDown
from kivy.uix.actionbar import ActionBar
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from time import gmtime, strftime
from kivy.clock import Clock
print("If you get errors when running the GUI from VESC, you need to clean getters.py en setters.py uit de pyvesc directory")
print("Every row except the first one.")

import time
from commands import *
import trainerCommunication
import commands
import trainerGraph
import json

import csv

class MyButtons():
    pass


class ControllerSimulate(GridLayout):
    def __init__(self, *args, **kwargs):
        super(ControllerSimulate, self).__init__(*args, **kwargs)

    def resetController(self):
        print('loading settings')
        try:
            if(self.comm.isConnected()):
                self.comm.sendCommand(ResetController)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def closeBridgeRelay(self):
        print('closing bridge relay')
        try:
            if(self.comm.isConnected()):
                self.comm.sendCommand(SetCloseBridgeRelay)
        except AttributeError:
            print('Comm port not instantiated/connected')
    def openBridgeRelay(self):
        print('opening bridge relay')
        try:
            if(self.comm.isConnected()):
                self.comm.sendCommand(SetOpenBridgeRelay)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def doFixDutyCycle(self):
        print('loading settings')
        try:
            if(self.comm.isConnected()):
                data = SetDutyCycle
                data.dutyCycle = float(self.ids['duty_slider'].value)
                print(data.dutyCycle)
                self.comm.sendSetCommand(data)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def doResetOvervoltage(self):
        print('Resetting overvoltage')
        try:
            if(self.comm.isConnected()):
                data = ResetOvervoltage
                self.comm.sendSetCommand(data)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def doResetSafety(self):
        print('Resetting safety')
        try:
            if(self.comm.isConnected()):
                data = ResetSafety
                self.comm.sendSetCommand(data)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def doToggleCapVoltage(self):
        print('ToggleCap')
        try:
            if(self.comm.isConnected()):
                data = ToggleCapRealVoltage
                self.comm.sendSetCommand(data)
        except AttributeError:
            print('Comm port not instantiated/connected')


    def setComm(self, comm):
        print('setting comport for Duty')
        self.comm = comm


class ControllerStatus(BoxLayout):
    statusText = ObjectProperty(None)
    auxText = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super(ControllerStatus, self).__init__(*args, **kwargs)

    def updateStatus(self,data):
        self.statusText.text = data

    def updateAuxValues(self,data):
        self.auxText.text = data


class ControllerOscilloscope(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(ControllerOscilloscope, self).__init__(*args, **kwargs)
        self.data = []
        self.controlTaskStates = controlTaskStates

    def setComm(self,comm):
        self.comm = comm


    def getEvents(self):
        data = GetLastEvents
        data.events = 10
        print('getting events: %i' %data.events)
        self.sendSetCommand(data)

    def eraseLog(self):
        data = ResetLog
        print('resetting log')
        self.sendSetCommand(data)

    def doSampling(self):
        data = StartSampling
        data.divider = self.ids['sample_divider'].value
        print('sampling with divider: %i' %data.divider)
        self.sendSetCommand(data)

    def doSaveSamples(self):
        if len(self.data)>0:
            fileName = strftime("Samples-%Y-%m-%d-%H-%M-%S.csv", gmtime())
            print('saving to %s' %fileName)
            with open(fileName, 'w') as f:
                w = csv.DictWriter(f, self.data[0].__dict__.keys())
                w.writeheader()
                for part in self.data:
                    w.writerow(part.__dict__)


    def doStopSampling(self):
        print('stop sampling')
        self.sendCommand(StopSampling)

    def doPlotting(self):
        print('plotting')
        ControllerGraph.doPlot(self.data)

    def doGetSamples(self):
        print('getting samples')
        aSet = sendGetAllControlState
        aSet.count = 0
        self.sendSetCommand(aSet)

    def doGetGenerator(self):
        print('Getting generator')
        aGet = GetGenerator
        self.sendCommand(aGet)

    def doSetStopSamplingEvent(self):
        aSet = SetStopSamplingEvent
        aSet.event = self.ids['event_slider'].value
        print(F'Setting sampling event to {aSet.event}')
        self.sendSetCommand(aSet)

    def doResumeGetSamples(self):
        aSet = sendGetAllControlState
        if len(self.data)>0:
            aSet.count = (self.data[-1].count+1)
        if aSet.count < 512:
            print(F'Resume getting samples from {aSet.count}')
            self.sendSetCommand(aSet)

    def doGetIsNewEventAvailable(self):
        self.sendCommand(GetIsNewEvent)

    def appendData(self,data):
        print('got a data packet %i' %len(self.data))
        self.data.append(data)
        self.ids['data_count'].text = 'Points: %i' %len(self.data)
        aSet = sendGetAllControlState
        if (self.comm.isSerial()):
            if (data.count < 5.11):
                aSet.count = round(data.count * 100 + 1)
                print('data count %f' % aSet.count)
                self.sendSetCommand(aSet)

    def updateIsNewEvent(self,data):
        self.ids['is_new_samples'].text = str(int(data.isNewEvent))

    def doResetData(self):
        self.data = []
        self.ids['data_count'].text = 'Points: %i' %len(self.data)

    def sendSetCommand(self,command):
        try:
            if(self.comm.isConnected()):
                self.comm.sendSetCommand(command)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def sendCommand(self,command):
        try:
            if(self.comm.isConnected()):
                self.comm.sendCommand(command)
        except AttributeError:
            print('Comm port not instantiated/connected')

class ControllerSetPoints(GridLayout):
    def __init__(self, *args, **kwargs):
        super(ControllerSetPoints, self).__init__(*args, **kwargs)
        self.rSlider = ObjectProperty(None)
        self.rText = ObjectProperty(None)
        self.uCapText = ObjectProperty(None)
        self.uCapSetSlider = ObjectProperty(None)

    def doUpdateSettings(self):
        try:
            if(self.comm.isConnected()):
                data = SetSetPoints
                data.voltage = self.ids['vout_slider'].value
                data.freq = self.ids['freq_slider'].value
                data.deadTime = self.ids['deadtime_slider'].value
                data.vbusMin = self.ids['vbusMin_slider'].value
                data.vbusMax = self.ids['vbusMax_slider'].value
                data.iMax = self.ids['iMax_slider'].value
                self.comm.sendSetCommand(SetSetPoints)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def updateSetpointValues(self,data):
        aStr = ""
        for (key, val) in data.__dict__.items():
            aStr = aStr + str(key) + ':  ' + str(val) + '\r\n'
        print(aStr)
        self.ids['vout_slider'].value = data.vout
        self.ids['freq_slider'].value = data.freq
        self.ids['deadtime_slider'].value = data.deadTime
        self.ids['vbusMin_slider'].value = data.vBusMin
        self.ids['vbusmax_slider'].value = data.vBusMax
        self.ids['iMax_slider'].value = data.iMax

    def setComm(self,comm):
        print('setting comport for setpoints')
        self.comm = comm

    def doLoadSettings(self):
        print('loading settings')
        try:
            if(self.comm.isConnected()):
                self.comm.sendCommand(GetSetPoints)
        except AttributeError:
            print('Comm port not instantiated/connected')

    def changeUCapMax(self,obj):
        print(obj)

    def changeR(self,obj):
        print(obj)

    def setUCapMax(self,value):
        self.uCapSetSlider.value = value

    def setR(self,value):
        self.rSlider.value = value

class Controller(BoxLayout):
    controllerStatus = ObjectProperty(None)
    comDropDown = DropDown()
    portButton = ObjectProperty(None)
    connectButton = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.portButton.bind(on_release=self.fillPorts)
        self.comm = trainerCommunication.ControllerCommunicationThread('COM0', 19200)
        self.connectButton.bind(on_release=self.connectToController)
        self.tcpConnectButton.bind(on_release=self.tcpConnectToController)
        self.comm.start()
        self.ids['controller_set_points'].setComm(self.comm)
        self.ids['controller_simulate'].setComm(self.comm)
        self.ids['controller_scope'].setComm(self.comm)
        self.liveDataEvent = Clock.schedule_interval(self.getAllData, 200)
        self.liveDataEvent.cancel()


    def makeBar(self):
        wid = ActionBar()
        return wid

    def comPortSelected(self,a,x):
        connectDirectly = False
        if(self.comm.isConnected()):
            connectDirectly = True
            self.comm.stopSerial()
        print('selected port: ' + x)
        self.portButton.text = x
        self.comm.setComPort(x)
        if connectDirectly:
            self.connectToController()

    def sendCommand(self,command):
#        if(not ((command == GetControlState) or (command==GetAuxValues))):
         self.comm.sendCommand(command)


    def startLiveView(self):
        self.startLiveUpdate()

    def stopLiveView(self):
        self.liveDataEvent.cancel()

    def startLiveUpdate(self,*args):
        print("Starting live update")
        self.liveDataEvent.cancel()
        self.liveDataEvent = Clock.schedule_interval(self.getAllData, 2)

    def connectToController(self,obj):
        if not self.comm.isConnected():
            self.comm.connect()
        if(self.comm.isConnected()):
            self.comm.setCallback(self.commandReceived)
  #          self.startLiveUpdate()

    def getAllData(self,obj):
        print("getting all data")
        self.sendCommand(commands.GetControlState)
        time.sleep(0.5)
        self.sendCommand(commands.GetAuxValues)

    def tcpConnectToController(self,obj):
        if not self.comm.isConnected():
            aPort = int(self.ids['tcpPort'].text)
            print("connecting to tcp port %i" %aPort)
            self.comm.tcpConnect(aPort)

        if (self.comm.isConnected()):
            self.comm.setCallback(self.commandReceived)
            self.startLiveUpdate()

    def commandReceived(self,data):
        print(data)
        if type(data)==commands.GetControlState:
            aStr = ""
            for (key,val) in data.__dict__.items():
#                print(key + " " + str(val))
                if key == 'controlTaskState':
                    if val < len(controlTaskStates):
                        controlName = controlTaskStates[int(val)]
                        aStr = aStr + str(key) + ':  ' + str(val) + "," + controlName + '\r\n'
                    else:
                        aStr = aStr + str(key) + ':  ' + str(val) + '\r\n'
                else:
                    aStr = aStr + str(key) + ':  ' + str(val) + '\r\n'
            self.controllerStatus.updateStatus(aStr)
        if type(data)==commands.GetAuxValues:
            aStr = ""
            for (key,val) in data.__dict__.items():
                aStr = aStr + str(key) + ':  ' + str(val) + '\r\n'
            self.controllerStatus.updateAuxValues(aStr)
            self.ids['iErrBar'].text = str(data.__dict__['IErr'])
            self.ids['vPPBar'].text = str(data.__dict__['Vpp'])
            self.ids['rPMBar'].text = str(data.__dict__['Rpm'])


        if type(data)==commands.GetSetPoints:
            self.ids['controller_set_points'].updateSetpointValues(data)
        if type(data)==commands.GetAllControlState:
            self.ids['controller_scope'].appendData(data)
        if type(data)==commands.GetGenerator:
            print(json.dumps(data.__dict__, indent=4))

        if type(data)==commands.Print:
            print("Controller Message: " + data.text)

        if type(data)==commands.GetIsNewEvent:
            event = data.isNewEvent
            print(F"New event is available?: {event}")
            self.ids['controller_scope'].updateIsNewEvent(data)

    def fillPorts(self,text):
        print('listing ports')
        data = trainerCommunication.listPorts()
        print(data)
        self.comDropDown.clear_widgets()
        for port in data:
            print(port)
            btn = Button(text=port[0], size_hint_y=None,height=44)
            btn.bind(on_release=lambda btn: self.comDropDown.select(btn.text))
            self.comDropDown.add_widget(btn)
        self.comDropDown.bind(on_select=self.comPortSelected)
        self.comDropDown.open(self.portButton)


class ControllerTrainerApp(App):
    def build(self):
        return Controller()

if __name__ == '__main__':
    ControllerTrainerApp().run()





#
# Tools:
# s = Slider(min=-100, max=100, value=25, step=0.2)
# s.bind(on_release=on_change)
# btn1 = ToggleButton(text='Male', group='sex',)
# button = Button(text='Hello world', font_size=14)
#
#
#
# checkbox = CheckBox()
# checkbox.bind(active=on_checkbox_active)
#
# def on_checkbox_active(checkbox, value):
#     if value:
#         print('The checkbox', checkbox, 'is active')
#     else:
#         print('The checkbox', checkbox, 'is inactive')
#
#
# def on_press(instance):
#     print('The button <%s> is being pressed' % instance.text)
#
# btn1 = Button(text='Hello world 1')
# btn1.bind(on_press=on_press)
#
# def on_change(instance,value):
#
# def on_enter(instance, value):
#     print('User pressed enter in', instance)
# def on_text(instance, value):
#     print('The widget', instance, 'have:', value)
# def on_focus(instance, value):
#     if value:
#         print('User focused', instance)
#     else:
#         print('User defocused', instance)
#
# textinput = TextInput(text='Hello world', multiline=False)
# textinput = TextInput()
# textinput.bind(text=on_text)
# textinput.bind(focus=on_focus)
# textinput.bind(on_text_validate=on_enter)


