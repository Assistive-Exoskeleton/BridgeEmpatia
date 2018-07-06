# -*- coding: utf-8 -*-
import ConfigParser
import math
import numpy
import os, sys

import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher

from BridgeInput import *
from BridgeControl import *
from BridgePatient import *

NONE                = -1
IDLE                = 0
INIT_SYSTEM         = 1
DONNING             = 2
REST_POSITION       = 3
READY               = 4
RUNNING             = 5
ERROR               = 6
SPEED_CTRL          = 7
POS_CTRL            = 8
POS_CTRL_ABS        = 9
RECALL_POSITION     = 10


class BridgeClass:
    def __init__(self, parent):
        self.MainWindow             = parent
        self.JointsNum              = 4
        self.Joints                 = [None] * self.JointsNum
        self.JointInitThreads       = [None] * self.JointsNum
        self.JointUpdateThreads     = [None] * self.JointsNum
        self.ControlThread          = None
        self.InputThread            = None
        self.Control                = ControlClass(self)
        self.Patient                = PatientClass()
        self.Joystick               = JoystickClass(self)
        self.Status                 = NONE
        self.OldStatus              = NONE
        self.InputList              = []
        self.SavedPositions         = []

    def SavePosition(self,name):
        "Save Actual Position"
        try:

            New_Position = PositionClass(self,name,[None]*self.JointsNum)
            for i in range(0, self.JointsNum):
                New_Position.Jtarget[i] = self.Joints[i].PositionStep
            self.SavedPositions.append(New_Position)
        except Exception, e:
            print "#Error: Save Position failed |" + str(e)
        finally:
            print " + New Position Saved : " + self.SavedPositions[len(self.SavedPositions)-1].Name + " " + str(self.SavedPositions[len(self.SavedPositions)-1].Jtarget)

    def GoToPosition(self,num):
        "Go To Saved Position"

        try:
            for i in range(0, self.JointsNum):
                self.Joints[i].SetJtarget(self.SavedPositions[num].Jtarget[i])
                self.Joints[i].RestDone = False
            self.SetStatus(RECALL_POSITION)
        except Exception, e:
            print "#Error: Go To Position failed |" + str(e)
        finally:
            print " + New Position Recalled : " + self.SavedPositions[num].Name + " " + str(self.SavedPositions[num].Jtarget)

    def SetStatus(self,case):

        "Set Status"
        self.Status = case
        try:
            wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo", case=case)
        except Exception, e:
            print "#Error Set Status failed |" + str(e)

    def MainThreadsInitialization(self):

        " Get active threads "
        threads_list = threading.enumerate()
        print threads_list

        " controlThread inputThread MainThread check"
        inputThread_running = False
        controlThread_running = False

        try:
            for i in range(0, len(threads_list)):
                th = threads_list[i]
                if th.name == "ControlThread":
                    print '# Warning: ControlThread already running.'
                    controlThread_running = True

                if th.name == "InputThread":
                    print '# Warning: InputThread already running.'
                    inputThread_running = True


            " Define and Run InputThread and ControThread "
            if not inputThread_running:
                self.InputThread = Thread_InputClass("InputThread", self, self.MainWindow.Coord)
                self.InputThread.start()
            if not controlThread_running:
                self.ControlThread = Thread_ControlClass("ControlThread", self, self.MainWindow.Coord, self.MainWindow.Conf)
                self.ControlThread.start()

            " Define Init Threads "
            for i, J in zip(range(0,self.JointsNum), self.Joints):
                " Define joint init threads "
                self.JointInitThreads[i]     = Thread_JointInitClass("JointInitThread" + str(i), J)
            return True

        except Exception, e:
            print "#Error: Main Threads Initialization failed |" + str(e)
            return False

    def UpdateThreadsInitialization(self):

        " Get active threads "
        threads_list = threading.enumerate()
        print threads_list

        try:
            for i, J in zip(range(0, self.JointsNum), self.Joints):
                if not "JointUpdateThread" + str(i) in threads_list:
                    print 'JointUpdateThread: ', i
                    self.JointUpdateThreads[i] = Thread_JointUpdateClass("JointUpdateThread" + str(i+1), J, self.MainWindow.Coord,
                                                                         self)
                    self.JointUpdateThreads[i].start()
            return True

        except Exception, e:
            print "#Error: Update Threads Initialization failed |" + str(e)
            return False

class PositionClass:
   def __init__(self, Bridge, Name, Jtarget):
       self.Bridge         = Bridge
       self.Name           = Name
       self.JointsNum      = self.Bridge.JointsNum
       self.Jtarget        = Jtarget

class ControlClass:
   def __init__(self, Bridge):

       self.Bridge                 = Bridge
       self.Status                 = IDLE
       self.Input                  = "None"
       self.Positions              = [None]
       self.Listen = 1
       self.FIRST_RUN = True

       " Timing Parameters"
       self.ThreadPeriod           = 0.5
       self.Time                   = 0.2
       self.MaxDegDispl            = 3

       " Max Speed [m/s]"
       self.S                      = 0.02

       " Tollerance sull'errore cartesiano nella cinematica inversa "
       self.Tollerance             = 1e-2 #5e-3
       self.Eps                    = 0.5 #0.2
       " Peso per smorzare la velocita' di giunto vicino alle singolarita'/limiti WS - NB massimo valore 1 "
       self.Wq0s                   = 0.005 #0.2

       " IK parameters "
       self.Dol                    = 5     # gradi di distanza da ROM
       self.Du                     = 0.1   # step to increase/decrease joint limit ramps
       self.Alpha                  = 1
       self.Alpha0                 = 1
       self.IterMax                = 1000
       self.Threshold              = 5   # deg di tolleranza

       self.IKparam = [self.Tollerance, self.Eps, self.Wq0s, self.Dol, self.Du, self.IterMax]

       " ############# "
       " VOCAL CONTROL "
       " ############# "
       self.VocalMaxSteps          = 10

       ' Set in BridgeInputThread '
       self.VocalSteps             = self.VocalMaxSteps
       self.VocalStepsCnt          = 0

   def SetIKparameters(self, IKparameters):

       self.Tollerance = IKparameters[0]
       self.Eps        = IKparameters[1]
       self.Wq0s       = IKparameters[2]
       self.Dol        = IKparameters[3]
       self.Du         = IKparameters[4]
       self.IterMax    = IKparameters[5]

       print '+ New IK Parameters = ', IKparameters

   def SetSpeedGain(self, SpeedGain):

       self.S = SpeedGain
       print '+ New Speed Gain =', self.S

   def SetDisplacement(self, Displacement):

       self.VocalSteps = Displacement
       print '+ New Displacement =', self.VocalSteps

   def SetHMI(self, HMISelection):

       self.Input = self.Bridge.InputList[HMISelection]
       print '+ New HMI =', self.Input

   def SetStatus(self, status):

       self.Status = status
       print '+ New Control Status =', self.Status

class BridgeCoordClass:
   def __init__(self):

       " User input [-1;+1]"
       self.p0                         = [0]*4

       " End effector coordinates (in space) - current "
       self.EndEff_current             = numpy.array([0.0, 0.0, 0.0, 0.0])

       " End effector coordinates (in space) - desired "
       self.EndEff_des                 = numpy.array([0.0, 0.0, 0.0, 0.0])

       " Usato per plot 3D, ma calcolato nel thread di controllo "
       self.Elbow                      = numpy.array([0.0, 0.0, 0.0])

       " Current joints position [deg] "
       self.J_current                  = [0]*5

       " Current joints position [rad] "
       self.J_current_rad              = [0]*5

       " Posizione desiderata dei giunti "
       self.J_des                      = [0]*5

       " Velocita' desiderata dei giunti "
       self.Jv                         = [0]*5

   def Setp0(self, p0):
       self.p0 = p0

class JoystickClass:
   def __init__(self, Bridge):
       " 0: Normale - 1: Advanced "
       self.Bridge             = Bridge
       self.Mode               = 0
       self.Initialized        = False
       self.SavePosition       = 0
       self.GotoSavedPosition  = 0
       self.Alarm              = 0
       #TODO: INIT JOYSTICK Dove va?
       self.Gain               = 1.0
       self.AxisOffset         = [-0.273468017578, -0.257843017578]
       self.CalibrationTmr     = 5000

   def Calibration(self, direction):

       try:
           self.CalibrationThread = Thread_JoystickCalibrationClass("CalibrationThread", self.Bridge, direction)
           self.CalibrationThread.start()

       except Exception, e:
           print "#Error: Joystick Calibration failed |" + str(e)

class SerialClass:
   def __init__(self):
       self.COM            = [None] * 5
       self.Connected      = [False] * 5

       " Flag generale connessione porte seriali "
       self.AllConnected   = False

       " Errore dovuto a un numero non sufficiente di porte seriali o configurazione mancante/sbagliata "
       self.Error          = True

   def availableSerialPort(self):
       suffixes = "S", "USB", "ACM", "AMA"
       nameList = ["COM"] + ["/dev/tty%s" % suffix for suffix in suffixes]
       portList = []
       for name in nameList:
           for number in range(48):
               portName = "%s%s" % (name, number)
               try:
                   serial.Serial(portName).close()
                   portList.append(portName)
               except IOError:
                   pass
       return tuple(portList)

class ExoClass:
   def __init__(self):
       self.Jmin           = [0]*5
       self.Jmax           = [0]*5
       self.Jratio         = [0]*5
       self.Joffset        = [0]*5
       self.Loaded         = False
       self.Filename       = ''

class BridgeConfClass:
    def __init__(self,parent):
       self.Bridge                 = parent
       self.version                = '1.0'
       self.exo_file               = 'Conf.ini'
       self.Serial                 = SerialClass()
       self.Exo                    = ExoClass()

       " Input values timer in milliseconds "
       self.InputValuesRefreshTmr  = 50

       # Parameters
       self.w_plot_joy             = 0
       self.h_plot_joy             = 0


       self.ReadConfFile(self.Bridge)

    def ReadConfFile (self,Bridge):
        self.Bridge = Bridge
        print '* Reading Configuration File ...'
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(self.exo_file)
            section = Config.sections()

            self.Bridge.Patient.Filename      = Config.get(section[0],"FileName")
            self.Bridge.InputList      = Config.get(section[0],"HMI").split(" ")
            self.Serial.COM[0]         = Config.get(section[0],"COM_J1")
            self.Serial.COM[1]         = Config.get(section[0],"COM_J2")
            self.Serial.COM[2]         = Config.get(section[0],"COM_J3")
            self.Serial.COM[3]         = Config.get(section[0],"COM_J4")
            self.Serial.COM[4]         = Config.get(section[0],"COM_J5")

            self.Exo.Jmin[0]            = int(Config.get(section[0],"J1_min"))
            self.Exo.Jmin[1]            = int(Config.get(section[0],"J2_min"))
            self.Exo.Jmin[2]            = int(Config.get(section[0],"J3_min"))
            self.Exo.Jmin[3]            = int(Config.get(section[0],"J4_min"))
            self.Exo.Jmin[4]            = int(Config.get(section[0],"J5_min"))

            self.Exo.Jmax[0]            = int(Config.get(section[0],"J1_max"))
            self.Exo.Jmax[1]            = int(Config.get(section[0],"J2_max"))
            self.Exo.Jmax[2]            = int(Config.get(section[0],"J3_max"))
            self.Exo.Jmax[3]            = int(Config.get(section[0],"J4_max"))
            self.Exo.Jmax[4]            = int(Config.get(section[0],"J5_max"))

            self.Exo.Jratio[0]          = float(Config.get(section[0],"J1_ratio"))
            self.Exo.Jratio[1]          = float(Config.get(section[0],"J2_ratio"))
            self.Exo.Jratio[2]          = float(Config.get(section[0],"J3_ratio"))
            self.Exo.Jratio[3]          = float(Config.get(section[0],"J4_ratio"))
            self.Exo.Jratio[4]          = float(Config.get(section[0],"J5_ratio"))

            self.Exo.Joffset[0]         = int(Config.get(section[0],"J1_offset"))
            self.Exo.Joffset[1]         = int(Config.get(section[0],"J2_offset"))
            self.Exo.Joffset[2]         = int(Config.get(section[0],"J3_offset"))
            self.Exo.Joffset[3]         = int(Config.get(section[0],"J4_offset"))
            self.Exo.Joffset[4]         = int(Config.get(section[0],"J5_offset"))

        except Exception, e:
            print '# Error: ReadConfFile failed | ' + str(e)
            # Read conf failed -> create a new configuration file

    def SavePath(self, filename):

        Config = ConfigParser.ConfigParser()
        Config.optionxform = str
        Config.read(self.exo_file)
        section = Config.sections()
        Config.set(section[0], 'FileName', filename)
        cfgfile = open(self.exo_file,'w')
        Config.write(cfgfile)
        cfgfile.close()

    def ParseExoFile (self, filename):
        try:
            Exo         = ExoClass()
            Config      = ConfigParser.ConfigParser()
            Config.read(filename)
            section     = Config.sections()

            Exo.Jmin[0]            = int(Config.get(section[0],"J1_min"))
            Exo.Jmin[1]            = int(Config.get(section[0],"J2_min"))
            Exo.Jmin[2]            = int(Config.get(section[0],"J3_min"))
            Exo.Jmin[3]            = int(Config.get(section[0],"J4_min"))
            Exo.Jmin[4]            = int(Config.get(section[0],"J5_min"))

            Exo.Jmax[0]            = int(Config.get(section[0],"J1_max"))
            Exo.Jmax[1]            = int(Config.get(section[0],"J2_max"))
            Exo.Jmax[2]            = int(Config.get(section[0],"J3_max"))
            Exo.Jmax[3]            = int(Config.get(section[0],"J4_max"))
            Exo.Jmax[4]            = int(Config.get(section[0],"J5_max"))

            Exo.Jratio[0]          = float(Config.get(section[0],"J1_ratio"))
            Exo.Jratio[1]          = float(Config.get(section[0],"J2_ratio"))
            Exo.Jratio[2]          = float(Config.get(section[0],"J3_ratio"))
            Exo.Jratio[3]          = float(Config.get(section[0],"J4_ratio"))
            Exo.Jratio[4]          = float(Config.get(section[0],"J5_ratio"))

            Exo.Joffset[0]         = int(Config.get(section[0],"J1_offset"))
            Exo.Joffset[1]         = int(Config.get(section[0],"J2_offset"))
            Exo.Joffset[2]         = int(Config.get(section[0],"J3_offset"))
            Exo.Joffset[3]         = int(Config.get(section[0],"J4_offset"))
            Exo.Joffset[4]         = int(Config.get(section[0],"J5_offset"))

            return Exo

        except Exception, e:
            print '# Error: ReadExoFile failed | ' + str(e)
            # Read conf failed -> create a new configuration file
            return False

    def WriteConfFile (self):

        print 'WriteConfFile called.'

        try:
            Config = ConfigParser.ConfigParser()
            Config.optionxform = str
            section = 'BRIDGE'
            Config.add_section(section)

            Config.set(section, 'FileName', self.Bridge.Patient.Filename)
            Config.set(section, 'HMI', 'Joystick Keyboard')
            Config.set(section, 'COM_J1', self.Serial.COM[0])
            Config.set(section, 'COM_J2', self.Serial.COM[1])
            Config.set(section, 'COM_J3', self.Serial.COM[2])
            Config.set(section, 'COM_J4', self.Serial.COM[3])
            Config.set(section, 'COM_J5', self.Serial.COM[4])

            Config.set(section, 'J1_min', self.Exo.Jmin[0])
            Config.set(section, 'J2_min', self.Exo.Jmin[1])
            Config.set(section, 'J3_min', self.Exo.Jmin[2])
            Config.set(section, 'J4_min', self.Exo.Jmin[3])
            Config.set(section, 'J5_min', self.Exo.Jmin[4])

            Config.set(section, 'J1_max', self.Exo.Jmax[0])
            Config.set(section, 'J2_max', self.Exo.Jmax[1])
            Config.set(section, 'J3_max', self.Exo.Jmax[2])
            Config.set(section, 'J4_max', self.Exo.Jmax[3])
            Config.set(section, 'J5_max', self.Exo.Jmax[4])

            Config.set(section, 'J1_ratio', self.Exo.Jratio[0])
            Config.set(section, 'J2_ratio', self.Exo.Jratio[1])
            Config.set(section, 'J3_ratio', self.Exo.Jratio[2])
            Config.set(section, 'J4_ratio', self.Exo.Jratio[3])
            Config.set(section, 'J5_ratio', self.Exo.Jratio[4])

            Config.set(section, 'J1_offset', self.Exo.Joffset[0])
            Config.set(section, 'J2_offset', self.Exo.Joffset[1])
            Config.set(section, 'J3_offset', self.Exo.Joffset[2])
            Config.set(section, 'J4_offset', self.Exo.Joffset[3])
            Config.set(section, 'J5_offset', self.Exo.Joffset[4])

            cfgfile = open(self.exo_file,'w')
            Config.write(cfgfile)
            cfgfile.close()
            return True
        except Exception, e:
            print '# Error: couldn\'t save exoskeleton configuration | ' + str(e)
            return False



    def SavePatient (self, Filename, Patient):

        print '* Saving Patient Configuration File ...'

        try:
            Config = ConfigParser.ConfigParser()
            Config.optionxform = str
            section = 'BRIDGE-PATIENT'
            Config.add_section(section)

            Config.set(section, 'Name', Patient.Name)

            Config.set(section, 'J1_min', Patient.Jmin[0])
            Config.set(section, 'J2_min', Patient.Jmin[1])
            Config.set(section, 'J3_min', Patient.Jmin[2])
            Config.set(section, 'J4_min', Patient.Jmin[3])
            Config.set(section, 'J5_min', Patient.Jmin[4])

            Config.set(section, 'J1_max', Patient.Jmax[0])
            Config.set(section, 'J2_max', Patient.Jmax[1])
            Config.set(section, 'J3_max', Patient.Jmax[2])
            Config.set(section, 'J4_max', Patient.Jmax[3])
            Config.set(section, 'J5_max', Patient.Jmax[4])

            Config.set(section, 'J1_default', Patient.Jdef[0])
            Config.set(section, 'J2_default', Patient.Jdef[1])
            Config.set(section, 'J3_default', Patient.Jdef[2])
            Config.set(section, 'J4_default', Patient.Jdef[3])
            Config.set(section, 'J5_default', Patient.Jdef[4])

            Config.set(section, 'J1_rest', Patient.Jrest[0])
            Config.set(section, 'J2_rest', Patient.Jrest[1])
            Config.set(section, 'J3_rest', Patient.Jrest[2])
            Config.set(section, 'J4_rest', Patient.Jrest[3])
            Config.set(section, 'J5_rest', Patient.Jrest[4])

            Config.set(section, 'l1', Patient.l1)
            Config.set(section, 'l2', Patient.l2)
            Config.set(section, 'l3', Patient.l3)

            cfgfile = open(Filename,'w')
            Config.write(cfgfile)
            cfgfile.close()

            return True
        except Exception, e:
            print '# Error: Saving Patient failed | ' + str(e)
            return False


