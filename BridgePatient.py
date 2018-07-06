import ConfigParser


class PatientClass:
   def __init__(self):

       self.Name           = 'Name'
       self.Jmin           = [0]*5
       self.Jmax           = [0]*5
       self.Jrest          = [0]*5
       self.Jdef           = [0]*5
       self.l1             = 1 #None      # [m]
       self.l2             = 1 #None      # [m]
       self.l3             = 1 #None      # [m]
       self.RJoint3        = 0.07     # [m]
       self.Loaded         = False
       self.Filename       = 'Defaults.ini'
       self.Input          = ''
       self.JoystickCalibration = [1.0]*4

   def ReadPatientFile(self, filename):

        print '* Reading Patient Configuration File ...'

        try:
            Config = ConfigParser.ConfigParser()
            Config.read(filename)

            section = Config.sections()

            self.Name               = Config.get(section[0],"Name")
            self.Jmin[0]            = int(Config.get(section[1],"J1_min"))
            self.Jmin[1]            = int(Config.get(section[1],"J2_min"))
            self.Jmin[2]            = int(Config.get(section[1],"J3_min"))
            self.Jmin[3]            = int(Config.get(section[1],"J4_min"))
            self.Jmin[4]            = int(Config.get(section[1],"J5_min"))

            self.Jmax[0]            = int(Config.get(section[1],"J1_max"))
            self.Jmax[1]            = int(Config.get(section[1],"J2_max"))
            self.Jmax[2]            = int(Config.get(section[1],"J3_max"))
            self.Jmax[3]            = int(Config.get(section[1],"J4_max"))
            self.Jmax[4]            = int(Config.get(section[1],"J5_max"))

            self.Jdef[0]            = int(Config.get(section[1],"J1_default"))
            self.Jdef[1]            = int(Config.get(section[1],"J2_default"))
            self.Jdef[2]            = int(Config.get(section[1],"J3_default"))
            self.Jdef[3]            = int(Config.get(section[1],"J4_default"))
            self.Jdef[4]            = int(Config.get(section[1],"J5_default"))

            self.Jrest[0]           = int(Config.get(section[1],"J1_rest"))
            self.Jrest[1]           = int(Config.get(section[1],"J2_rest"))
            self.Jrest[2]           = int(Config.get(section[1],"J3_rest"))
            self.Jrest[3]           = int(Config.get(section[1],"J4_rest"))
            self.Jrest[4]           = int(Config.get(section[1],"J5_rest"))

            self.l1                 = float(Config.get(section[2],"l1"))
            self.l2                 = float(Config.get(section[2],"l2"))
            self.l3                 = float(Config.get(section[2],"l3"))

            self.JoystickCalibration[0] = float(Config.get(section[3],"axis_forward"))
            self.JoystickCalibration[1] = float(Config.get(section[3], "axis_backward"))
            self.JoystickCalibration[2] = float(Config.get(section[3], "axis_left"))
            self.JoystickCalibration[3] = float(Config.get(section[3], "axis_right"))

            return True

        except Exception, e:
            print '# Error: ReadPatientFile failed | ' + str(e)
            return False

   def ParsePatientFile (self, filename):

        try:

            Patient     = PatientClass()
            Config      = ConfigParser.ConfigParser()
            Config.read(filename)
            section     = Config.sections()

            Patient.Name               = Config.get(section[0],"Name")
            #Patient.Input              = Config.get(section[0],"Input")
            Patient.Jmin[0]            = int(Config.get(section[1],"J1_min"))
            Patient.Jmin[1]            = int(Config.get(section[1],"J2_min"))
            Patient.Jmin[2]            = int(Config.get(section[1],"J3_min"))
            Patient.Jmin[3]            = int(Config.get(section[1],"J4_min"))
            Patient.Jmin[4]            = int(Config.get(section[1],"J5_min"))

            Patient.Jmax[0]            = int(Config.get(section[1],"J1_max"))
            Patient.Jmax[1]            = int(Config.get(section[1],"J2_max"))
            Patient.Jmax[2]            = int(Config.get(section[1],"J3_max"))
            Patient.Jmax[3]            = int(Config.get(section[1],"J4_max"))
            Patient.Jmax[4]            = int(Config.get(section[1],"J5_max"))

            Patient.Jdef[0]            = int(Config.get(section[1],"J1_default"))
            Patient.Jdef[1]            = int(Config.get(section[1],"J2_default"))
            Patient.Jdef[2]            = int(Config.get(section[1],"J3_default"))
            Patient.Jdef[3]            = int(Config.get(section[1],"J4_default"))
            Patient.Jdef[4]            = int(Config.get(section[1],"J5_default"))

            Patient.Jrest[0]           = int(Config.get(section[1],"J1_rest"))
            Patient.Jrest[1]           = int(Config.get(section[1],"J2_rest"))
            Patient.Jrest[2]           = int(Config.get(section[1],"J3_rest"))
            Patient.Jrest[3]           = int(Config.get(section[1],"J4_rest"))
            Patient.Jrest[4]           = int(Config.get(section[1],"J5_rest"))

            Patient.l1                 = float(Config.get(section[2],"l1"))
            Patient.l2                 = float(Config.get(section[2],"l2"))
            Patient.l3                 = float(Config.get(section[2],"l3"))

            Patient.JoystickCalibration[0] = float(Config.get(section[3], "axis_forward"))
            Patient.JoystickCalibration[1] = float(Config.get(section[3], "axis_backward"))
            Patient.JoystickCalibration[2] = float(Config.get(section[3], "axis_left"))
            Patient.JoystickCalibration[3] = float(Config.get(section[3], "axis_right"))

            return Patient

        except Exception, e:
            print '# Error: ReadPatientFile failed | ' + str(e)
            # Read conf failed -> create a new configuration file
            return False

   def SavePatient(self, filename, Patient):

       print '* Saving Patient Configuration File ...'

       try:
           Config = ConfigParser.ConfigParser()
           Config.optionxform = str
           section = 'BRIDGE-PATIENT'
           Config.add_section(section)

           Config.set(section, 'Name', Patient.Name)

           section = 'JOINT-ROMs'
           Config.add_section(section)

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

           section = 'LENGTHS'
           Config.add_section(section)

           Config.set(section, 'l1', Patient.l1)
           Config.set(section, 'l2', Patient.l2)
           Config.set(section, 'l3', Patient.l3)

           section = 'JOYSTICK'
           Config.add_section(section)

           Config.set(section, 'axis_forward', Patient.JoystickCalibration[0])
           Config.set(section, 'axis_backward', Patient.JoystickCalibration[1])
           Config.set(section, 'axis_left', Patient.JoystickCalibration[2])
           Config.set(section, 'axis_right', Patient.JoystickCalibration[3])

           cfgfile = open(filename, 'w')
           Config.write(cfgfile)
           cfgfile.close()

           return True
       except Exception, e:
           print '# Error: Saving Patient failed | ' + str(e)
           return False