# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import time
import threading
import datetime
import numpy
import math

import BridgeGUI
from Bridge            import *
from BridgeDialog      import *
from BridgeControl     import *
from BridgeJoint       import *
from BridgeInput       import *

from BridgeRecorder    import Thread_RecordClass

import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher

import serial

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import get_test_data
import matplotlib.animation as animation
from matplotlib.patches import Ellipse, Polygon
from matplotlib import cm
#import subprocess
import scipy.io as spio
import winsound

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
RETRIEVE_POSITION   = 10



" ############# "
" # GUI CLASS # "
" ############# "

class MainWindow(BridgeGUI.BridgeWindow):
    def __init__(self, parent):

        BridgeGUI.BridgeWindow.__init__(self, parent)

        # Define bridge configurations
        self.Coord = BridgeCoordClass()
        self.Bridge = BridgeClass(self)
        self.Conf   = BridgeConfClass(self.Bridge)

        if self.Bridge.Patient.ReadPatientFile(self.Bridge.Patient.Filename):
            self.Bridge.Patient.Loaded = True
        else:
            self.Bridge.Patient.Loaded = False

        " Initialize plots "
        self.exo3d_plot     = CreatePlot3DExo(self.exo3d_container,self.Bridge)
        self.ani            = animation.FuncAnimation(self.exo3d_plot.figure, self.Animate, fargs=[], interval = 500)

        " Initialize plots "
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths([-23,-3,-3,-3])
        self.statusbar.SetStatusText('Ready', 0)
        self.statusbar.SetStatusText('COM: -', 1)
        self.statusbar.SetStatusText('Patient: None', 2)
        self.statusbar.SetStatusText('Joystick: None', 3)

        self.Jdesc_lbl          = [self.J1desc_lbl, self.J2desc_lbl, self.J3desc_lbl, self.J4desc_lbl, self.J5desc_lbl]
        self.Jvalue_lbl         = [self.J1value_lbl, self.J2value_lbl, self.J3value_lbl, self.J4value_lbl, self.J5value_lbl]

        for i, lbl in zip(range(0, len(self.Jvalue_lbl)), self.Jvalue_lbl):
            lbl.Name = str(i)

        self.Jmin_lbl           = [self.J1min_lbl, self.J2min_lbl, self.J3min_lbl, self.J4min_lbl, self.J5min_lbl]
        self.Jmax_lbl           = [self.J1max_lbl, self.J2max_lbl, self.J3max_lbl, self.J4max_lbl, self.J5max_lbl]
        self.Jdef_lbl           = [self.J1def_lbl, self.J2def_lbl, self.J3def_lbl, self.J4def_lbl, self.J5def_lbl]
        self.Jinitialized_lbl   = [self.J1initialized_lbl, self.J2initialized_lbl, self.J3initialized_lbl, self.J4initialized_lbl, self.J5initialized_lbl]
        self.Jboundaries_lbl    = [self.J1boundaries_lbl, self.J2boundaries_lbl, self.J3boundaries_lbl, self.J4boundaries_lbl, self.J5boundaries_lbl]
        self.Jfault_lbl         = [self.J1fault_lbl, self.J2fault_lbl, self.J3fault_lbl, self.J4fault_lbl, self.J5fault_lbl]
        self.Ctrl_lbl           = [self.ctrlIDLE_lbl, self.ctrlINIT_lbl, self.ctrlDONNING_lbl, self.ctrlRESTPOS_lbl, self.ctrlREADY_lbl, self.ctrlRUNNING_lbl, self.ctrlSTOP_lbl]
        self.button_list        = [self.disconnect_butt, self.init_butt, self.disableCtrl_butt, self.enableCtrl_butt, self.stop_butt, self.savePos_butt, self.gotoPos_butt]
        self.IKparam_list       = [self.m_tollerance_entry, self.m_epsilon_entry, self.m_wq0s_entry, self.m_dol_entry, self.m_du_entry, self.m_itermax_entry]

        for lbl in self.Jvalue_lbl:
            lbl.Bind( wx.EVT_LEFT_DCLICK, self.open_jointDialog_command )

        for item in self.button_list:
            item.Disable()
        self.connect_butt.Enable()
        self.stop_butt.Enable()

        input_choiceChoices = self.Bridge.InputList

        self.input_choice.Clear()
        self.input_choice.AppendItems(input_choiceChoices)
        self.input_choice.SetSelection(0)
        self.UpdateIKparam()

        Publisher.subscribe(self.UpdateJointsInfo,      "UpdateJointsInfo")
        Publisher.subscribe(self.ShowDonningDialog,     "ShowDonningDialog")
        Publisher.subscribe(self.UpdateControlInfo,     "UpdateControlInfo")
        Publisher.subscribe(self.UpdateInputInfo,       "UpdateInputInfo")
        Publisher.subscribe(self.UpdateSavedPositions,  "UpdateSavedPositions")
        Publisher.subscribe(self.UpdateIKparam,         "UpdateIKparam")
        Publisher.subscribe(self.ShowDialogError,       "ShowDialogError")
        Publisher.subscribe(self.ShowDialogAlert,       "ShowDialogAlert")
        Publisher.subscribe(self.StartTimer,            "StartTimer")

        " Create timer function - Update input values "
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateInputValues, self.timer)


    " ################### "
    " #### PUBLISHER #### "
    " ################### "

    def StartTimer(self,msg):
        self.timer.Start(msg)

    def ShowDialogError (self, msg):
        dialog = DialogError(self, msg)
        dialog.ShowModal()
        return

    def ShowDialogAlert (self, msg):
        dialog = DialogAlert(self, msg)
        dialog.ShowModal()
        return

    def ShowDonningDialog (self):
        if self.Bridge.Status != DONNING:
            dialog = DialogError(self, "Donning Failed")
            dialog.ShowModal()
            return

        dialog = DialogDonning(self)
        if dialog.ShowModal() == wx.ID_OK:
            self.Bridge.SetStatus(REST_POSITION)
        else:
            dialog = DialogError(self, "System Locked")
            dialog.ShowModal()
            return

    def UpdateControlInfo (self, case):

        " Update Status Info "

        if case == NONE:

            " Lock Buttons"
            for item in self.button_list:
                item.Disable()
            self.connect_butt.Enable()
            self.stop_butt.Enable()

            " Update statubar "
            self.statusbar.SetStatusText('Disconnected', 0)
            print "+ New Status = NONE"

        else:

            for i, lbl in zip(range(0, len(self.Ctrl_lbl)), self.Ctrl_lbl):
                if case == i:

                    if i != len(self.Ctrl_lbl):
                        lbl.SetBackgroundColour((57,232,149))
                    else:
                        lbl.SetBackgroundColour((224,97,97))
                elif case ==  NONE:
                    pass
                else:
                    if i != len(self.Ctrl_lbl):
                        lbl.SetBackgroundColour((242,255,242))
                    else:
                        lbl.SetBackgroundColour((255,232,232))

            if case == IDLE:
                self.connect_butt.Disable()
                self.disconnect_butt.Enable()
                self.init_butt.Enable()
                self.enableCtrl_butt.Enable()
                print "+ New Status = IDLE"

            elif case == INIT_SYSTEM:
                self.connect_butt.Disable()
                self.init_butt.Disable()
                self.disconnect_butt.Enable()
                self.enableCtrl_butt.Enable()
                print "+ New Status = INITIALIZATION"


            elif case == RUNNING:
                self.connect_butt.Disable()
                self.init_butt.Disable()
                self.enableCtrl_butt.Disable()
                self.disconnect_butt.Enable()
                self.disableCtrl_butt.Enable()
                self.savePos_butt.Enable()
                self.gotoPos_butt.Enable()
                print "+ New Status = RUNNING"


            elif case == READY:
                self.enableCtrl_butt.Enable()
                self.disableCtrl_butt.Disable()
                self.connect_butt.Disable()
                self.disconnect_butt.Enable()
                self.init_butt.Disable()
                self.savePos_butt.Disable()
                self.gotoPos_butt.Disable()
                print "+ New Status = READY"


            " Update statubar "
            self.statusbar.SetStatusText('Connected', 0)

        " Force win refresh (background issue) "
        self.Refresh()

    def UpdateInputInfo (self):

        " Set Input Info "
        self.inputDescription_lbl.SetLabel(str(self.Bridge.Control.Input))

        if not self.Bridge.Joystick.Mode:
            self.JoystickModeA_lbl.SetBackgroundColour((57,232,149))
            self.JoystickModeB_lbl.SetBackgroundColour((242,255,242))
        else:
            self.JoystickModeA_lbl.SetBackgroundColour((242,255,242))
            self.JoystickModeB_lbl.SetBackgroundColour((57,232,149))

        if self.Bridge.Joystick.SavePosition:
            self.JoystickSavePos_lbl.SetBackgroundColour((57,232,149))
        else:
            self.JoystickSavePos_lbl.SetBackgroundColour((242,255,242))

        if self.Bridge.Joystick.GotoSavedPosition:
            self.JoystickRecallPos_lbl.SetBackgroundColour((57,232,149))
        else:
            self.JoystickRecallPos_lbl.SetBackgroundColour((242,255,242))


        " Force win refresh (background issue) "
        #self.Refresh()

    def UpdateInputValues (self,msg):

        " Set Input Values "
        self.P0_X_lbl.SetLabel("%.2f" % self.Coord.p0[0])
        self.P0_Y_lbl.SetLabel("%.2f" % self.Coord.p0[1])
        self.P0_Z_lbl.SetLabel("%.2f" % self.Coord.p0[2])
        self.P0_PS_lbl.SetLabel("%.2f" % self.Coord.p0[3])

    def UpdateJointsInfo (self):

        for i, Joint in zip( range(0,self.Bridge.JointsNum), self.Bridge.Joints ):

            if Joint.Homed:
                self.Jinitialized_lbl[i].SetLabel(u"●")
            else:
                self.Jinitialized_lbl[i].SetLabel(u"○")

            if Joint.Bounded:
                self.Jboundaries_lbl[i].SetLabel(u"●")
            else:
                self.Jboundaries_lbl[i].SetLabel(u"○")
            try:
                self.Jvalue_lbl[i].SetLabel(str(int(Joint.Position)))
                self.Jmin_lbl[i].SetLabel(str(int(Joint.Jmin)))
                self.Jmax_lbl[i].SetLabel(str(int(Joint.Jmax)))
            except:
                self.Jvalue_lbl[i].SetLabel("N.A.")


    def UpdateIKparam(self):

        " Update IK parameters "

        for i, lbl in zip(range(0,len(self.IKparam_list)), self.IKparam_list):
            lbl.SetLabel(str(self.Bridge.Control.IKparam[i]))

    def UpdateSavedPositions(self):

        " Update Saved Positions "

        self.SavedPositions_list.Clear()
        for i, Position in zip(range(0,len(self.Bridge.SavedPositions)), self.Bridge.SavedPositions):
            self.SavedPositions_list.Append(Position.Name)
            self.SavedPositions_list.SetSelection(i)


    def Animate(self, i):

        self.exo3d_plot.line.set_data([0, self.Coord.Elbow[0], self.Coord.EndEff_current[0]], [0, self.Coord.Elbow[1], self.Coord.EndEff_current[1]])
        self.exo3d_plot.line.set_3d_properties([0, self.Coord.Elbow[2], self.Coord.EndEff_current[2]])
        self.exo3d_plot.line2.set_data(self.Coord.EndEff_des[0], self.Coord.EndEff_des[1])
        self.exo3d_plot.line2.set_3d_properties(self.Coord.EndEff_des[2])

        # self.joystick_plot.line.set_data([0, p_elbow[0,i], EndEff0[0,i]], [0, p_elbow[1,i], EndEff0[1,i]])
        # for j, self.joystick_plot.line in enumerate(lines):
        #offset = [120, 120]

        '''
        offset = [self.Conf.w_plot_joy/2, self.Conf.h_plot_joy/2]
        self.joystick_plot.line.set_data([offset[0]+offset[0]*self.Coord.p0[1], offset[0]+offset[0]*self.Coord.p0[1]], [offset[1]+offset[1]*self.Coord.p0[0], offset[1]+offset[1]*self.Coord.p0[0]])
        
        if abs(self.Coord.p0[1]) > 0.4 and abs(self.Coord.p0[0]) > 0.4:
            self.joystick_plot.line.set_data([offset[0]+offset[0]*self.Coord.p0[0]*0.7, offset[0]+offset[0]*self.Coord.p0[0]*0.7], [offset[1]-offset[1]*self.Coord.p0[1]*0.7, offset[1]-offset[1]*self.Coord.p0[1]*0.7])
        else:
            self.joystick_plot.line.set_data([offset[0]+offset[0]*self.Coord.p0[0], offset[0]+offset[0]*self.Coord.p0[0]], [offset[1]-offset[1]*self.Coord.p0[1], offset[1]-offset[1]*self.Coord.p0[1]])

        if self.Coord.p0[2] >= 0.4:
            self.joystick_plot.line.set_markerfacecolor([1, 0, abs(self.Coord.p0[2])])
        elif self.Coord.p0[2] <= -0.4:
            self.joystick_plot.line.set_markerfacecolor([0, abs(self.Coord.p0[2]), 0])
        else:
            self.joystick_plot.line.set_markerfacecolor('black')
        
        #marker_style = dict(linestyle='-', color='red', markersize=15)
        #lines = [plt.plot([], [], marker='o', **marker_style)[0] for _ in range(N)]
        
    
        self.joystick_plot.figure.canvas.draw()
        
        for jj in range(0,self.monitorJoint_grid.GetNumberRows()):
            self.monitorJoint_grid.SetCellValue(jj, 1, str("{0:.3f}".format(round(self.Coord.J_current[jj],3))))
            self.monitorCtrl_grid.SetCellValue(jj, 1, str("{0:.3f}".format(round(self.Coord.Jv[jj],3))))
            self.monitorJoint_grid.SetCellValue(jj, 5, str("{0:.3f}".format(round(self.Coord.SavedPos[jj],3))))
        '''

    def BridgeInitialization(self):

        " Joints Init "
        for i in range(0, self.Bridge.JointsNum):
            self.Bridge.Joints[i]   = Joint(i+1,
                                            self.Conf.Serial.COM[i],
                                            self.Bridge.Patient,
                                            self.Conf.Exo,
                                            self.Coord)

        " Copy patient to Bridge "
        #self.Bridge.Patient         = self.Conf.Patient

        return True


    " ################## "
    " ####   MENU   #### "
    " ################## "

    def exo_setup_command (self, event):
        dialog = DialogExoSetup(self, self.Conf, self.Bridge)

        if dialog.ShowModal() == wx.ID_OK:
            self.Conf.Serial.Error = False

    def patient_setup_command (self, event):
        dialog = DialogPatientSetup(self, self.Bridge, self.Conf)

        if dialog.ShowModal() == wx.ID_OK:
            " Update joint values "
            for i, Jmin, Jmax, Jdef in zip(range(0,5), self.Jmin_lbl, self.Jmax_lbl, self.Jdef_lbl):
                Jmin.SetLabel(str(self.Bridge.Patient.Jmin[i]))
                Jmax.SetLabel(str(self.Bridge.Patient.Jmax[i]))
                Jdef.SetLabel(str(self.Bridge.Patient.Jdef[i]))

            if self.Conf.Serial.AllConnected:
	            " Update patient ROM values "
	            for i in range (0, self.Bridge.JointsNum):
    	        	self.Bridge.Joints[i].SetRange(self.Bridge.Patient.Jmin[i], self.Bridge.Patient.Jmax[i])

            " Update input description "
            self.inputDescription_lbl.SetLabel(str(self.Bridge.Control.Input))

            self.statusbar.SetStatusText('Patient: Loaded', 2)

    def joystick_calibration_command( self, event ):

        if self.Bridge.Joystick.Initialized:
    	    dialog= DialogJoystickCalibration(self, self.Conf, self.Bridge)
    	    dialog.ShowModal()
        else:
            print "# Warning: Joystick not initialized"
            dialog = DialogAlert(self, "# Warning: Joystick not initialized")
            dialog.ShowModal()


    " ################## "
    " #### COMMANDS #### "
    " ################## "

    def connect_command(self, event):

        " Verifico che le il file paziente sia stato caricato "
        if not self.Bridge.Patient.Loaded:
            dialog = DialogError(self, "Patient not loaded.")
            dialog.ShowModal()
            return

        " Verifico che le porte seriali siano state correttamente impostate "
        if not __debug__:
            if self.Conf.Serial.Error:
                dialog = DialogError(self, "Serial COM error.\nCheck preferences dialog.")
                dialog.ShowModal()
                return
        else:
            self.Conf.Serial.Error = False

        " Init Joints and threads "
        if not self.BridgeInitialization():
            dialog = DialogError(self, "Error: Bridge initialization failed.")
            dialog.ShowModal()
            return
        if not self.Bridge.MainThreadsInitialization():
            dialog = DialogError(self, "Error: Threads initialization failed.")
            dialog.ShowModal()
            return

        if not __debug__:

            " Open Serial Ports "
            try:
                for i, J in zip(range(0, len(self.Bridge.Joints)), self.Bridge.Joints):
                    if J.OpenPort():
                        print '+ %s Connected' % J.CommPort
                        self.Conf.Serial.Connected[i] = True
                    else:
                        print '- Error: couldn\'t open %s.' % J.CommPort

            except:
                print "#Error: could not open %s." % J.CommPort
                dialog = DialogError(self, "Error: COM init failed.")
                dialog.ShowModal()
                return

            " Check if all COM are Connected "

        if all(i == True for i in self.Conf.Serial.Connected[0:self.Bridge.JointsNum]) or  __debug__:

            self.Bridge.SetStatus(IDLE)
            " Start Timer for UpdateInputInfo"
            self.StartTimer(self.Conf.InputValuesRefreshTmr)

        else:

            " Update statubar "
            self.statusbar.SetStatusText('Connection error', 0)

            if not __debug__:
                try:
                    " Close serial ports previously open "
                    for i, J in zip(range(0,self.Bridge.JointsNum), self.Bridge.Joints):
                        if self.Conf.Serial.Connected[i]:
                            J.ClosePort()
                            print '+ %s Disconnected' % J.CommPort
                            self.Conf.Serial.Connected[i] = False
                        else:
                            print '- Error: couldn\'t close %s.' % J.CommPort
                except Exception, e:
                    print 'Error  ' + str(e)

        self.set_control_interface(event)

    def disconnect_command (self, event):

        " Get active threads "
        threads_list = threading.enumerate()
        print threads_list

        " Kill all the threads except MainThread "

        print "* Terminating Threads ..."
        for i in range(0, len(threads_list)):
            th = threads_list[i]
            if th.name != "MainThread" :
                try:
                    th.terminate()
                    th.join()
                except Exception, e:
                    print "#Error terminating " + th.name + " | " + str(e)

        if not __debug__:
            try:
                print "* Closing Serial Ports ..."
                for i, J in zip(range(0,self.Bridge.JointsNum), self.Bridge.Joints):
                    if self.Conf.Serial.Connected[i]:
                        while not J.FlushPort():
                            time.sleep(0.1)
                        while not J.ClosePort():
                            time.sleep(0.1)
                        print '+ %s Closed' % J.CommPort
                        self.Conf.Serial.Connected[i] = False
                    else:
                        print '- Error: couldn\'t close %s.' % J.CommPort
            except Exception, e:
                print str(e)

        self.Bridge.SetStatus(NONE)

        self.Bridge.MainWindow.timer.Stop()

    def initialize_system_command (self, event):

        try:
            " Update control status "
            if not __debug__:
                self.Bridge.SetStatus(INIT_SYSTEM)
            else:
                self.Bridge.SetStatus(READY)

        except Exception, e:
            dialog = DialogError(self, "System initialization failed.")
            dialog.ShowModal()
            print " #Error: Inizialization failed " + str(e)
            return

    def enable_control_command (self, event):

        " Verifica ROM giunti paziente & Run update threads "
        for i in range(0, self.Bridge.JointsNum):
            self.Bridge.Joints[i].Jmin = self.Bridge.Patient.Jmin[i]
            self.Bridge.Joints[i].Jmax = self.Bridge.Patient.Jmax[i]

        if not __debug__:
            " Run JointUpdateThreads "
            if not self.Bridge.UpdateThreadsInitialization():
                dialog = DialogError(self, "Error: Threads initialization failed.")
                dialog.ShowModal()
                return

        " Start Saving Thread "

        self.RecordThread = Thread_RecordClass("RecordThread", self.Bridge, self.Coord)
        self.RecordThread.start()

        " Set Status "
        self.Bridge.SetStatus(RUNNING)

        " Set control status "
        self.Bridge.Control.Status = POS_CTRL

        self.Bridge.Control.FirstRun = True

    def disable_control_command (self, events):

        threads_list= threading.enumerate()

        "Kill all the threads"

        print "* Terminating JointUpdateThreads ..."
        for i in range(0, len(threads_list)):
            th = threads_list[i]
            if th.name != "MainThread" and th.name != "ControlThread" and th.name != "InputThread":
                try:
                    th.terminate()
                    th.join()
                except Exception, e:
                    print "#Error terminating " + th.name + " | " + str(e)

        " Change Status "
        self.Bridge.SetStatus(READY)
        self.Bridge.Control.Status = IDLE

    def stop_command (self, event):

        if self.Bridge.Control.Input == 'Joystick':
            print '+ Joystick Button'
            if self.Bridge.Joystick.Mode == 0:
                self.Bridge.Joystick.Mode = 1
            else:
                self.Bridge.Joystick.Mode = 0

        " Update input info in main window "
        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")

    def exit (self,event):
        " Kill all the threads except MainThread "

        " Get active threads "
        threads_list = threading.enumerate()
        print threads_list

        print "* Terminating Threads ..."
        for i in range(0, len(threads_list)):
            th = threads_list[i]
            if th.name != "MainThread":
                try:
                    th.terminate()
                    th.join()
                except Exception, e:
                    print "# Error terminating " + th.name + " | " + str(e)

        if not __debug__:
            try:
                print "* Closing Serial Ports ..."
                for i, J in zip(range(0, self.Bridge.JointsNum), self.Bridge.Joints):
                    if self.Conf.Serial.Connected[i]:
                        while not J.FlushPort():
                            time.sleep(0.1)
                        while not J.ClosePort():
                            time.sleep(0.1)
                        print '+ %s Closed' % J.CommPort
                        self.Conf.Serial.Connected[i] = False
                    else:
                        print '# Error: couldn\'t close %s.' % J.CommPort
            except Exception, e:
                print str(e)
        try:
            self.Close()
            print "Closed"
        except Exception, e:
            print "# Error closing | " + str(e)

    def save_position_command(self, event):
        " Save Position"
        try:
            self.Bridge.SavePosition("GUI "+str(len(self.Bridge.SavedPositions)))
            self.UpdateSavedPositions()
        except Exception, e:
            dialog = DialogError(self, "Save Position failed.")
            dialog.ShowModal()
            print "#Error Save Position Failed|" + str(e)

    def goto_position_command (self, event):
        "GoTo Position"
        try:
            Selection = self.SavedPositions_list.GetSelection()
            if Selection == -1:
                dialog = DialogError(self, "Please Save Position first")
                dialog.ShowModal()
            else:
                self.Bridge.GoToPosition(Selection)
        except Exception, e:
            dialog = DialogError(self, "GoTo Position failed.")
            dialog.ShowModal()
            print "#Error Go To Position Failed|" + str(e)

    def open_jointDialog_command (self, event):

        widget = event.GetEventObject()
        dialog = DialogJoint(self, int(widget.GetName()), self.Bridge.Joints[int(widget.GetName())], self.Bridge.Status)
        dialog.ShowModal()

    def set_control_interface (self,event):
        "Set Control Interface "
        try:
            self.Bridge.Control.SetHMI(self.input_choice.GetSelection())
            self.UpdateInputInfo()
            self.inputDescription_lbl.SetLabel(str(self.Bridge.Control.Input))
        except Exception, e:
            print '#Error: Set Control Interface failed |' + str(e)
            return

    def set_displacement(self, event):
        "Set Displacement Step for Vocal Control"
        try:
            self.Bridge.Control.SetDisplacement(self.displacement_entry.GetValue())
        except Exception, e:
            print '#Error: Set Displacement failed |' + str(e)
            return

    def set_speed_gain(self, event):
        "Set Speed Gain"
        try:
            self.Bridge.Control.SetSpeedGain(float(self.speed_gain_entry.GetValue())/100)
        except Exception, e:
            print '#Error: Set Speed Gain failed |' + str(e)
            return

    def save_ik_parameters( self, event ):
        "Set IK Parameters"
        IKparam = [None]*len(self.IKparam_list)
        try:
            for i, lbl in zip(range(0, len(self.IKparam_list)), self.IKparam_list):
                IKparam[i] = float(unicodedata.normalize('NFKD', lbl.GetValue()).encode("ascii", "ignore"))
            self.Bridge.Control.SetIKparameters(IKparam)
        except Exception, e:
            print '#Error: Set IK parameters failed |' + str(e)
            return



" ############## "
" #PLOT 3D EXO # "
" ############## "

class CreatePlot3DExo(wx.Panel):

    def __init__(self, parent, Bridge):
        wx.Panel.__init__(self, parent)

        self.Bridge = Bridge
        self.dpi = 75
        self.dim_pan = parent.GetSize()
        self.figure = Figure(figsize=(self.dim_pan[0] * 1.0 / self.dpi, (self.dim_pan[1]) * 1.0 / self.dpi),
                             dpi=self.dpi)

        sysTextColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        col_norm = (sysTextColour[0] * 1.0 / 255, sysTextColour[1] * 1.0 / 255, sysTextColour[2] * 1.0 / 255)

        self.figure.patch.set_facecolor(col_norm)

        # Canvas
        self.canvas = FigureCanvas(parent, -1, self.figure)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.canvas, 1, wx.ALL | wx.EXPAND)

        self.ax = self.figure.add_subplot(1, 1, 1, projection='3d')
        self.ax.axis('equal')

        self.ax.set_xlim3d(-(self.Bridge.Patient.l1 + self.Bridge.Patient.l2 + self.Bridge.Patient.l3),
                           (self.Bridge.Patient.l1 + self.Bridge.Patient.l2 + self.Bridge.Patient.l3))
        self.ax.set_ylim3d(-(self.Bridge.Patient.l1 + self.Bridge.Patient.l2 + self.Bridge.Patient.l3),
                           (self.Bridge.Patient.l1 + self.Bridge.Patient.l2 + self.Bridge.Patient.l3))
        self.ax.set_zlim3d(-(self.Bridge.Patient.l1 + self.Bridge.Patient.l2 + self.Bridge.Patient.l3),
                           (self.Bridge.Patient.l1 + self.Bridge.Patient.l2 + self.Bridge.Patient.l3))

        marker_style = dict(linestyle='-', color=[0.2, 0.2, 0.2], markersize=20)
        self.line = self.ax.plot([], [], [], marker='o', **marker_style)[0]
        marker_style2 = dict(linestyle='-', color='red', markersize=15)
        self.line2 = self.ax.plot([], [], [], marker='o', **marker_style2)[0]

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # self.ax.set_xticklabels([])
        # self.ax.set_yticklabels([])
        # self.ax.set_zticklabels([])

        self.ax.view_init(elev=50., azim=50)
        # self.ax.view_init(elev=0, azim=270)

        parent.SetSizer(sizer1)
        parent.Fit()

'########'
'# MAIN #'
'########'

print 'Debug Mode: ',__debug__

# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
app = wx.App(False)

# create an object
frame = MainWindow(None)

# show the frame
frame.Show(True)

# start the applications
app.MainLoop()