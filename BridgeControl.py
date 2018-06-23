# -*- coding: utf-8 -*-
import threading, time
from serial import *
import math
from numpy.linalg import inv
import math
import numpy
from Bridge import *
import scipy.io as spio
import datetime
import winsound # per audio feedback

import wx
from wx.lib.wordwrap import wordwrap
#from wx.lib.pubsub import setuparg1 #evita problemi con py2exe
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher

from Bridge import *
from BridgeJoint import *

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
TARGET_POSITION     = 10

'''
global file_EndEff0
file_EndEff0 = []
global file_EndEff_des
file_EndEff_des = []
global file_J_current
file_J_current = []
global file_J_des
file_J_des = []
global file_p0
file_p0_ = []
global file_elbow
file_elbow = []
'''

class Thread_ControlClass(threading.Thread):
    def __init__(self, Name, Bridge, Coord, Conf, CheckWs=False):

        threading.Thread.__init__(self, name=Name)
        self.Running            = False
        self.Name               = Name
        self.Coord              = Coord
        self.Bridge             = Bridge

        self.CheckWS            = CheckWs




    def run(self):

        print '* Control Thread Run'

        if __debug__:
            self.Coord.J_current = self.Bridge.Patient.Jrest

        self.Running = True

        while self.Running:


            " ############# "
            " STATE MACHINE "
            " ############# "

            if self.Bridge.Status == IDLE:
                time.sleep(0.2)

            elif self.Bridge.Status == INIT_SYSTEM:

                " Initialize Joints "

                " Initialize joint 1 - Start init thread "
                self.Bridge.JointInitThreads[1].start()

                " Wait for the joint to get to the home position "
                while self.Bridge.Joints[1].Homed is False:
                    " Keep escape chance "
                    if not self.Running:
                        break

                    time.sleep(0.5)

                " Update graphics in main window "
                wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")
                
                " Initialize all the remaining joints - Start init threads "
                
                for initThread in self.Bridge.JointInitThreads:
                    if initThread.Name != "JointInitThread1":
                        initThread.start()

                #TODO: da riscrivere in modo pitonico "

                while self.Bridge.Joints[0].Homed == False or self.Bridge.Joints[1].Homed == False or self.Bridge.Joints[2].Homed == False or self.Bridge.Joints[3].Homed == False:

                    " Keep escape chance "
                    if not self.Running:
                        break

                    " Update graphics in main window "
                    wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")

                    time.sleep(0.5)

                
                " All the joints are initialized and in home position - change control status "
                self.Bridge.Status = DONNING

                time.sleep(0.1)

                " Update graphics in main window "
                wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")

                " Call donning dialog "
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo", case = self.Bridge.Status)
                wx.CallAfter(Publisher.sendMessage, "ShowDonningDialog")

            elif self.Bridge.Status == DONNING:
                time.sleep(0.5)

            elif self.Bridge.Status == REST_POSITION:

                " Status where the initialization of the system is done, but the ctrl is NOT enabled "
                #self.Bridge.Control.Status = POS_CTRL_ABS
                
                arrigon         = []
                arrigon_thread  = []

                for i, J in zip(range(0, self.Bridge.JointsNum), self.Bridge.Joints):
                    # arrigon.append(self.Bridge.Joints[i].RestDone)
                    arrigon_thread.append(Thread_JointTargetPositionClass("JointTargetPositionThread" + str(i), J))

                " Run all the threads "
                for thread in arrigon_thread:
                    thread.start()

                while 1 and self.Running:
                    ''' MARTA: da ripristinare per Giunto 3
                    " Wait for all flags to be true - molto pitonico! "
                    if all(i == True for i in arrigon):
                        break
                    '''
                    if self.Bridge.Joints[0].RestDone == True and self.Bridge.Joints[1].RestDone == True and self.Bridge.Joints[2].RestDone == True:
                        break

                    time.sleep(0.5)
                    
                self.Bridge.Status = READY
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo", case = self.Bridge.Status)
                wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")

            elif self.Bridge.Status == READY:
                " Status where the initialization of the system is done, but the ctrl is NOT enabled "

                time.sleep(0.1)

            elif self.Bridge.Status == RUNNING:

                t0 = time.clock()

                for i in range(0, self.Bridge.JointsNum):

                    if not __debug__:
                        self.Coord.J_current[i] = self.Bridge.Joints[i].Position
                    else:
                        self.Bridge.Joints[i].Position = self.Coord.J_current[i]

                #TODO check self.p0_check - da valutare "
                if self.Bridge.Control.Input == 'Vocal':

                    if self.Bridge.Control.VocalStepsCnt >= self.Bridge.Control.VocalSteps:
                        self.Coord.p0 = [0]*4
                        # self.Bridge.Control.VocalStepsCnt = 0
                    else:
                        self.Bridge.Control.VocalStepsCnt = self.Bridge.Control.VocalStepsCnt+1


                if not self.Bridge.Control.Status == POS_CTRL_ABS:

                    if all(i == 0 for i in self.Coord.p0):
                        self.Bridge.Control.Status = POS_CTRL
                    else:
                        self.Bridge.Control.Status = SPEED_CTRL


                        " 2. Run IK algorithm "
                        self.MartaCtrl()

                        " Update graphics in main window "
                        wx.CallAfter(Publisher.sendMessage, "UpdateJointsInfo")


                elapsed_time = time.clock() - t0
                # print elapsed_time

                if elapsed_time > self.Bridge.Control.ThreadPeriod:
                    elapsed_time = self.Bridge.Control.ThreadPeriod
                    print ' ControlThread: Overrun'
                else:
                    time.sleep(self.Bridge.Control.ThreadPeriod - elapsed_time)

            elif self.Bridge.Status == TARGET_POSITION:

                print "+ Target Position"
                for i in range(0, self.Bridge.JointsNum):
                    self.Bridge.Joints[i].TargetDone = False

                self.Bridge.Control.SetStatus(POS_CTRL_ABS)

                arrigon = [False] * self.Bridge.JointsNum

                while 1 and self.Running:


                    for i in range(0, self.Bridge.JointsNum):
                        arrigon[i] = self.Bridge.Joints[i].TargetDone

                    if all(i == True for i in arrigon):
                        break

                print arrigon

                print "RETRIEVE POSITION DONE"

                self.Bridge.SetStatus(RUNNING)
                self.Bridge.Control.SetStatus(POS_CTRL)


            if self.Bridge.Status != self.Bridge.OldStatus:
                self.Bridge.OldStatus = self.Bridge.Status
                wx.CallAfter(Publisher.sendMessage, "UpdateControlInfo", case = self.Bridge.Status)


        print '- Control Thread Out'

    def MartaCtrl(self):

        self.Coord.J_current_rad           = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.temp_EndEff0       = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.WS_is_gay          = False
        self.dq_prev            = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0]) # inizializzazione del primo step
        " Matrice 'la' Jacobiana "
        self.Jacob              = numpy.zeros((3, self.Bridge.JointsNum))
        " Matrice pesi "
        self.Wq                 = numpy.eye(self.Bridge.JointsNum)

        self.ul                 = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.dl                 = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0])
        #TODO: ?
        self.change_dir_count   = [0]*5
        self.p0_check           = [0]*4


        " STEP 1: FK "

        for i in range (0,self.Bridge.JointsNum):

            self.Coord.J_current_rad[i] = self.Coord.J_current[i]*math.pi/180

        " FK per calcolo di posizione attuale -> Elbow "

        # 3 Giunti
        # self.Coord.Elbow[0] = math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        # self.Coord.Elbow[1] = -math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        # self.Coord.Elbow[2] = math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)

        "4 Joints"
        self.Coord.Elbow[0]   = self.Bridge.Patient.RJoint3*(math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1])) + math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        self.Coord.Elbow[1]   = self.Bridge.Patient.RJoint3*(math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) + math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])) - math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2)
        self.Coord.Elbow[2]   = math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])

        " FK per calcolo di posizione attuale -> EndEff_current "
        # 3 Giunti
        # self.Coord.EndEff_current[0] = math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])
        # self.Coord.EndEff_current[1] = -math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])
        # self.Coord.EndEff_current[2] = math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1])

        "4 Joints"
        self.Coord.EndEff_current[0] = self.Bridge.Patient.RJoint3*(math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0]) + math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) + math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])
        self.Coord.EndEff_current[1] = self.Bridge.Patient.RJoint3*(math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) + math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2]) - math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) - math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[0])
        self.Coord.EndEff_current[2] = math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[3])

        " Calculate EndEff_des (only for step-by-step control) "
        # if not self.Coord.GoToSavedPosMainTrigger:
        self.Coord.EndEff_des[0] = self.Coord.EndEff_current[0] + self.Coord.p0[0]*self.Bridge.Control.S*self.Bridge.Control.Time # x attuale + p0*v_max*tempo loop controllo [m]
        self.Coord.EndEff_des[1] = self.Coord.EndEff_current[1] + self.Coord.p0[1]*self.Bridge.Control.S*self.Bridge.Control.Time # y attuale + p0*v_max*tempo loop controllo [m]
        self.Coord.EndEff_des[2] = self.Coord.EndEff_current[2] + self.Coord.p0[2]*self.Bridge.Control.S*self.Bridge.Control.Time # z attuale + p0*v_max*tempo loop controllo [m]
        # self.Coord.EndEff_des[3] = self.Coord.EndEff_current[3] + self.Coord.p0[3]*self.Bridge.Control.MaxDegDispl        # PS pesata per input [°]

        self.temp_EndEff_current = [0]*4
        for i in range (0,4):
            self.temp_EndEff_current[i] = self.Coord.EndEff_current[i]

        " STEP 2: Check belonging to the possible workspace di EndEff_des "
        # TODO: modificare condizioni WS
        self.WS_is_gay = True # aggiungere funzione check WS


        " STEP 3: IK: EndEff_des -> J_des (valori di giunto che devo raggiungere [deg]) "
        # inizializzazione parametri ciclo IK
        exit         = False # controlla num massimo di iterazioni algoritmo IK
        n            = 0     # counter numero iterazioni algoritmo IK        
        self.Wq      = numpy.eye(self.Bridge.JointsNum)
        self.dq_prev = numpy.array([0.0, 0.0, 0.0, 0.0])

        # TODO: check input movimento nel thread gestione input "

        if self.WS_is_gay and (abs(self.Coord.p0[0]) > 0 or abs(self.Coord.p0[1]) > 0 or abs(self.Coord.p0[2]) > 0 or abs(self.Coord.p0[3]) > 0):
            
            dp = self.Coord.EndEff_des[0:3]-self.temp_EndEff_current[0:3]

            while (abs(dp[0]) > 1e-7 + self.Bridge.Control.Tollerance*abs(self.Coord.p0[1]) or abs(dp[1]) > 1e-7+self.Bridge.Control.Tollerance*abs(self.Coord.p0[0]) or abs(dp[2]) > 1e-7 + self.Bridge.Control.Tollerance*abs(self.Coord.p0[2])) and exit == False:

                # 3 Giunti
                '''
                self.Jacob[0,0] = self.Bridge.Patient.RJoint3*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]) - math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])
                self.Jacob[0,1] = - math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1]) - self.Bridge.Patient.l3*math.cos(self.J_current_rad[0])*math.cos(self.J_current_rad[2])*math.sin(self.J_current_rad[1])
                self.Jacob[0,2] = - self.Bridge.Patient.l3*math.cos(self.J_current_rad[2])*math.sin(self.J_current_rad[0]) - self.Bridge.Patient.l3*math.cos(self.J_current_rad[0])*math.cos(self.J_current_rad[1])*math.sin(self.J_current_rad[2])
                self.Jacob[1,0] = - math.cos(self.J_current_rad[0])*math.cos(self.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.J_current_rad[0])*math.sin(self.J_current_rad[1]) + self.Bridge.Patient.l3*math.sin(self.J_current_rad[0])*math.sin(self.J_current_rad[2]) - self.Bridge.Patient.l3*math.cos(self.J_current_rad[0])*math.cos(self.J_current_rad[1])*math.cos(self.J_current_rad[2])
                self.Jacob[1,1] = math.sin(self.J_current_rad[0])*math.sin(self.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.J_current_rad[1])*math.sin(self.J_current_rad[0]) + self.Bridge.Patient.l3*math.cos(self.J_current_rad[2])*math.sin(self.J_current_rad[0])*math.sin(self.J_current_rad[1])
                self.Jacob[1,2] = - self.Bridge.Patient.l3*math.cos(self.J_current_rad[0])*math.cos(self.J_current_rad[2]) + self.Bridge.Patient.l3*math.cos(self.J_current_rad[1])*math.sin(self.J_current_rad[0])*math.sin(self.J_current_rad[2])
                self.Jacob[2,0] = 0
                self.Jacob[2,1] = math.cos(self.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.sin(self.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.J_current_rad[1])*math.cos(self.J_current_rad[2])
                self.Jacob[2,2] = -self.Bridge.Patient.l3*math.sin(self.J_current_rad[1])*math.sin(self.J_current_rad[2])              
                '''

                # 4 Giunti
                self.Jacob[0,0]= self.Bridge.Patient.RJoint3 *(math.cos(self.Coord.J_current_rad[0]) *math.sin(self.Coord.J_current_rad[2]) + math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2]) - math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) - math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[0])
                self.Jacob[0,1]= - math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) -self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2]) -self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[1]) -self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[3])
                self.Jacob[0,2]= self.Bridge.Patient.RJoint3*(math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0]) + math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) + self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1]))
                self.Jacob[0,3]= - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0]) + math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[3])
                self.Jacob[1,0]= self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0]) + math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) - self.Bridge.Patient.RJoint3*(math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1])) - math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])
                self.Jacob[1,1]= math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[3])
                self.Jacob[1,2]= self.Bridge.Patient.RJoint3*(math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2]) - math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) + self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) + math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]))
                self.Jacob[1,3]= self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[3]) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2]) - math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2]))
                self.Jacob[2,0]= 0
                self.Jacob[2,1]= math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3]) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[3])
                self.Jacob[2,2]= self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[3]) - self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])
                self.Jacob[2,3]= self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[2]) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[3])

                # print 'Jacob ', self.Jacob
                # Jacobiano moltiplicato per i pesi -> iterazione sulla matrice Jacobiana
                JacobW = numpy.dot(self.Jacob, self.Wq)

                # SVD
                U, s, V = numpy.linalg.svd(JacobW, full_matrices=False)
                s_min = numpy.amin(s)

                if s_min < self.Bridge.Control.Eps:

                    " Peso per smorzare le velocità di giunto in singolarita' "
                    self.Wq[0,0] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
                    self.Wq[1,1] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
                    self.Wq[2,2] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
                    self.Wq[3,3] = self.Bridge.Control.Wq0s+(1-self.Bridge.Control.Wq0s)*s_min/self.Bridge.Control.Eps
            
                else:
                    self.Wq[0,0] = 1
                    self.Wq[1,1] = 1
                    self.Wq[2,2] = 1
                    self.Wq[3,3] = 1

                " ################### "
                " 3.2. LIMITI dei ROM "
                " ################### "

                if not __debug__:
                    for i, J in zip(range(0, self.Bridge.JointsNum), self.Bridge.Joints):

                        if self.dq_prev[i] >= 0:
                            self.dl[i] = J.Jmax - J.Position
                        else:
                            self.dl[i] = J.Position - J.Jmin

                        if self.dl[i] < self.Bridge.Control.Dol:
                            self.ul[i] = max(self.ul[i] - self.Bridge.Control.Du, self.dl[i] / self.Bridge.Control.Dol)
                        else:
                            self.ul[i] = min(self.ul[i] + self.Bridge.Control.Du, 1)
                        self.Wq[i, i] = self.Bridge.Control.Wq0s + (1 - self.Bridge.Control.Wq0s) * self.ul[i]
                        self.Bridge.Control.Alpha = self.Bridge.Control.Alpha0 * (1 - self.ul[i] ** 2)
                else:
                    for i, J_current, J in zip(range(0, self.Bridge.JointsNum), self.Coord.J_current, self.Bridge.Joints):

                        if self.dq_prev[i] >= 0:
                            self.dl[i] = J.Jmax - J_current
                        else:
                            self.dl[i] = J_current - J.Jmin

                        if self.dl[i] < self.Bridge.Control.Dol:
                            self.ul[i] = max(self.ul[i] - self.Bridge.Control.Du, self.dl[i] / self.Bridge.Control.Dol)
                        else:
                            self.ul[i] = min(self.ul[i] + self.Bridge.Control.Du, 1)

                        self.Wq[i, i] = self.Bridge.Control.Wq0s + (1 - self.Bridge.Control.Wq0s) * self.ul[i]

                        self.Bridge.Control.Alpha = self.Bridge.Control.Alpha0 * (1 - self.ul[i] ** 2)


                " ###################################################### "
                " 3.3 Aggiornamento e calcolo della variazione di giunto "
                " ###################################################### "

                " Aggiorno il Jacobiano "
                JacobW = numpy.dot(self.Jacob, self.Wq)

                " Equazione per trovare la variazione di giunto da applicare "
                temp = inv(numpy.dot(JacobW, JacobW.transpose()) + self.Bridge.Control.Alpha*numpy.eye(3))

                dq = numpy.dot(numpy.dot(numpy.dot(self.Wq,JacobW.transpose()), temp), dp.transpose())
                self.dq_prev = dq               

                " Update dei valori di giunto che voglio raggiungere "

                self.Coord.J_des[0:self.Bridge.JointsNum] = self.Coord.J_current_rad[0:self.Bridge.JointsNum]*180/math.pi + dq*180/math.pi

                " ################################### "
                " 3.4. Aggiornamento valori di giunto "
                " ################################### "

                # self.Coord.J_current_rad[0:4] = self.Coord.J_des[0:4]*math.pi/180
                self.Coord.J_current_rad[0] = self.Coord.J_des[0]*math.pi/180
                self.Coord.J_current_rad[1] = self.Coord.J_des[1]*math.pi/180
                self.Coord.J_current_rad[2] = self.Coord.J_des[2]*math.pi/180
                self.Coord.J_current_rad[3] = self.Coord.J_des[3]*math.pi/180

                # 3 Giunti
                '''
                p_update    = numpy.array([0.0, 0.0, 0.0]) 
                p_update[0] = math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])
                p_update[1] = -math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1]) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])
                p_update[2] = math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1])
                '''

                # 4 Giunti
                p_update    = numpy.array([0.0, 0.0, 0.0]) 
                p_update[0] = self.Bridge.Patient.RJoint3*(math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) - math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0]) + math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) + math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])
                p_update[1] = self.Bridge.Patient.RJoint3*(math.cos(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[2]) + math.cos(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])) - self.Bridge.Patient.l3*math.sin(self.Coord.J_current_rad[3])*(math.cos(self.Coord.J_current_rad[0])*math.cos(self.Coord.J_current_rad[2]) - math.sin(self.Coord.J_current_rad[0])*math.sin(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])) - math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[0])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) - self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[0])
                p_update[2] = self.Coord.EndEff_current[2] = math.sin(self.Coord.J_current_rad[1])*(self.Bridge.Patient.l1 + self.Bridge.Patient.l2) + self.Bridge.Patient.RJoint3*math.cos(self.Coord.J_current_rad[1])*math.cos(self.Coord.J_current_rad[2]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[3])*math.sin(self.Coord.J_current_rad[1]) + self.Bridge.Patient.l3*math.cos(self.Coord.J_current_rad[1])*math.sin(self.Coord.J_current_rad[2])*math.sin(self.Coord.J_current_rad[3])
                
                " Update errore che devo ridurre con le mie iterazioni (idealmente zero) "
                dp = self.Coord.EndEff_des[0:3] - p_update

                " Update del num di iterazioni ciclo while "
                n = n+1
                if n >= self.Bridge.Control.IterMax:
                    exit = True
                    for i in range(0, self.Bridge.JointsNum):

                        if not __debug__:
                            self.Coord.J_des[i] = self.Bridge.Joints[i].Position
                            #self.Coord.p0 = [0] * 4
                            #self.Bridge.Control.Status = POS_CTRL
                        else:
                            self.Coord.J_des[i] = self.Coord.J_current[i]
                            #self.Coord.p0 = [0] * 4
                            #self.Bridge.Control.Status = POS_CTRL


                    print '  Maximum # of iterations'

            " Verifico che la soluzione trovata rispetti i limiti di giunto altrimenti li limito all'estremo più vicino --> riporto errore "

            for i, J in zip(range(0,self.Bridge.JointsNum), self.Bridge.Joints):

                if J.Position <= (J.Jmin + self.Bridge.Control.Threshold) and self.Coord.J_des[i] <= J.Jmin and (self.Coord.J_des[i] - J.Position) <= 0:
                    winsound.Beep(550, 500)  # frequency, duration[ms
                    print '# J%d close to lower limit (J_des: %f) - (J_current: %f) - (Jmin: %f)' % (i+1, self.Coord.J_des[i], J.Position, J.Jmin)
                    J.Bounded = True
                    self.Coord.J_des[i] = J.Jmin


                elif J.Position <= (J.Jmax - self.Bridge.Control.Threshold) and self.Coord.J_des[i] >= J.Jmax and (self.Coord.J_des[i] - J.Position) >= 0:
                    winsound.Beep(330, 500) # frequency, duration[ms]
                    print '# J%d close to upper limit (J_des: %f) - (J_current: %f) - (Jmax: %f)' % (i+1, self.Coord.J_des[i], J.Position, J.Jmax)
                    J.Bounded = True
                    self.Coord.J_des[i] = J.Jmax
                else:
                    J.Bounded = False

                JCurrentPos = []
                if not __debug__:
                    for J in self.Bridge.Joints:
                        JCurrentPos.append(J.Position)
                else:
                    for i in range(0, self.Bridge.JointsNum):
                        JCurrentPos.append(self.Coord.J_current[i])

                '''
                diff = [x - y for x, y in zip(JCurrentPos, self.Coord.J_des)]
                for i in diff:
                    if abs(i) > self.Bridge.Control.MaxDegDispl:
                        print 'Repentine Change'
                        self.Coord.J_des = JCurrentPos
                        self.Bridge.Control.Status = POS_CTRL
                '''
                " Check no repentine change of joints value! "

            diff = [0]*5
            for i in range(0, self.Bridge.JointsNum):
                diff[i] = self.Coord.J_des[i] - JCurrentPos[i]

                if abs(diff[i]) > self.Bridge.Control.MaxDegDispl:
                    print '# Repentine Change'
                    self.Coord.J_des = JCurrentPos
                    self.Bridge.Control.Status = POS_CTRL

                self.Coord.Jv[i] = ((self.Coord.J_des[i] - JCurrentPos[i]) / self.Bridge.Control.Time)

                # TODO: valutare cosa fare - "
                #self.Conf.CtrlEnable =  False

 
            '''
            " Mappo lo spostamento di posizione in spostamento di velocità richiesto ai giunti "
            " calcolo delta in gradi che voglio muovere sui vari motori"
            for i in range(0,self.Bridge.JointsNum):
                if self.Bridge.Control.BoundedJv[i]:
                    # reset del flag
                    self.Bridge.Control.BoundedJv[i] = False
                else:
            '''

            # print 'Jv ', self.Coord.Jv
            # for i in range(0,self.Bridge.JointsNum):
            #   print
            #   print str(i) + ' ' + str(self.Coord.Jv[i])

            for i in range(0,self.Bridge.JointsNum):
                if __debug__:
                    self.Coord.J_current[i] = self.Coord.J_des[i]
                else:
                    self.Coord.J_current[i] = self.Bridge.Joints[i].Position

            # # monitor variables
            # #file_J_current.append(self.Coord.J_current[0])
            # file_J_current.append(self.Coord.J_current[1])
            # #file_J_current.append(self.Coord.J_current[2])
            # #file_J_current.append(self.Coord.J_current[3])
            # file_p0_.append(self.Coord.p0[0])
            # file_p0_.append(self.Coord.p0[1])
            # file_p0_.append(self.Coord.p0[2])
            # file_p0_.append(self.Coord.p0[3])
            # #file_EndEff0.append(self.Coord.EndEff_current[0])
            # #file_EndEff0.append(self.Coord.EndEff_current[1])
            # file_EndEff0.append(self.Coord.EndEff_current[2])
            # #file_EndEff_des.append(self.Coord.EndEff_des[0])
            # #file_EndEff_des.append(self.Coord.EndEff_des[1])
            # file_EndEff_des.append(self.Coord.EndEff_des[2])
            # # file_J_current.append(self.Bridge.Joints[0].Position)
            # # file_J_current.append(self.Bridge.Joints[1].Position)
            # # file_J_current.append(self.Bridge.Joints[2].Position)
            # # file_J_current.append(self.Bridge.Joints[3].Position)

            # #file_J_des.append(self.Coord.J_des[0])
            # file_J_des.append(self.Coord.J_des[1])
            # #file_J_des.append(self.Coord.J_des[2])
            # #file_J_des.append(self.Coord.J_des[3])
            # file_elbow.append(self.Coord.Elbow[2])

        else:
            self.Coord.Jv = [0]*5
            self.Bridge.Control.Status = POS_CTRL

    def terminate(self):
        " Exit the thread "
        self.Running = False
        self.Bridge.Status = NONE

        # text_file_EndEff0 = open("Output_EndEff0.txt", "w")
        # text_file_EndEff_des = open("Output_EndEff_des.txt", "w")
        # text_file_J_current = open("Output_J_current.txt", "w")
        # text_file_J_des = open("Output_J_des.txt", "w")
        # text_file_p0_ = open("Output_p0.txt", "w")

        # # scrivo variabili sui file prima di chiudere
        # text_file_EndEff0.write("\n{0}".format(file_EndEff0))
        # text_file_EndEff_des.write("\n{0}".format(file_EndEff_des))
        # text_file_J_current.write("\n{0}".format(file_J_current))
        # text_file_J_des.write("\n{0}".format(file_J_des))
        # text_file_p0_.write("\n{0}".format(file_p0_))

