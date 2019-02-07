# -*- coding: utf-8 -*-
#!/usr/bin/env python

import threading
import time
import pygame
import keyboard
import math
import os

from Bridge import *
#from BridgeDialog import *
import winsound     # Audio Feedback
import subprocess
#from BridgeDialog import *
from BridgeGUI import Dialog_Error
#from BridgeDialog import DialogError
import BridgeGUI

import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher

import speech_recognition as sr

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
RECALL_POSITION   = 10


" ################################ "
" # JOYSTICK UPDATE THREAD CLASS # "
" ################################ "

class Thread_InputClass(threading.Thread):
    def __init__(self, Name, Bridge, Coord):

        threading.Thread.__init__(self, name=Name)
        self.Running            = False
        self.Name               = Name
        self.Bridge             = Bridge
        self.Coord              = Coord

        self.AudioPath          = os.getcwd() + '\\Assets\\Audio\\'

        self.PyJoystick         = None

        self.VocalCmd           = None

        self.PositionName       = ""
        self.PositionNum        = ""


        " Variabili per il riconoscimento vocale "
        self.r                          = sr.Recognizer()
        #self.r.energy_threshold         = 2000
        self.r.dynamic_energy_threshold = False


        " Variabili per il controllo dei cicli "
        self.VOCAL_IDLE                 = 0
        self.VOCAL_RUNNING_CONFERMATION = 1     # wait for running confermation
        self.VOCAL_RUNNING              = 2
        self.VOCAL_STOP_CONFERMATION    = 3     # wait for running confermation
        self.VOCAL_HELP                 = 4
        self.VOCAL_SAVE_POSITION        = 5
        self.VOCAL_SAVE_POSITION_NAME   = 6
        self.VOCAL_CONFIRM_POSITION_NAME= 7
        self.VOCAL_RECALL_POSITION    = 8

        self.VocalStatus                = self.VOCAL_IDLE

        " Variabili per controllo 'step' "
        self.VocalSteps                 = self.Bridge.Control.VocalMaxSteps
        self.Step_Param                  = [1, 5, 20]
        self.Speed_Param                 = [0.01, 0.02, 0.04]

        self.var_mem                    = ['','','','','']
        self.NumVarMem                  = 0
        self.vm                         = 4*[0]

        " Dizionari "
        self.instr_dict    = {'fer':'fermo', 'rip':'riposo', 'mem':'memorizza', 'dor':'dormi', 'ter':'termina', 'ric':'richiama'}
        self.direction_dict = {'si':[0,0.5,0,0], 'de':[0,-0.5,0,0], 'sa':[0,0,0.5,0], 'sc':[0,0,-0.5,0], 'av':[0.5,0,0,0], 'in':[-0.5,0,0,0]}
        self.step_dict      = {'spostamento picc': self.Step_Param[0], 'spostamento medi': self.Step_Param[1], 'spostamento gran': self.Step_Param[2]}
        self.speed_dict = {'velocità picc': self.Speed_Param[0], 'velocità medi': self.Speed_Param[1], 'velocità gran': self.Speed_Param[2]}

    def run(self):

        print '* Input Thread Run'


        " Human-Machine Interfaces Initialization"

        for i in range(len(self.Bridge.InputList)):  # InputList is defined a priori in Conf.ini (HMIs to be used)

            if self.Bridge.InputList[i] == 'Joystick':
                print '+ Joystick Interface'
                try:
                    " Init pygame "
                    pygame.init()

                    " Count available joysticks "
                    if pygame.joystick.get_count() == 0:
                        print '# Warning: Joystick missing'
                        wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg = "# Warning: Joystick missing")
                        return

                    " Init Joystick "
                    pygame.display.init()
                    pygame.joystick.init()
                    self.PyJoystick = pygame.joystick.Joystick(0)
                    self.PyJoystick.init()
                    self.Bridge.Joystick.Initialized = True

                except Exception, e:

                    print '# Error: Pygame initialization failed | ' + str(e)
                    wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg = "# Error: Pygame initialization failed")
                    self.Bridge.Joystick.Initialized = False
                    return

            elif self.Bridge.InputList[i] == 'Vocal':
                print '+ Vocal Interface'
                " Introduzione controllo vocale "

                try:
                    with sr.Microphone() as source:
                        self.r.adjust_for_ambient_noise(source)
                    # winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                    # au_file = audio_file+'Jarvis.wav'
                    # return_code = subprocess.call(["afplay", au_file])

                except Exception, e:
                    print '# Error: Init Embedded Vocal failed' + str(e)
                    " Update input info in main window "
                    return False

            elif self.Bridge.InputList[i] == 'Visual':
                print '+ Visual Interface'
                pass
            
            elif self.Bridge.InputList[i] == 'Keyboard':
                print '+ Keyboard Interface'
                pass

                " Update input info in main window "

            else:
                print '# Error: Not implemented interface: ' + self.Bridge.InputList[i]
                wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg = "# Error: Not implemented interface")

        " Update input info in main window "
        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")

        self.Running = True

        while self.Running:

            if self.Bridge.Control.Input == "Joystick" and self.Bridge.Joystick.Initialized:

                self.Bridge.Control.FIRST_RUN = 1
                self.VocalStatus = self.VOCAL_IDLE
                events = pygame.event.get()

                " If a joystick event occurred "
                for event in events:
                    if event.type == pygame.QUIT:
                        self.terminate()

                    elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:

                        self.Bridge.Joystick.SavePosition      = self.PyJoystick.get_button(2)
                        self.Bridge.Joystick.GotoSavedPosition = self.PyJoystick.get_button(3)
                        self.Bridge.Joystick.Alarm             = self.PyJoystick.get_button(4)
                        wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")

                        if self.PyJoystick.get_button(0):

                            if self.Bridge.Joystick.Mode:
                                self.Bridge.Joystick.Mode = 0
                                print '* Change Plane Button: X-Y'
                                winsound.Beep(880, 500)

                            else:
                                self.Bridge.Joystick.Mode = 1
                                print '* Change Plane Button: Z'
                                winsound.Beep(440, 500)

                            if self.Bridge.Status == RECALL_POSITION:
                                self.Bridge.SetStatus(RUNNING)
                                self.Bridge.Control.SetStatus(POS_CTRL)
                                for i in range(0, self.Bridge.JointsNum):
                                    self.Bridge.Joints[i].TargetDone = True

                        if self.PyJoystick.get_button(2):


                            try:
                                num = len(self.Bridge.SavedPositions)
                                name = "Joystick " + str(num)
                                self.Bridge.SavePosition(name)
                                wx.CallAfter(Publisher.sendMessage, "UpdateSavedPositions")
                            except Exception, e:
                                print "#Error Save Position Failed | " + str(e)
                            winsound.Beep(880, 500)
                            time.sleep(0.500)
                            winsound.Beep(880, 500)
                            time.sleep(0.500)

                        if self.PyJoystick.get_button(3):



                            try:
                                self.Bridge.GoToPosition(len(self.Bridge.SavedPositions)-1)
                            except Exception, e:
                                print "#Error Go To Position Failed | " + str(e)

                            winsound.Beep(880, 500)
                            time.sleep(0.500)
                            winsound.Beep(880, 500)
                            time.sleep(0.500)
                            winsound.Beep(880, 500)
                            time.sleep(0.500)

                        if self.PyJoystick.get_button(4):

                            print "Alarm"
                            self.Bridge.MainWindow.disable_control_command(self)
                            self.Bridge.SetStatus(ERROR)
                            winsound.Beep(880, 1000)

                    elif event.type == pygame.JOYAXISMOTION:

                        for i in range (0,2):
                            axis = - ( self.PyJoystick.get_axis(i) - self.Bridge.Joystick.AxisOffset[i])
                            #axis = self.PyJoystick.get_axis(i)
                            " Remove Deadband"
                            if abs(axis) < 0.01:
                                axis = 0.0

                            " Calibrated Joystick Acquisition " # 0:Forward 1:Backward 2:Right 3:Left
                            # Z axis
                            if self.Bridge.Joystick.Mode:

                                self.Coord.p0[0] = 0.0
                                self.Coord.p0[1] = 0.0

                                if i == 1:  # Z axis
                                    if axis > 0:
                                        self.Coord.p0[2] = axis/self.Bridge.Patient.JoystickCalibration[0] # Upward
                                    else:
                                        self.Coord.p0[2] = axis/self.Bridge.Patient.JoystickCalibration[1]  # Downward
                                else:       # Theta 5
                                    self.Coord.p0[3] = 0

                            # X-Y axis
                            else:

                                if i == 1: # X axis
                                    if axis > 0:
                                        self.Coord.p0[0] = axis/self.Bridge.Patient.JoystickCalibration[0]  # Forward
                                    else:
                                        self.Coord.p0[0] = axis/self.Bridge.Patient.JoystickCalibration[1]  # Backward
                                else: # Y axis
                                    if axis < 0:
                                        self.Coord.p0[1] = -axis/self.Bridge.Patient.JoystickCalibration[2] # Left
                                    else:
                                        self.Coord.p0[1] = -axis/self.Bridge.Patient.JoystickCalibration[3] # Right

                                self.Coord.p0[2] = 0.0
                                self.Coord.p0[3] = 0.0




                pygame.event.clear()

            elif self.Bridge.Control.Input == "Vocal":

                if self.Bridge.Control.FIRST_RUN:

                    " Introduzione controllo vocale "
                    winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                    # au_file = audio_file+'Jarvis.wav'
                    # return_code = subprocess.call(["afplay", au_file])

                    self.Bip()
                    self.Bridge.Control.FIRST_RUN = False
                else:
                    " Get command "
                    print "Listening on Laptop... "
                    self.VocalCmd = self.WaitForInstructions()
                    self.VocalCmd = self.VocalCmd.lower()
                    print "Recognized : ", self.VocalCmd

                    " ################### "
                    " VOCAL STATE MACHINE "
                    " ################### "

                    if self.VocalCmd[0:4] == 'aiut':
                        self.VocalCmd = ""
                        print '* Alarm! '
                        self.Bridge.MainWindow.disable_control_command(self)
                        self.Bridge.SetStatus(ERROR)
                        winsound.Beep(880, 1000)
                        self.VocalStatus = self.VOCAL_IDLE

                    elif 'termina' in self.VocalCmd:
                        self.VocalCmd = ""
                        self.VocalStatus = self.VOCAL_STOP_CONFERMATION
                        winsound.PlaySound(self.AudioPath + 'ConfermaSpegnimento.wav', winsound.SND_FILENAME)
                        # au_file = audio_file+'ConfermaSpegnimento.wav'
                        # return_code = subprocess.call(["afplay", au_file])
                        self.Bip()

                    elif self.VocalStatus == self.VOCAL_IDLE:

                        if 'attiva' in self.VocalCmd:

                            winsound.PlaySound(self.AudioPath + 'ConfermaAttivazione.wav', winsound.SND_FILENAME)
                            print "vero o falso?"
                            self.VocalCmd=""
                            # au_file = audio_file + 'ConfermaAttivazione.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_RUNNING_CONFERMATION

                        elif 'dormi' in self.VocalCmd:
                            self.VocalCmd = ""
                            self.VocalStatus = self.VOCAL_IDLE

                    elif self.VocalStatus == self.VOCAL_RUNNING_CONFERMATION:

                        if self.VocalCmd == 'ok':
                            self.VocalCmd = ""
                            print '*** CONTROLLO VOCALE ATTIVATO ***'
                            winsound.PlaySound(self.AudioPath + 'SonoAttivo.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'SonoAttivo.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_RUNNING

                        elif self.VocalCmd == 'falso':
                            self.VocalCmd = ""
                            print '*** CONTROLLO VOCALE DISATTIVATO ***'
                            winsound.PlaySound(self.AudioPath + 'Dormi2.wav', winsound.SND_FILENAME)
                            # au_file = audio_file + 'Dormi2.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_IDLE

                        elif not self.VocalCmd == "":

                            print '*** COMANDO VOCALE NON VALIDO ***'
                            self.VocalCmd = ""
                            winsound.PlaySound(self.AudioPath + 'IstruzioneNonValida.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'IstruzioneNonValida.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()
                            pass

                    elif self.VocalStatus == self.VOCAL_RUNNING:

                        if 'dormi' in self.VocalCmd:
                            winsound.PlaySound(self.AudioPath + 'Dormi.wav', winsound.SND_FILENAME)
                            self.VocalStatus = self.VOCAL_IDLE

                        elif 'memo' in self.VocalCmd:
                            winsound.PlaySound(self.AudioPath + 'Memorizza.wav', winsound.SND_FILENAME)
                            self.VocalStatus = self.VOCAL_SAVE_POSITION

                        elif 'richiama' in self.VocalCmd:
                            winsound.PlaySound(self.AudioPath + 'RipetiNuovaPosizione1.wav', winsound.SND_FILENAME)
                            self.VocalStatus = self.VOCAL_RECALL_POSITION

                            " Parse command "
                        elif not self.VocalCmd == "":
                            self.CommandRecognition(self.VocalCmd)

                        self.Bip()
                        self.VocalCmd = ""

                    elif self.VocalStatus == self.VOCAL_SAVE_POSITION:

                        if 'ok' in self.VocalCmd:
                            winsound.PlaySound(self.AudioPath + 'NomeNuovaPosizione.wav', winsound.SND_FILENAME)
                            self.VocalStatus = self.VOCAL_SAVE_POSITION_NAME

                        elif 'falso' in self.VocalCmd:
                            self.VocalStatus = self.VOCAL_RUNNING

                        self.Bip()
                        self.VocalCmd = ""


                    elif self.VocalStatus == self.VOCAL_SAVE_POSITION_NAME:

                        self.PositionName = self.VocalCmd.upper()
                        winsound.PlaySound(self.AudioPath + 'RipetiNuovaPosizione2.wav', winsound.SND_FILENAME)
                        self.VocalStatus = self.VOCAL_CONFIRM_POSITION_NAME
                        self.Bip()

                    elif self.VocalStatus == self.VOCAL_CONFIRM_POSITION_NAME:

                        if self.VocalCmd.upper() == self.PositionName and self.PositionName.upper() != "RECOGNITION FAILED":
                            self.Bridge.SavePosition(self.PositionName)
                            wx.CallAfter(Publisher.sendMessage, "UpdateSavedPositions")
                            winsound.PlaySound(self.AudioPath + 'NuovaPosizioneMemorizzata.wav', winsound.SND_FILENAME)
                        else:
                            winsound.PlaySound(self.AudioPath + 'ImpossibileMemorizzare.wav', winsound.SND_FILENAME)
                        self.VocalStatus = self.VOCAL_RUNNING


                    elif self.VocalStatus == self.VOCAL_RECALL_POSITION:

                        for i, Position in zip(range(0, len(self.Bridge.SavedPositions)), self.Bridge.SavedPositions):
                            if Position.Name.lower() in self.VocalCmd:
                                self.PositionNum = i
                                self.PositionName = self.VocalCmd
                                print self.PositionName

                                self.Bridge.GoToPosition(self.PositionNum)
                                wx.CallAfter(Publisher.sendMessage, "UpdateSavedPositions")

                        self.Bip()
                        self.VocalStatus = self.VOCAL_RUNNING


                    elif self.VocalStatus == self.VOCAL_STOP_CONFERMATION:
                        if self.VocalCmd == 'ok':
                            self.VocalCmd = ""
                            print '*** CONTROLLO VOCALE TERMINATO ***'
                            winsound.PlaySound(self.AudioPath + 'Spegnimento.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'Spegnimento.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()

                            self.VocalStatus = self.VOCAL_IDLE
                            self.Bridge.Control.Input = "Joystick"
                            #self.terminate()

                        elif self.VocalCmd == 'falso':
                            self.VocalCmd = ""
                            print '*** CONTROLLO VOCALE ATTIVO ***'
                            winsound.PlaySound(self.AudioPath + 'Jarvis.wav', winsound.SND_FILENAME)
                            # au_file = audio_file+'Dormi2.wav'
                            # return_code = subprocess.call(["afplay", au_file])
                            self.Bip()
                            self.VocalStatus = self.VOCAL_IDLE
                        else:
                            if not self.VocalCmd == "":
                                print '*** COMANDO VOCALE NON VALIDO ***'
                                winsound.PlaySound(self.AudioPath + 'IstruzioneNonValida.wav', winsound.SND_FILENAME)
                                # au_file = audio_file+'IstruzioneNonValida.wav'
                                # return_code = subprocess.call(["afplay", au_file])
                                self.Bip()

                    elif self.VocalStatus == self.VOCAL_HELP:
                        # TODO: VOCAL HELP
                        print 'TODO: VOCAL_HELP'
                        time.sleep(1)

            elif self.Bridge.Control.Input == "Keyboard":

                self.Bridge.Control.FIRST_RUN = 1
                self.VocalStatus = self.VOCAL_IDLE


                if keyboard.is_pressed('up'):
                    self.Coord.p0[0] = 0.5
                elif keyboard.is_pressed('down'):
                    self.Coord.p0[0] = -0.5
                else:
                    self.Coord.p0[0] = 0.0

                if keyboard.is_pressed('left'):
                    self.Coord.p0[1] = 0.5
                elif keyboard.is_pressed('right'):
                    self.Coord.p0[1] = -0.5
                else:
                    self.Coord.p0[1] = 0.0

                if keyboard.is_pressed('w'):
                    self.Coord.p0[2] = 0.5
                elif keyboard.is_pressed('s'):
                    self.Coord.p0[2] = -0.5
                else:
                    self.Coord.p0[2] = 0.0

                if keyboard.is_pressed('q'):
                    self.MainWindow.disable_control_command()

            " Update input info in main window "
            #wx.CallAfter(Publisher.sendMessage, "UpdateInputInfo")
            time.sleep(0.1)

        print '- Input Thread Out'

    " Funzione di riconoscimento dei comandi che può essere personalizzata -> customizzazione "

    def CommandRecognition(self, instr):

        " instr_dict "
        # 'fer': 'fermo'
        # 'rip': 'riposo'
        # 'mem': 'memorizza'
        # 'dor': 'dormi'

        " direction_dict "
        # 'sin':[-1, 0, 0, 0]
        # 'des':[ 1, 0, 0, 0]
        # 'sal':[ 0, 0,-1, 0]
        # 'sce':[ 0, 0, 1, 0]
        # 'ava':[ 0,-1, 0, 0]
        # 'ind':[ 0, 1, 0, 0]

        " step_dict "
        # 'spostamento picc': self.Step_Param[0]
        # 'spostamento medi': self.Step_Param[1]
        # 'spostamento gran': self.Step_Param[2]


        self.Coord.p0                       = [0,0,0,0]
        self.Bridge.Control.VocalStepsCnt   = 0

        #self.VocalCmd = None

        if instr[0:3] in self.instr_dict:
            
            " ############## "
            " VOCAL COMMANDS "
            " ############## "
            
            self.VocalCmd   = self.instr_dict[instr[0:3]]

        elif instr[0:2] in self.direction_dict:

            " ########## "
            " DIRECTIONS "
            " ########## "

            " Rest VocalComand "
            self.VocalCmd   = ""
            " Update p0 coordinates "
            self.Coord.p0   = self.direction_dict[instr[0:2]]

        elif instr[0:16] in self.step_dict:
            " ##### "
            " STEPS "
            " ##### "
            self.Bridge.Control.VocalSteps = self.step_dict[instr[0:16]]
            print 'Numero di step selezionati: ', self.Bridge.Control.VocalSteps

        elif not instr== "" :
            print '*** Istruzione non valida ***'
            self.VocalCmd=""
            #winsound.PlaySound('IstruzioneNonValida.wav', winsound.SND_FILENAME)
            # au_file = audio_file+'IstruzioneNonValida.wav'
            # return_code = subprocess.call(["afplay", au_file])
            #self.Bip()

    def WaitForInstructions(self):

        with sr.Microphone() as source:
            try:
                cmd = self.r.listen(source, phrase_time_limit = 2)
                print '+ Microphone Record called.'
                #cmd = self.r.record(source, duration=2)
                self.Bridge.Control.SetStatus(POS_CTRL)

                # metto al massimo il numero di step fatti così interrompo il ciclo
                #ALE
                self.Bridge.Control.VocalStepsCnt = self.Bridge.Control.VocalSteps

                try:
                    print '+ Recognize Google called.'
                    instruction = self.r.recognize_google(cmd, language = "it-IT")
                except Exception, e:
                    instruction = 'Recognition Failed'
                    print '# ERROR: Speech Recognition Failed ' + str(e)

                return instruction

            except Exception, e:
                instruction = 'Listen Failed'
                print str(e)

    def Bip(self):
        Freq    = 700 # Set Frequency To 2500 Hertz
        Dur     = 950 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur)

    def terminate(self):
        " Exit the thread "
        try:
            pygame.quit()
        except Exception, e:
            print "# Error Terminate pygame | " + str(e)
        self.Running = False


" ############################## "
" # JOYSTICK CALIBRATION CLASS # "
" ############################## "

class Thread_JoystickCalibrationClass(threading.Thread):

    def __init__(self, Name, Bridge, direction):

        threading.Thread.__init__(self, name = Name)
        self.Running                = False
        self.Bridge                 = Bridge
        self.direction              = direction
        self.direction_list         = ["Forward", "Backward", "Left", "Right"]

    def run(self):

        self.Running = True



        if self.direction <= 1:
            i=1
        else:
            i=0
        print self.direction

        #self.Bridge.Patient.JoystickCalibration[self.direction] = 0
        temp = 0

        try:

            self.PyJoystick = pygame.joystick.Joystick(0)
            self.PyJoystick.init()

            while self.Running:

                axis = - (self.PyJoystick.get_axis(i) - self.Bridge.Joystick.AxisOffset[i])

                if abs(axis) > temp:

                    temp = abs(axis)

            print self.direction_list[self.direction] + ': ' + str(temp)
            self.Bridge.Patient.JoystickCalibration[self.direction] = temp

            self.Bridge.Patient.SavePatient(self.Bridge.Patient.Filename, self.Bridge.Patient)

            wx.CallAfter(Publisher.sendMessage, "UpdateJoystickCalibrationInfo")

        except Exception, e:

            print '# ERROR: Joystick failure | ' + str(e)
            wx.CallAfter(Publisher.sendMessage, "ShowDialogError", msg="# Error: Joystick failure")
            self.Running = False
            return

    def terminate(self):

        self.Running = False
