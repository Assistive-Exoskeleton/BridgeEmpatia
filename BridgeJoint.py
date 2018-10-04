# -*- coding: utf-8 -*-
import math
from numpy.linalg import inv
import math
import numpy
import serial
import threading, time



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

class Joint:

    def __init__(self, Num, COM, Bridge, Exo, Coord):

        self.Bridge         = Bridge
        self.Num            = Num
        self.CommPort       = ""
        self.Ratio          = Exo.Jratio[Num-1]         # reduction ratio
        self.Offset         = Exo.Joffset[Num-1]        # home (0 step) position (deg)
        self.Jdef           = self.Bridge.Patient.Jdef[Num-1]       # lo uso come target iniziale
        self.StepDegrees    = 1.8
        self.Jtarget        = self.Bridge.Patient.Jrest[Num-1]      # lo uso come posizione di rest post donning
        self.Jrest          = self.Bridge.Patient.Jrest[Num-1]
        self.JtargetStep    = self.deg2step(self.Jtarget)
        self.JminExo        = Exo.Jmin[Num-1]           # min joint angular position
        self.JmaxExo        = Exo.Jmax[Num-1]           # max joint angular position
        self.Imin           = Exo.Imin[Num-1]
        self.Imax           = Exo.Imax[Num-1]
        self.Jmin           = 0                         # patient min
        self.Jmax           = 0                         # patient max
        self.InitError      = False

        if not self.SetRange(self.Bridge.Patient.Jmin[Num-1], self.Bridge.Patient.Jmax[Num-1]):
            self.InitError = True

        " Degrees value of one step "


        " Current position "
        self.Position       = None
        self.PositionDeg    = None
        self.PositionStep   = None

        self.Connected      = False

        self.Bounded        = False
        self.Coord          = Coord
        self.Timeout        = False

        self.Port           = serial.Serial()

        self.ForceExit      = False

        self.Homed          = False
        self.RestDone       = False
        self.TargetDone     = False


        self.SetPort(COM)
        
    def SetJtarget(self, Jtarget):
        self.JtargetStep = Jtarget

    " Set serial port "
    def SetPort(self, name):
        self.CommPort = name

    " Set joint range "
    def SetRange(self, jmin, jmax):
        if jmin > jmax:
            self.Jmin           = self.JminExo
            self.Jmax           = self.JmaxExo
            return False
            
        if jmin < self.JminExo:
            self.Jmin = self.JminExo
        else:
            self.Jmin = jmin
        
        if jmax > self.JmaxExo:
            self.Jmax = self.JmaxExo
        else:
            self.Jmax = jmax
    
    " Check the controller response "
    def ReplyCheck(self, sentcmd):

        stream  = str()
        looppa  = 1
        

#        while not stream.endswith("\r",stream):
        while looppa == 1:

            cnt     = 0

            " Wait for data in the RXbuffer "
            while self.Port.inWaiting() < 1:
                cnt += 1

                if cnt > 100:
                    self.Timeout = True
                    return False

                time.sleep(0.01)
                
            try:
                newchar = self.Port.read(1)
            except:
                return False

            if newchar == '\r':
                cmd_reply = stream + newchar
                looppa = 0
            else:
                stream += newchar
        
        # print 'reply:' + cmd_reply
        
        " escludo il cancelletto dal confronto "
        if cmd_reply == sentcmd[1 : ]:
            return True

        else:
            print " ReplyCheck() - Wrong Reply"
            return False
        
    " Set up one or more parameters "
    def WriteCmd(self, command):

        for cmd_el in command:

            try:
                self.Port.write(cmd_el)
            except Exception, e:
                print 'WriteCmd() failed | ' + str(e)
                return False

            ret = self.ReplyCheck(cmd_el)

            if ret == False:
                return False
                
        return True

    def WriteCmdOrig(self, command):

        ok_flag = True
        
        for cmd_el in command:
            
            try:
                self.Port.write(cmd_el)
                #print 'sent command: ' + cmd_el
                
                if self.ReplyCheck(cmd_el) == 1:
                    ok_flag = True
                    #print 'Config sent correctly'
                else:
                    ok_flag = False
                    print 'Wrong Reply to Config 2'
            except Exception, e:
                print 'WriteCmd() failed. ' + str(e)
                return False
                
        return ok_flag

    def ReadCmd(self, command):
        
        try:
            self.Port.write(command)
            #print 'parameter to read: ' + command
            
            stream = str()
            looppa = 1

#           while not stream.endswith("\r",stream):
            while looppa == 1:

                #wait for data in the RXbuffer
                while self.Port.inWaiting() < 1:
                    time.sleep(0.01)
                
                newchar = self.Port.read(1)

                if newchar == '\r':
                    cmd_reply = stream + newchar
                    looppa = 0               
                    #print cmd_reply      
                else:
                    stream += newchar

                if self.ForceExit:
                    return
            #print 'reply:' + cmd_reply
            #cmd_reply = cmd_reply[1 : ] #ELIMINO CANCELLETTO DA RIMUOVERE!!!
            #print 'mod reply: ' + cmd_reply
            #print 'comm_t', command[1:len(command)-1]            
            #print 'reply_t', cmd_reply[ : len(command)-2]
            
            #command = command[1 : ]
#            if cmd_reply[ : 2] == command[1:3] :  #escludo il cancelletto dal confronto
            if cmd_reply[ : len(command)-2] == command[1:len(command)-1] :  #escludo il cancelletto dal confronto
                #if true, the controller response is relative to my query
                #so the value is after the header (and before the terminator)
                #value = int(cmd_reply[2: -1])
                #print 'valstring', cmd_reply[len(command)-2: -1]
                value = int(cmd_reply[len(command)-2: -1])
                #print 'val', value
                #print "Config sent correctly"
                return value
            else:
                print 'Wrong Reply to Read'
                return 0
        except Exception, e:
            print 'ReadCmd() failed | ' + str(e)
            return -1

    def OpenPort(self):
        try:
            self.Port.port     = self.CommPort
            self.Port.baudrate = 115200
            self.Port.parity   = serial.PARITY_NONE
            self.Port.stopbits = serial.STOPBITS_ONE
            self.Port.bytesize = serial.EIGHTBITS
            self.Port.timeout  = 0.1
            self.Port.open()
            self.Port.isOpen()
            self.Port.flush()
            self.Port.flushInput()
            self.Port.flushOutput()
            self.Connected = True
            return True

        except Exception, e:
            self.Connected = False
            print "#Error |", str(e)
            return False

    def ClosePort(self):

        " Close serial port "

        try:
            if self.Port.isOpen():
                self.Port.close()
                self.Connected = False
            return True

        except Exception, e:
            print "#Error Close Port |", e
            return False

    def FlushPort(self):

        "Flush COM port"
        try:
            if self.Port.isOpen():
                self.Port.flush()
                #self.Port.flushInput()
                #self.Port.flushOutput()
            return True

        except Exception, e:
            print "#Error Flush Port |", e
            return False

    '#######################'
    '# MOT0R CONTROL MODES #'
    '#######################'

    "Set the Absolute Position Mode: Profile #1"
    def SetAbsolutePositionMode(self):
        targetspeed = '#1o%d\r' % int(3*self.Ratio)
        print targetspeed
        command = ["#1y1\r","#1p2\r",targetspeed]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.1)
            return True
        except Exception, e:
            print "# Set Absolute Position Mode failed | " + str(e)
            return False

    def SetStandStillCurrent(self,current):
        targetcurrent = "#1r%d\r" % current
        command = [targetcurrent]
        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.1)
            return True
        except Exception, e:
            print "# Set Standstill Current failed | " + str(e)
            return False

    "Set the Relative Position Mode: Profile #3"
    def SetRelativePositionMode(self):
        command = ["#1y3\r","#1s0\r","#1A\r"]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.1)
            return True
        except Exception, e:
            print "# Set Relative Position Mode failed | " + str(e)
            return False

    "Set the Speed Mode: Profile #10"
    def SetSpeedMode(self):
        command = ["#1y10\r"]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.1)
            return True
        except Exception, e:
            print "# Set Absolute Position Mode failed | " + str(e)
            return False

    "Set the Homing Mode: Profile #2"
    def SetHomingMode(self):
        command = ["#1y2\r", "#1A\r"]


        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.01)
            return True
        except Exception, e:
            print "# Set Homing Mode failed | " + str(e)
            return False

    "Start the Motor"
    def MotorStart(self):
        command = ["#1A\r"]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.01)
            return True
        except Exception, e:
            print '# Motor Start failed | ' + str(e)
            return False

    def MotorStop(self):
        command = ["#1S\r","#1S\r"]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.01)
            return True
        except Exception, e:
            print '# Motor Stop failed | ' + str(e)
            return False

    "Test the Motor"
    def MotorTest(self):

        self.SetRelativePositionMode()

        command = ["#1s100\r","#1A\r"]

        try:
            while self.WriteCmd(command) == False:
                if self.Timeout:
                    return False

                time.sleep(0.01)

        except Exception, e:
            print '# Error Motor Test + | ' + str(e)
            return False

        time.sleep(1)

        command = ["#1s-100\r","#1A\r"]
        try:
            while self.WriteCmd(command) == False:
                if self.Timeout:
                    return False

                time.sleep(0.01)

        except Exception, e:
            print '# Error Motor Test - | ' + str(e)
            return False

        time.sleep(0.5)

        return True



    def SetPositionDeg(self, p0deg):

        " Send the target position to the controller (deg) "
        try:
            " Check if the desired value is in the correct range "
            if p0deg >= self.Jmin and p0deg <= self.Jmax:
                " Calculate deg to step "
                p0step = self.deg2step(p0deg - self.Offset)
            else:
                return False

            print 'J%d p0step: '   % self.Num, p0step
            print 'J%d p0step actual: ' % self.Num, self.PositionStep


            if  abs(p0step - self.PositionStep) < 1:

                print 'J%d Stop' % self.Num
                return False

            else:

                print 'J%d Move' % self.Num
                targetpos = "#1s%d\r" % p0step
                command = [targetpos, "#1A\r"]  #Target Position, Start Movement
                self.WriteCmd(command)
                return True

        except Exception, e:
            return False
            print "#Error Set Position Deg | " + str(e)

    def SetPositionStep(self, p0step):

        " Send the target position to the controller (step) "
        try:
            " Check if the desired value is in the correct range "
            if self.step2deg(p0step) <= self.Jmin and self.step2deg(p0step) >= self.Jmax and abs(p0step - self.PositionStep) <= 1:

                print 'J%d Stop' % self.Num
                return False

            else:

                print 'J%d Move' % self.Num
                targetpos = "#1s%d\r" % p0step
                command = [targetpos, "#1A\r"]  #Target Position, Start Movement
                self.WriteCmd(command)
                return True

        except Exception, e:
            return False
            print "#Error Set Position Step | " + str(e)

    def SetSpeedHz(self, speed):

        if speed >= 0:
            " Counterclockwise "
            targetdirection = "#1d1\r"
        else:
            " Clockwise "
            targetdirection = "#1d0\r"

        speed = abs(speed)
        if speed > 25000:
            speed = 25000

        "Check range of speed"
        if speed >= 1 and speed <= 25000:
            targetspeed = "#1o%d\r" % speed
            command = [targetdirection, targetspeed, "#1A\r"]  #target position, start movement
            # print 'Speed J%d: ' % self.Num + targetspeed
            ret = self.WriteCmd(command)
            time.sleep(0.01)
            return ret
        else:
            command = ["#1S\r"]
            self.WriteCmd(command)
            time.sleep(0.01)
            return False, -1

    def HomingQuery(self):

        self.DriveErrorClear()
        time.sleep(0.1)

        " First Reference Query"

        if self.ReadCmd("#1:is_referenced\r") == 0:

            self.SetHomingMode()

            while self.ReadCmd("#1:is_referenced\r") == 0:

                if not self.Port.isOpen():
                    return False

                time.sleep(0.1)

            self.DriveErrorReset()
            time.sleep(0.1)
        else:
            print "Homing not necessary!"

        return True

    def DriveErrorClear(self):
        command = ["#1D\r"]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.01)
            return True
        except Exception, e:
            print "# Drive Error Clear failed | " + str(e)
            return False

    def DriveErrorReset(self):
        command = ["#1D0\r"]

        try:
            while self.WriteCmd(command) == False:
                time.sleep(0.01)
            return True
        except Exception, e:
            print "# Drive Error Clear failed | " + str(e)
            return False
    
    "Read the actual position from the controller (deg)"
    def GetPositionDeg(self):
        return self.step2deg(self.ReadCmd("#1I\r")) + self.Offset

    "Read the actual position from the controller (step)"
    def GetPositionStep(self):
        return self.ReadCmd("#1I\r")

    "Return the conversion deg -> step"
    def deg2step(self,pdeg):
        return int(pdeg * self.Ratio / self.StepDegrees)
        
    "Return the conversion step -> deg"
    def step2deg(self, pstep):
        return (pstep / (self.Ratio / self.StepDegrees))


" ####################"
"  JOINT INIT THREAD  "
" ####################"
class Thread_JointInitClass(threading.Thread):

    def __init__(self, Name, Jj):
        threading.Thread.__init__(self, name=Name)
        self.Name           = Name
        self.Running        = False
        self.Jn             = Jj
        
    def run(self):

        self.Running = True

        print '* J%d Homing ...' % self.Jn.Num

        if self.Jn.HomingQuery() == False:

            print '# Error: J%d HomingQuery failed' % self.Jn.Num
            return False

        " Get encoder position "
        self.Jn.PositionStep = self.Jn.GetPositionStep()
        self.Jn.Position = self.Jn.GetPositionDeg()

        print '+ J%d Homing position (deg: %d | step: %d)' % (self.Jn.Num, self.Jn.Position, self.Jn.PositionStep)
        
        time.sleep(0.5)

        " Set the Absolute Mode"
        self.Jn.SetAbsolutePositionMode()

        " Set the donning position "
        self.Jn.SetPositionDeg(self.Jn.Jdef)

        while abs(self.Jn.Position - self.Jn.Jdef) > 0.5:
            if self.Running == False:
                break
            self.Jn.Position = self.Jn.GetPositionDeg()
            self.Jn.PositionStep = self.Jn.GetPositionStep()
            time.sleep(0.1)

        self.Jn.Position = self.Jn.GetPositionDeg()

        print 'J%d - In position (%f)' % (self.Jn.Num, self.Jn.Position)

        " Set home flag "
        self.Jn.Homed = True

        print '+ J%d Default position (deg: %d | step: %d):' % (self.Jn.Num, self.Jn.Position, self.Jn.PositionStep)
        print 'J%d - target position (%f)' % (self.Jn.Num, self.Jn.Jdef)

        self.Jn.SetStandStillCurrent(self.Jn.Imin)
        self.Jn.MotorStop()

    def terminate(self):
        " Exit the thread "
        self.Running = False

" ############################## "
"  JOINT TARGET POSITION THREAD  "
" ############################## "
class Thread_JointTargetPositionClass(threading.Thread):

    def __init__(self, Name, Jj):
        threading.Thread.__init__(self)
        self.Name           = Name
        self.Running        = False
        self.Jn             = Jj
        
    def run(self):

        self.Running = True
        self.Jn.RestDone = False

        " Read Position"
        self.Jn.Position = self.Jn.GetPositionDeg()
        self.Jn.PositionStep = self.Jn.GetPositionStep()
        " Motor Error Reset "
        self.Jn.DriveErrorClear()

        " Set Absolute Mode "
        self.Jn.SetAbsolutePositionMode()
        self.Jn.SetStandStillCurrent(self.Jn.Imax)

        " Set the Target position "
        self.Jn.SetPositionDeg(self.Jn.Jrest)

        while abs(self.Jn.GetPositionDeg() - self.Jn.Jrest) > 0.5:
            if self.Running == False:
                break
            self.Jn.Position = self.Jn.GetPositionDeg()
            time.sleep(0.1)

        self.Jn.Position = self.Jn.GetPositionDeg()

        print '+ J%d Rest position (%f -> %f)' % (self.Jn.Num, self.Jn.Jrest, self.Jn.Position)

        self.Jn.RestDone = True
        
    def terminate(self):
        " Exit the thread "
        self.Running = False
    
" ##################### "
"  JOINT UPDATE THREAD  "
" ##################### "
class Thread_JointUpdateClass(threading.Thread):
    def __init__(self, Name, Jj, Coord, Bridge):
        threading.Thread.__init__(self, name=Name)
        self.Name           = Name
        self.Running        = False
        self.Jn             = Jj
        #TODO: valutare tempi meno stringenti (originale 0.1) "
        self.Period         = 0.2
        self.StopPosition   = None
        self.OldStatus      = IDLE
        self.Bridge         = Bridge
        self.Coord          = Coord
        self.Jn.ForceExit   = False

        
    def run(self):

        self.Running   = True

        " Position Control, Relative Position, Start"
        #self.Jn.SetRelativePositionMode()

        " Get current position "


        while self.Running:

            try:
                " Measure process time "
                t0 = time.clock()

                " Detecting New Control Mode"
                if self.Bridge.Control.Status != self.OldStatus:
                    self.OldStatus = self.Bridge.Control.Status

                    self.Jn.MotorStop()
                    self.Jn.DriveErrorClear()

                    if self.Bridge.Control.Status == SPEED_CTRL:
                        self.Jn.SetSpeedMode()

                    if self.Bridge.Control.Status == POS_CTRL:

                        self.Jn.SetRelativePositionMode()
                        self.Jn.SetStandStillCurrent(self.Jn.Imax)

                        # "Position Control - Relative Position"
                        # command = ["#1y3\r", "#1s0\r", "#1A\r"]
                        # while self.Jn.WriteCmd(command) == False:
                        #     time.sleep(0.01)

                        # "Position Control - Absolute Position"
                        # command = ["#1y1\r", "#1p2\r", "#1A\r"]

                    elif self.Bridge.Control.Status == POS_CTRL_ABS:

                        "Position Control - Absolute Position"

                        self.Jn.SetAbsolutePositionMode()
                        self.Jn.SetPositionStep(self.Jn.JtargetStep)

                    else:

                        "Position Control - Relative Position"

                self.Jn.PositionStep = self.Jn.GetPositionStep()
                self.Jn.Position = self.Jn.GetPositionDeg()

                " If the control is enabled "

                if self.Bridge.Control.Status == SPEED_CTRL:
                    
                    " Set speed "
                    self.Jn.SetSpeedHz(self.Jn.deg2step(self.Coord.Jv[self.Jn.Num - 1]))

                elif self.Bridge.Control.Status == POS_CTRL:

                    #self.Jn.Position = self.Jn.GetPositionDeg()

                    #TODO: cosa succede se il sistema e' forzato? "
                    #self.Jn.SetPositionDeg(self.Jn.GetPositionDeg())

                    '#############################'
                    '# ABSOLUTE POSITION CONTROL #'
                    '#############################'

                elif self.Bridge.Control.Status == POS_CTRL_ABS:

                    if abs(self.Jn.PositionStep - self.Jn.JtargetStep) > 1:
                        print 'J%d - In position (%f)' % (self.Jn.Num, self.Jn.PositionStep)
                        print 'J%d - target position (%f)' % (self.Jn.Num, self.Jn.JtargetStep)
                    else:
                       self.Jn.TargetDone = True


                elapsed_time = time.clock() - t0

                if elapsed_time > self.Period:
                    print '@ Warning: JointUpdate %d Overrun: %d' % (self.Jn.Num, elapsed_time)
                else:
                    time.sleep(self.Period - elapsed_time)

            except Exception, e:
                print '# Error: JointUpdate %d failure | %s' % (self.Jn.Num, str(e))
                self.terminate()
                break

        print "* Stopping Motors ..."
        " Stopping Record "
        self.Jn.MotorStop()
        self.Jn.SetStandStillCurrent(self.Jn.Imin)

        " Flush COM Port"
        self.Jn.FlushPort()

    def terminate(self):

        " Exit the thread "
        self.Running = False
        #self.Jn.ForceExit = True



        
