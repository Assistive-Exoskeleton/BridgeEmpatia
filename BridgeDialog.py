# -*- coding: utf-8 -*-
# !/usr/bin/env python


import os
import sys

import BridgeGUI

import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher


import unicodedata

from Bridge import *
from BridgeJoint import *
from BridgeInput import *


" ######################## "
" Dialog Exoskeleton Setup "
" ######################## "

class DialogExoSetup(BridgeGUI.DialogExoSetup):
    def __init__(self, parent, Conf, Bridge):
        BridgeGUI.DialogExoSetup.__init__(self, parent)

        self.Conf = Conf
        self.Bridge = Bridge
        self.Error = False

        self.Jmin_entry_list = [self.J1min_entry, self.J2min_entry, self.J3min_entry, self.J4min_entry, self.J5min_entry]
        self.Jmax_entry_list = [self.J1max_entry, self.J2max_entry, self.J3max_entry, self.J4max_entry, self.J5max_entry]
        self.Joffset_entry_list = [self.J1offset_entry, self.J2offset_entry, self.J3offset_entry, self.J4offset_entry, self.J5offset_entry]
        self.Jratio_entry_list = [self.J1ratio_entry, self.J2ratio_entry, self.J3ratio_entry, self.J4ratio_entry, self.J5ratio_entry]

        " Motor plot choice "
        self.choice_COM_list = [self.choice_COM_M1, self.choice_COM_M2, self.choice_COM_M3, self.choice_COM_M4, self.choice_COM_M5]

        " Test button list "
        self.test_button_list = [self.J1test_butt, self.J2test_butt, self.J3test_butt, self.J4test_butt, self.J5test_butt]

        for i, but in zip(range(0, len(self.test_button_list)), self.test_button_list):
            " Set widget name - Index number "
            but.Name = str(i)

        " Get available serial port "
        self.portList = self.Conf.Serial.availableSerialPort()

        if len(self.portList) < 5:
            self.error_lbl.SetLabel("Error: not enough serial COM")
            self.Error = True

        for i, choice in zip(range(0, 6), self.choice_COM_list):

            for j in range(0, len(self.portList)):
                choice.Append(self.portList[j])

            # Try to set COM from conf
            try:
                choice.SetSelection(self.portList.index(self.Conf.Serial.COM[i]))
            except:
                choice.SetSelection(0)

        for i, Jmin, Jmax, Joffset, Jratio in zip(range(0, 5), self.Jmin_entry_list, self.Jmax_entry_list,
                                                  self.Joffset_entry_list, self.Jratio_entry_list):
            Jmin.SetValue(str(self.Conf.Exo.Jmin[i]))
            Jmax.SetValue(str(self.Conf.Exo.Jmax[i]))
            Joffset.SetValue(str(self.Conf.Exo.Joffset[i]))
            Jratio.SetValue(str(self.Conf.Exo.Jratio[i]))

    def ok_command(self, event):

        " get serial port only if no error condition occurs "
        if not self.Error:
            for isig, choice_COM in zip(range(0, 5), self.choice_COM_list):
                self.Conf.Serial.COM[isig] = self.portList[choice_COM.GetSelection()]

        for isig, Jmin, Jmax, Joffset, Jratio in zip(range(0, 5), self.Jmin_entry_list, self.Jmax_entry_list,
                                                     self.Joffset_entry_list, self.Jratio_entry_list):
            " Remove accents and get values "
            self.Conf.Exo.Jmin[isig] = int(unicodedata.normalize('NFKD', Jmin.GetValue()).encode("ascii", "ignore"))
            self.Conf.Exo.Jmax[isig] = int(unicodedata.normalize('NFKD', Jmax.GetValue()).encode("ascii", "ignore"))
            self.Conf.Exo.Joffset[isig] = int(
                unicodedata.normalize('NFKD', Joffset.GetValue()).encode("ascii", "ignore"))
            self.Conf.Exo.Jratio[isig] = float(
                unicodedata.normalize('NFKD', Jratio.GetValue()).encode("ascii", "ignore"))

        self.Conf.Exo.Loaded = True

        self.Conf.WriteConfFile()

        self.EndModal(wx.ID_OK)
        self.Destroy()

    def cancel_command(self, event):
        self.Destroy()

    def test_command(self, event):
        " Get widget "
        widget = event.GetEventObject()

        " Get COM "
        serialcom = self.portList[self.choice_COM_list[int(widget.GetName())].GetSelection()]
        '''
        joint = Joint(   0,         # Num
                        serialcom,  # COM
                        5,          # Max
                        -5,         # Min
                        75,         # Ratio
                        0,          # Offset
                        0,          # Default
                        None)       # Coord
        '''
        PatientEs = PatientClass()
        ExoEs = ExoClass()

        joint = Joint(0,  # Num
                      serialcom,  # COM
                      PatientEs,  # Ratio
                      ExoEs,  # offset
                      None)  # Coord

        " Open serial port "
        if not joint.OpenPort():
            dialog = DialogError(self, "Unable to open %s" % serialcom)
            dialog.ShowModal()
            return

        " Clear drive error & Run test motor "
        jointDriveErrorClear()
        ret = joint.MotorTest()

        " Close serial port "
        if not joint.ClosePort():
            dialog = DialogError(self, "Unable to close %s" % serialcom)
            dialog.ShowModal()
            return

        if ret:
            dialog = DialogError(self, "Test procedure done")
            dialog.ShowModal()
        else:
            error = ''
            if joint.Timeout:
                error = ' | Timeout occurred'

            dialog = DialogError(self, "Test procedure failed %s" % error)
            dialog.ShowModal()


" #################### "
" Dialog Patient Setup "
" #################### "

class DialogPatientSetup(BridgeGUI.Dialog_PatientSetup):
    def __init__(self, parent, Bridge, Conf):
        BridgeGUI.Dialog_PatientSetup.__init__(self, parent)

        self.Filename = None
        self.Bridge = Bridge
        self.Conf   = Conf

        self.Jmin_entry_list = [self.J1min_entry, self.J2min_entry, self.J3min_entry, self.J4min_entry,
                                self.J5min_entry]
        self.Jmax_entry_list = [self.J1max_entry, self.J2max_entry, self.J3max_entry, self.J4max_entry,
                                self.J5max_entry]
        self.Jdef_entry_list = [self.J1def_entry, self.J2def_entry, self.J3def_entry, self.J4def_entry,
                                self.J5def_entry]
        self.Jrest_entry_list = [self.J1rest_entry, self.J2rest_entry, self.J3rest_entry, self.J4rest_entry,
                                 self.J5rest_entry]

        self.joystick_list = [self.joystick_forward_lbl, self.joystick_backward_lbl, self.joystick_left_lbl, self.joystick_right_lbl]

        if self.Bridge.Patient.Loaded:

            self.patientName_entry.SetValue(self.Bridge.Patient.Name)

            for i, Jmin, Jmax, Jdef, Jrest in zip(range(0, 5), self.Jmin_entry_list, self.Jmax_entry_list,
                                                  self.Jdef_entry_list, self.Jrest_entry_list):
                Jmin.SetValue(str(self.Bridge.Patient.Jmin[i]))
                Jmax.SetValue(str(self.Bridge.Patient.Jmax[i]))
                Jdef.SetValue(str(self.Bridge.Patient.Jdef[i]))
                Jrest.SetValue(str(self.Bridge.Patient.Jrest[i]))

            self.l1_lbl.SetValue(str(self.Bridge.Patient.l1))
            self.l2_lbl.SetValue(str(self.Bridge.Patient.l2))
            self.l3_lbl.SetValue(str(self.Bridge.Patient.l3))

            for i, Joystick in zip(range(0,4),self.joystick_list):
                Joystick.SetValue("%.4f" % self.Bridge.Patient.JoystickCalibration[i])

        else:
            for Jmin, Jmax, Jdef, Jrest in zip(self.Jmin_entry_list, self.Jmax_entry_list, self.Jdef_entry_list,
                                               self.Jrest_entry_list):
                Jmin.SetValue('N.A.')
                Jmax.SetValue('N.A.')
                Jdef.SetValue('N.A.')
                Jrest.SetValue('N.A.')

            for l in self.l_entry_list:
                l.SetValue('N.A.')

        Publisher.subscribe(self.UpdateJoystickCalibrationInfo, "UpdateJoystickCalibrationInfo")

    def ok_command(self, event):

        for isig, Jmin, Jmax, Jdef, Jrest in zip(range(0, 5), self.Jmin_entry_list, self.Jmax_entry_list,
                                                 self.Jdef_entry_list, self.Jrest_entry_list):
            " Remove accents and get values "
            self.Bridge.Patient.Jmin[isig]  = int(unicodedata.normalize('NFKD', Jmin.GetValue()).encode("ascii", "ignore"))
            self.Bridge.Patient.Jmax[isig]  = int(unicodedata.normalize('NFKD', Jmax.GetValue()).encode("ascii", "ignore"))
            self.Bridge.Patient.Jdef[isig]  = int(unicodedata.normalize('NFKD', Jdef.GetValue()).encode("ascii", "ignore"))
            self.Bridge.Patient.Jrest[isig] = int(unicodedata.normalize('NFKD', Jrest.GetValue()).encode("ascii", "ignore"))

        self.Bridge.Patient.l1 = float(unicodedata.normalize('NFKD', self.l1_lbl.GetValue()).encode("ascii", "ignore"))
        self.Bridge.Patient.l2 = float(unicodedata.normalize('NFKD', self.l2_lbl.GetValue()).encode("ascii", "ignore"))
        self.Bridge.Patient.l3 = float(unicodedata.normalize('NFKD', self.l3_lbl.GetValue()).encode("ascii", "ignore"))



        " Save patient name "
        self.Bridge.Patient.Name = unicodedata.normalize('NFKD', self.patientName_entry.GetValue()).encode("ascii",
                                                                                                         "ignore")
        " Save patient input "
        self.Bridge.Patient.Loaded = True

        self.EndModal(wx.ID_OK)
        self.Destroy()

    def save_command(self, event):
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        dlg = wx.FileDialog(self, "Choose a File:", wildcard="INI files (*.ini)|*.ini", defaultDir=path,
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            " Get filename "
            self.Filename = dlg.GetPath()

            " Create local patient "
            Patient = PatientClass()

            " Get values from entries "
            for isig, Jmin, Jmax, Jdef, Jrest in zip(range(0, 5), self.Jmin_entry_list, self.Jmax_entry_list,
                                                     self.Jdef_entry_list, self.Jrest_entry_list):
                " Remove accents and get values "
                Patient.Jmin[isig]  = int(unicodedata.normalize('NFKD', Jmin.GetValue()).encode("ascii", "ignore"))
                Patient.Jmax[isig]  = int(unicodedata.normalize('NFKD', Jmax.GetValue()).encode("ascii", "ignore"))
                Patient.Jdef[isig]  = int(unicodedata.normalize('NFKD', Jdef.GetValue()).encode("ascii", "ignore"))
                Patient.Jrest[isig] = int(unicodedata.normalize('NFKD', Jrest.GetValue()).encode("ascii", "ignore"))

            Patient.l1 = float(unicodedata.normalize('NFKD', self.l1_lbl.GetValue()).encode("ascii", "ignore"))
            Patient.l2 = float(unicodedata.normalize('NFKD', self.l2_lbl.GetValue()).encode("ascii", "ignore"))
            Patient.l3 = float(unicodedata.normalize('NFKD', self.l3_lbl.GetValue()).encode("ascii", "ignore"))

            for isig, Joystick in zip(range(0,4), self.joystick_list):
                Patient.JoystickCalibration[isig] = float(unicodedata.normalize('NFKD', Joystick.GetValue()).encode("ascii", "ignore"))

            " get patient name "
            Patient.Name = unicodedata.normalize('NFKD', self.patientName_entry.GetValue()).encode("ascii", "ignore")

            " Save patient file"
            self.Bridge.Patient.SavePatient(self.Filename, Patient)
            self.Conf.SavePath(self.Filename)

    def cancel_command(self, event):
        self.Destroy()

    def load_command(self, event):

        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # otherwise ask the user what new file to open
        dlg = wx.FileDialog(self, "Choose a File:", wildcard="INI files (*.ini)|*.ini", defaultDir=path,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            " Get selected file "
            self.Filename = dlg.GetPath()
            self.Conf.SavePath(self.Filename)

            try:

                Patient = self.Bridge.Patient.ParsePatientFile(self.Filename)

                self.patientName_entry.SetValue(Patient.Name)

                for i, Jmin, Jmax, Jdef, Jrest in zip(range(0, 5), self.Jmin_entry_list, self.Jmax_entry_list,
                                                      self.Jdef_entry_list, self.Jrest_entry_list):
                    Jmin.SetValue(str(Patient.Jmin[i]))
                    Jmax.SetValue(str(Patient.Jmax[i]))
                    Jdef.SetValue(str(Patient.Jdef[i]))
                    Jrest.SetValue(str(Patient.Jrest[i]))

                self.l1_lbl.SetValue(str(Patient.l1))
                self.l2_lbl.SetValue(str(Patient.l2))
                self.l3_lbl.SetValue(str(Patient.l3))

                for i, Joystick in zip(range(0, 4), self.joystick_list):
                    Joystick.SetValue("%.4f" % Patient.JoystickCalibration[i])

            except Exception, e:
                print '# Error ' + str(e)
                self.Filename = None
                pass

    def joystick_calibration_command( self, event ):

        if self.Bridge.Joystick.Initialized:
    	    dialog= DialogJoystickCalibration(self, self.Conf, self.Bridge)
    	    dialog.ShowModal()
        else:
            print "# Warning: Joystick not initialized"
            dialog = DialogAlert(self, "# Warning: Joystick not initialized")
            dialog.ShowModal()

    def UpdateJoystickCalibrationInfo(self):
        try:
            for i, Joystick in zip(range(0, 4), self.joystick_list):
                Joystick.SetValue("%.4f" % self.Bridge.Patient.JoystickCalibration[i])
        except Exception, e:
            print "# Error | " + str(e)



" ########################### "
" Dialog Joystick Calibration "
" ########################### "
class DialogJoystickCalibration(BridgeGUI.Dialog_JoystickCalibration):

    def __init__(self, parent, Conf, Bridge):

        BridgeGUI.Dialog_JoystickCalibration.__init__(self, parent)

        self.Conf = Conf
        self.Bridge = Bridge

        self.calib_buttlist = [self.calib_butt1, self.calib_butt2, self.calib_butt3, self.calib_butt4]
        self.JoystickCalibration_lbl = [self.JoystickCalibration0_lbl, self.JoystickCalibration1_lbl, self.JoystickCalibration2_lbl, self.JoystickCalibration3_lbl]
        self.JoystickCalibrationValues_lbl = [self.JoystickCalibrationValues0_lbl, self.JoystickCalibrationValues1_lbl, self.JoystickCalibrationValues2_lbl, self.JoystickCalibrationValues3_lbl]
        self.UpdateJoystickCalibrationInfo()
        Publisher.subscribe(self.UpdateJoystickCalibrationInfo, "UpdateJoystickCalibrationInfo")

        for i, but in zip(range(0, len(self.calib_buttlist)), self.calib_buttlist):
            " Set widget name - Index number "
            but.Name = str(i)

    def joystick_calibration_command_axis(self, event):

        widget = event.GetEventObject()
        print widget.GetName()
        direction = int(widget.GetName())

        if self.Bridge.Control.Input == 'Joystick':

            if direction == 0:
                self.dialog = DialogAlert(self, 'Please, push the joystick forward as much as you can')
            elif direction == 1:
                self.dialog = DialogAlert(self, 'Please, push the joystick backward as much as you can')
            elif direction == 2:
                self.dialog = DialogAlert(self, 'Please, push the joystick left as much as you can')
            else:
                self.dialog = DialogAlert(self, 'Please, push the joystick right as much as you can')


            print "* Calibrating Joystick ..."

            self.Bridge.Joystick.Calibration(direction)

            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.end_calibration, self.timer)
            self.timer.Start(self.Bridge.Joystick.CalibrationTmr)

            self.dialog.ShowModal()

        else:

            dialog = DialogError(self, 'Please, select the joystick as control modality')
            dialog.ShowModal()

    def end_calibration(self, msg):
        try:
            self.Bridge.Joystick.CalibrationThread.terminate()
            self.timer.Stop()
            self.dialog.Destroy()
        except Exception, e:
            print "#Error | " + str(e)

    def ok_command(self,event):
        try:
            self.Destroy()
            wx.CallAfter(Publisher.sendMessage, "UpdateJoystickCalibrationInfo")
        except Exception, e:
            print "# Error | " + str(e)

    def UpdateJoystickCalibrationInfo (self):

        for i in range(0,len(self.Bridge.Patient.JoystickCalibration)):
            if self.Bridge.Patient.JoystickCalibration[i] != 1.0:
                self.JoystickCalibration_lbl[i].SetLabel(u"●")
                self.JoystickCalibrationValues_lbl[i].SetLabel("%.4f" % self.Bridge.Patient.JoystickCalibration[i])


" ############ "
" Dialog Error "
" ############ "

class DialogError(BridgeGUI.Dialog_Error):
    def __init__(self, parent, error):
        BridgeGUI.Dialog_Error.__init__(self, parent)
        self.error_lbl.SetLabel(error)

    def cancel_command(self, event):
        self.Destroy()


" ############ "
" Dialog Alert "
" ############ "

class DialogAlert(BridgeGUI.Dialog_Alert):

    def __init__(self, parent, message):
        BridgeGUI.Dialog_Alert.__init__(self, parent)
        self.alert_lbl.SetLabel(message)

    def cancel_command(self, event):
        self.Destroy()


" ############ "
" Dialog Joint "
" ############ "

class DialogJoint(BridgeGUI.Dialog_Joint):
    def __init__(self, parent, Num, Joint, Status):
        BridgeGUI.Dialog_Joint.__init__(self, parent)

        self.Joint = Joint
        self.Status = Status

        self.Joint.Position = self.Joint.GetPositionDeg()
        wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")

        if self.Joint:
            # self.angle_entry.SetValue(str(self.Joint.Position))
            self.angle_entry.SetValue(str(int(self.Joint.Position)))
        else:
            self.angle_entry.SetValue('0')

        self.joint_lbl.SetLabel('J' + str(Num + 1))

    def plus_command(self, event):
        self.angle = int(self.angle_entry.GetValue()) + 1

        self.angle_entry.SetValue(str(self.angle))

    def minus_command(self, event):
        self.angle = int(self.angle_entry.GetValue()) - 1

        self.angle_entry.SetValue(str(self.angle))

    def go_command(self, event):
        if not self.Joint:
            self.error_lbl.SetLabel('Joint not initialized')
        elif self.Status != READY:
            self.error_lbl.SetLabel('System status error')
        else:
            self.Joint.SetAbsolutePositionMode()
            if self.Joint.SetPositionDeg(self.angle):

                while abs(self.Joint.GetPositionDeg() - self.angle) > 0.5:
                    print '**** I am going to the requested position, J%d - %d' % (
                    self.Joint.Num, self.Joint.GetPositionDeg())
                    time.sleep(1)

            self.Joint.Position = self.Joint.GetPositionDeg()
            wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")

    def cancel_command(self, event):
        self.Destroy()



" ############## "
" Dialog Donning "
" ############## "

class DialogDonning(BridgeGUI.DialogDonning):
    def      __init__(self, parent):
        BridgeGUI.DialogDonning.__init__(self, parent)

    def ok_command(self, event):
        self.EndModal(wx.ID_OK)
        self.Destroy()
