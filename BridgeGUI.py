# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class BridgeWindow
###########################################################################

class BridgeWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge", pos = wx.DefaultPosition, size = wx.Size( 1100,720 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 1080,-1 ), wx.Size( -1,-1 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Connect"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItem1.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_MENU ) )
		self.m_menu1.AppendItem( self.m_menuItem1 )
		
		self.m_menuItem4 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Clear"+ u"\t" + u"Ctrl+C", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem4 )
		
		self.m_menu1.AppendSeparator()
		
		self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Close"+ u"\t" + u"Ctrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItem2.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ) )
		self.m_menu1.AppendItem( self.m_menuItem2 )
		
		self.m_menubar1.Append( self.m_menu1, u"File" ) 
		
		self.Tools = wx.Menu()
		self.m_preferences = wx.MenuItem( self.Tools, wx.ID_ANY, u"Preferences"+ u"\t" + u"Ctrl+P", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_preferences.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_TOOLBAR ) )
		self.Tools.AppendItem( self.m_preferences )
		
		self.m_patient = wx.MenuItem( self.Tools, wx.ID_ANY, u"Patient"+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_patient.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_REPORT_VIEW, wx.ART_TOOLBAR ) )
		self.Tools.AppendItem( self.m_patient )
		
		self.m_menubar1.Append( self.Tools, u"Tools" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer93 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2311112 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText62 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Input", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText62.Wrap( -1 )
		self.m_staticText62.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText62.SetBackgroundColour( wx.Colour( 243, 132, 112 ) )
		self.m_staticText62.SetMinSize( wx.Size( 135,-1 ) )
		
		bSizer2311112.Add( self.m_staticText62, 0, wx.ALL, 5 )
		
		self.inputDescription_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.inputDescription_lbl.Wrap( -1 )
		self.inputDescription_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer2311112.Add( self.inputDescription_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2411111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText911111 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText911111.Wrap( -1 )
		self.m_staticText911111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText911111.SetToolTipString( u"Min" )
		self.m_staticText911111.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer2411111.Add( self.m_staticText911111, 1, wx.ALL, 5 )
		
		self.P0_X_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"- -", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.P0_X_lbl.Wrap( -1 )
		self.P0_X_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer2411111.Add( self.P0_X_lbl, 1, wx.ALL, 5 )
		
		
		bSizer2311112.Add( bSizer2411111, 0, wx.EXPAND, 5 )
		
		bSizer24111111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9111111 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText9111111.Wrap( -1 )
		self.m_staticText9111111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText9111111.SetToolTipString( u"Min" )
		self.m_staticText9111111.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24111111.Add( self.m_staticText9111111, 1, wx.ALL, 5 )
		
		self.P0_Y_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"- -", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.P0_Y_lbl.Wrap( -1 )
		self.P0_Y_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer24111111.Add( self.P0_Y_lbl, 1, wx.ALL, 5 )
		
		
		bSizer2311112.Add( bSizer24111111, 1, wx.EXPAND, 5 )
		
		bSizer24111112 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9111112 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Z", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText9111112.Wrap( -1 )
		self.m_staticText9111112.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText9111112.SetToolTipString( u"Min" )
		self.m_staticText9111112.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24111112.Add( self.m_staticText9111112, 1, wx.ALL, 5 )
		
		self.P0_Z_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"- -", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.P0_Z_lbl.Wrap( -1 )
		self.P0_Z_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer24111112.Add( self.P0_Z_lbl, 1, wx.ALL, 5 )
		
		
		bSizer2311112.Add( bSizer24111112, 1, wx.EXPAND, 5 )
		
		bSizer24111113 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9111113 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"PS", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText9111113.Wrap( -1 )
		self.m_staticText9111113.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText9111113.SetToolTipString( u"Min" )
		self.m_staticText9111113.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24111113.Add( self.m_staticText9111113, 1, wx.ALL, 5 )
		
		self.P0_PS_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"- -", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.P0_PS_lbl.Wrap( -1 )
		self.P0_PS_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer24111113.Add( self.P0_PS_lbl, 1, wx.ALL, 5 )
		
		
		bSizer2311112.Add( bSizer24111113, 1, wx.EXPAND, 5 )
		
		self.m_staticline15 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2311112.Add( self.m_staticline15, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2531111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.JoystickModeA_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"X - Y", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.JoystickModeA_lbl.Wrap( -1 )
		self.JoystickModeA_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.JoystickModeA_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer2531111.Add( self.JoystickModeA_lbl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.JoystickModeB_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Z - PS", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.JoystickModeB_lbl.Wrap( -1 )
		self.JoystickModeB_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer2531111.Add( self.JoystickModeB_lbl, 1, wx.ALL, 5 )
		
		
		bSizer2311112.Add( bSizer2531111, 0, wx.EXPAND, 5 )
		
		bSizer25111111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.JoystickSavePos_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Save Pos.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.JoystickSavePos_lbl.Wrap( -1 )
		self.JoystickSavePos_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer25111111.Add( self.JoystickSavePos_lbl, 1, wx.ALL, 5 )
		
		self.JoystickRecallPos_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Recall", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.JoystickRecallPos_lbl.Wrap( -1 )
		self.JoystickRecallPos_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer25111111.Add( self.JoystickRecallPos_lbl, 1, wx.ALL, 5 )
		
		
		bSizer2311112.Add( bSizer25111111, 0, wx.EXPAND, 5 )
		
		bSizer25211111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer2311112.Add( bSizer25211111, 0, wx.EXPAND, 5 )
		
		bSizer252111111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer2311112.Add( bSizer252111111, 1, wx.EXPAND, 5 )
		
		bSizer2521111111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.JoystickAlarm_lbl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Alarm", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.JoystickAlarm_lbl.Wrap( -1 )
		self.JoystickAlarm_lbl.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.JoystickAlarm_lbl.SetBackgroundColour( wx.Colour( 255, 232, 232 ) )
		
		bSizer2521111111.Add( self.JoystickAlarm_lbl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer2311112.Add( bSizer2521111111, 1, wx.EXPAND, 5 )
		
		
		bSizer6.Add( bSizer2311112, 0, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		self.m_staticline22 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer4.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer96 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer96.SetMinSize( wx.Size( 312,-1 ) ) 
		self.m_tab_settings = wx.Notebook( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_control_settings = wx.Panel( self.m_tab_settings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer23111121 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText6111121 = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"Control Settings", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText6111121.Wrap( -1 )
		self.m_staticText6111121.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText6111121.SetBackgroundColour( wx.Colour( 132, 193, 255 ) )
		self.m_staticText6111121.SetMinSize( wx.Size( -1,20 ) )
		
		bSizer23111121.Add( self.m_staticText6111121, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer721 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer73 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1441 = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"State Machine", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_staticText1441.Wrap( -1 )
		self.m_staticText1441.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText1441.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer73.Add( self.m_staticText1441, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlIDLE_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"IDLE", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlIDLE_lbl.Wrap( -1 )
		self.ctrlIDLE_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlIDLE_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer73.Add( self.ctrlIDLE_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlINIT_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"INITIALIZATION", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlINIT_lbl.Wrap( -1 )
		self.ctrlINIT_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlINIT_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer73.Add( self.ctrlINIT_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlDONNING_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"DONNING", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlDONNING_lbl.Wrap( -1 )
		self.ctrlDONNING_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlDONNING_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer73.Add( self.ctrlDONNING_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlRESTPOS_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"REST POSITION", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlRESTPOS_lbl.Wrap( -1 )
		self.ctrlRESTPOS_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlRESTPOS_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer73.Add( self.ctrlRESTPOS_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlREADY_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"READY", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlREADY_lbl.Wrap( -1 )
		self.ctrlREADY_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlREADY_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer73.Add( self.ctrlREADY_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlRUNNING_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"RUNNING", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlRUNNING_lbl.Wrap( -1 )
		self.ctrlRUNNING_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlRUNNING_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer73.Add( self.ctrlRUNNING_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ctrlSTOP_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ctrlSTOP_lbl.Wrap( -1 )
		self.ctrlSTOP_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ctrlSTOP_lbl.SetBackgroundColour( wx.Colour( 255, 232, 232 ) )
		
		bSizer73.Add( self.ctrlSTOP_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer721.Add( bSizer73, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer74 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer107 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_control_interface = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"Control Interface", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_control_interface.Wrap( -1 )
		self.m_control_interface.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_control_interface.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer107.Add( self.m_control_interface, 0, wx.ALL|wx.EXPAND, 5 )
		
		input_choiceChoices = [ u"None" ]
		self.input_choice = wx.Choice( self.m_control_settings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, input_choiceChoices, 0 )
		self.input_choice.SetSelection( 0 )
		self.input_choice.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer107.Add( self.input_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer74.Add( bSizer107, 0, wx.EXPAND, 5 )
		
		bSizer106 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_vocal_displacement = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"Displacement", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_vocal_displacement.Wrap( -1 )
		self.m_vocal_displacement.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_vocal_displacement.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer106.Add( self.m_vocal_displacement, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.displacement_entry = wx.Slider( self.m_control_settings, wx.ID_ANY, 10, 1, 20, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer106.Add( self.displacement_entry, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer74.Add( bSizer106, 0, wx.EXPAND, 5 )
		
		bSizer1061 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_speed_gain = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"Speed Gain", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_speed_gain.Wrap( -1 )
		self.m_speed_gain.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_speed_gain.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer1061.Add( self.m_speed_gain, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.speed_gain_entry = wx.Slider( self.m_control_settings, wx.ID_ANY, 2, 1, 5, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer1061.Add( self.speed_gain_entry, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer74.Add( bSizer1061, 0, wx.EXPAND, 5 )
		
		bSizer10611 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_speed_gain1 = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"Control Mode", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_speed_gain1.Wrap( -1 )
		self.m_speed_gain1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_speed_gain1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer10611.Add( self.m_speed_gain1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.ControlMode_lbl = wx.StaticText( self.m_control_settings, wx.ID_ANY, u"OFF", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.ControlMode_lbl.Wrap( -1 )
		self.ControlMode_lbl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.ControlMode_lbl.SetBackgroundColour( wx.Colour( 242, 255, 242 ) )
		
		bSizer10611.Add( self.ControlMode_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer74.Add( bSizer10611, 1, wx.EXPAND, 5 )
		
		
		bSizer721.Add( bSizer74, 1, wx.EXPAND, 5 )
		
		
		bSizer23111121.Add( bSizer721, 1, wx.EXPAND, 5 )
		
		
		self.m_control_settings.SetSizer( bSizer23111121 )
		self.m_control_settings.Layout()
		bSizer23111121.Fit( self.m_control_settings )
		self.m_tab_settings.AddPage( self.m_control_settings, u"Control", True )
		self.m_advanced_settings = wx.Panel( self.m_tab_settings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer231111211 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText61111211 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Advanced Settings", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText61111211.Wrap( -1 )
		self.m_staticText61111211.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText61111211.SetBackgroundColour( wx.Colour( 132, 193, 255 ) )
		self.m_staticText61111211.SetMinSize( wx.Size( -1,20 ) )
		
		bSizer231111211.Add( self.m_staticText61111211, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7211 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer731 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText14411 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"IK Parameters", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_staticText14411.Wrap( -1 )
		self.m_staticText14411.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText14411.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer731.Add( self.m_staticText14411, 0, wx.EXPAND|wx.ALL, 5 )
		
		bSizerParameter1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Parameter = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Tollerance", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.Parameter.Wrap( -1 )
		self.Parameter.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Parameter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizerParameter1.Add( self.Parameter, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_tollerance_entry = wx.TextCtrl( self.m_advanced_settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.m_tollerance_entry.SetMaxSize( wx.Size( 70,-1 ) )
		
		bSizerParameter1.Add( self.m_tollerance_entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer731.Add( bSizerParameter1, 0, wx.EXPAND, 5 )
		
		bSizerParameter11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Parameter1 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Epsilon", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.Parameter1.Wrap( -1 )
		self.Parameter1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Parameter1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizerParameter11.Add( self.Parameter1, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_epsilon_entry = wx.TextCtrl( self.m_advanced_settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.m_epsilon_entry.SetMaxSize( wx.Size( 70,-1 ) )
		
		bSizerParameter11.Add( self.m_epsilon_entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer731.Add( bSizerParameter11, 0, wx.EXPAND, 5 )
		
		bSizerParameter12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Parameter2 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Wq0s", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.Parameter2.Wrap( -1 )
		self.Parameter2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Parameter2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizerParameter12.Add( self.Parameter2, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_wq0s_entry = wx.TextCtrl( self.m_advanced_settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.m_wq0s_entry.SetMaxSize( wx.Size( 70,-1 ) )
		
		bSizerParameter12.Add( self.m_wq0s_entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer731.Add( bSizerParameter12, 0, wx.EXPAND, 5 )
		
		bSizerParameter13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Parameter3 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Dol", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.Parameter3.Wrap( -1 )
		self.Parameter3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Parameter3.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizerParameter13.Add( self.Parameter3, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_dol_entry = wx.TextCtrl( self.m_advanced_settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.m_dol_entry.SetMaxSize( wx.Size( 70,-1 ) )
		
		bSizerParameter13.Add( self.m_dol_entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer731.Add( bSizerParameter13, 0, wx.EXPAND, 5 )
		
		bSizerParameter14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Parameter4 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Du", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.Parameter4.Wrap( -1 )
		self.Parameter4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Parameter4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizerParameter14.Add( self.Parameter4, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_du_entry = wx.TextCtrl( self.m_advanced_settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.m_du_entry.SetMaxSize( wx.Size( 70,-1 ) )
		
		bSizerParameter14.Add( self.m_du_entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer731.Add( bSizerParameter14, 0, wx.EXPAND, 5 )
		
		bSizerParameter15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Parameter5 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"IterMax", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.Parameter5.Wrap( -1 )
		self.Parameter5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.Parameter5.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizerParameter15.Add( self.Parameter5, 1, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_itermax_entry = wx.TextCtrl( self.m_advanced_settings, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.m_itermax_entry.SetMaxSize( wx.Size( 70,-1 ) )
		
		bSizerParameter15.Add( self.m_itermax_entry, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer731.Add( bSizerParameter15, 0, wx.EXPAND, 5 )
		
		bSizer111 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button_save_ik_parameters = wx.Button( self.m_advanced_settings, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.m_button_save_ik_parameters, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer731.Add( bSizer111, 1, wx.EXPAND, 5 )
		
		
		bSizer7211.Add( bSizer731, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer741 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1443 = wx.StaticText( self.m_advanced_settings, wx.ID_ANY, u"Advanced", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.SIMPLE_BORDER )
		self.m_staticText1443.Wrap( -1 )
		self.m_staticText1443.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText1443.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer741.Add( self.m_staticText1443, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer7211.Add( bSizer741, 1, wx.EXPAND, 5 )
		
		
		bSizer231111211.Add( bSizer7211, 1, wx.EXPAND, 5 )
		
		
		self.m_advanced_settings.SetSizer( bSizer231111211 )
		self.m_advanced_settings.Layout()
		bSizer231111211.Fit( self.m_advanced_settings )
		self.m_tab_settings.AddPage( self.m_advanced_settings, u"Advanced", False )
		
		bSizer96.Add( self.m_tab_settings, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer96, 0, wx.EXPAND, 5 )
		
		self.m_staticline221 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer4.Add( self.m_staticline221, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer221 = wx.BoxSizer( wx.VERTICAL )
		
		self.exo3d_container = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.exo3d_container.SetMinSize( wx.Size( -1,300 ) )
		
		bSizer221.Add( self.exo3d_container, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer221, 1, wx.EXPAND, 5 )
		
		
		bSizer93.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer93 )
		self.m_panel1.Layout()
		bSizer93.Fit( self.m_panel1 )
		bSizer2.Add( self.m_panel1, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText6 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joint 1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText6.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_staticText6.SetMinSize( wx.Size( 140,-1 ) )
		
		bSizer23.Add( self.m_staticText6, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.J1desc_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Abduzione/adduzione spalla", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J1desc_lbl.Wrap( -1 )
		self.J1desc_lbl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer23.Add( self.J1desc_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.J1value_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"XX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.J1value_lbl.Wrap( -1 )
		self.J1value_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer23.Add( self.J1value_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer24.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.J1min_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MIN", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J1min_lbl.Wrap( -1 )
		self.J1min_lbl.SetToolTipString( u"Min" )
		self.J1min_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24.Add( self.J1min_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		bSizer24.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.J1max_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MAX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J1max_lbl.Wrap( -1 )
		self.J1max_lbl.SetToolTipString( u"Max" )
		self.J1max_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24.Add( self.J1max_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText17 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		bSizer24.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		self.J1def_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"DEF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1def_lbl.Wrap( -1 )
		self.J1def_lbl.SetToolTipString( u"Default" )
		
		bSizer24.Add( self.J1def_lbl, 0, wx.ALL, 5 )
		
		
		bSizer24.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer23.Add( bSizer24, 0, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText168 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText168.Wrap( -1 )
		self.m_staticText168.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer25.Add( self.m_staticText168, 0, wx.ALL, 5 )
		
		self.J1initialized_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.J1initialized_lbl.Wrap( -1 )
		self.J1initialized_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J1initialized_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer25.Add( self.J1initialized_lbl, 0, wx.EXPAND, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Initialized", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer25.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		
		bSizer23.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		bSizer251 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1681 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1681.Wrap( -1 )
		self.m_staticText1681.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer251.Add( self.m_staticText1681, 0, wx.ALL, 5 )
		
		self.J1boundaries_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.J1boundaries_lbl.Wrap( -1 )
		self.J1boundaries_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J1boundaries_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer251.Add( self.J1boundaries_lbl, 0, 0, 5 )
		
		self.M1boundariesA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Boundaries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M1boundariesA_lbl.Wrap( -1 )
		bSizer251.Add( self.M1boundariesA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer23.Add( bSizer251, 0, wx.EXPAND, 5 )
		
		bSizer252 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1682 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1682.Wrap( -1 )
		self.m_staticText1682.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer252.Add( self.m_staticText1682, 0, wx.ALL, 5 )
		
		self.J1fault_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.J1fault_lbl.Wrap( -1 )
		self.J1fault_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J1fault_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer252.Add( self.J1fault_lbl, 0, 0, 5 )
		
		self.M1faultA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Fault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M1faultA_lbl.Wrap( -1 )
		bSizer252.Add( self.M1faultA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer23.Add( bSizer252, 0, wx.EXPAND, 5 )
		
		
		bSizer22.Add( bSizer23, 0, 0, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer22.Add( self.m_staticline2, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer231 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText61 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joint 2", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText61.Wrap( -1 )
		self.m_staticText61.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText61.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_staticText61.SetMinSize( wx.Size( 140,-1 ) )
		
		bSizer231.Add( self.m_staticText61, 0, wx.ALL, 5 )
		
		self.J2desc_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Flesso/estensione spalla", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J2desc_lbl.Wrap( -1 )
		self.J2desc_lbl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer231.Add( self.J2desc_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.J2value_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"XX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.J2value_lbl.Wrap( -1 )
		self.J2value_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer231.Add( self.J2value_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer241 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer241.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.J2min_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MIN", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J2min_lbl.Wrap( -1 )
		self.J2min_lbl.SetToolTipString( u"Min" )
		self.J2min_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer241.Add( self.J2min_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText191 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )
		bSizer241.Add( self.m_staticText191, 0, wx.ALL, 5 )
		
		self.J2max_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MAX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J2max_lbl.Wrap( -1 )
		self.J2max_lbl.SetToolTipString( u"Max" )
		self.J2max_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer241.Add( self.J2max_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText171 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText171.Wrap( -1 )
		bSizer241.Add( self.m_staticText171, 0, wx.ALL, 5 )
		
		self.J2def_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"DEF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2def_lbl.Wrap( -1 )
		self.J2def_lbl.SetToolTipString( u"Default" )
		
		bSizer241.Add( self.J2def_lbl, 0, wx.ALL, 5 )
		
		
		bSizer241.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer231.Add( bSizer241, 0, wx.EXPAND, 5 )
		
		bSizer253 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16821 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16821.Wrap( -1 )
		self.m_staticText16821.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer253.Add( self.m_staticText16821, 0, wx.ALL, 5 )
		
		self.J2initialized_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2initialized_lbl.Wrap( -1 )
		self.J2initialized_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J2initialized_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer253.Add( self.J2initialized_lbl, 0, wx.EXPAND, 5 )
		
		self.m_staticText123 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Initialized", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText123.Wrap( -1 )
		bSizer253.Add( self.m_staticText123, 1, wx.ALL, 5 )
		
		
		bSizer231.Add( bSizer253, 0, wx.EXPAND, 5 )
		
		bSizer2511 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16822 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16822.Wrap( -1 )
		self.m_staticText16822.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer2511.Add( self.m_staticText16822, 0, wx.ALL, 5 )
		
		self.J2boundaries_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2boundaries_lbl.Wrap( -1 )
		self.J2boundaries_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J2boundaries_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer2511.Add( self.J2boundaries_lbl, 0, 0, 5 )
		
		self.M2boundariesA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Boundaries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M2boundariesA_lbl.Wrap( -1 )
		bSizer2511.Add( self.M2boundariesA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer231.Add( bSizer2511, 0, wx.EXPAND, 5 )
		
		bSizer2521 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16823 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16823.Wrap( -1 )
		self.m_staticText16823.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer2521.Add( self.m_staticText16823, 0, wx.ALL, 5 )
		
		self.J2fault_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2fault_lbl.Wrap( -1 )
		self.J2fault_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J2fault_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer2521.Add( self.J2fault_lbl, 0, 0, 5 )
		
		self.M2faultA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Fault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M2faultA_lbl.Wrap( -1 )
		bSizer2521.Add( self.M2faultA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer231.Add( bSizer2521, 0, wx.EXPAND, 5 )
		
		
		bSizer22.Add( bSizer231, 0, 0, 5 )
		
		self.m_staticline21 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer22.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer2311 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText611 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joint 3", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText611.Wrap( -1 )
		self.m_staticText611.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText611.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_staticText611.SetMinSize( wx.Size( 140,-1 ) )
		
		bSizer2311.Add( self.m_staticText611, 0, wx.ALL, 5 )
		
		self.J3desc_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Intra/extra rotazione spalla", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J3desc_lbl.Wrap( -1 )
		self.J3desc_lbl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2311.Add( self.J3desc_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.J3value_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"XX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.J3value_lbl.Wrap( -1 )
		self.J3value_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer2311.Add( self.J3value_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2411 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer2411.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.J3min_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MIN", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J3min_lbl.Wrap( -1 )
		self.J3min_lbl.SetToolTipString( u"Min" )
		self.J3min_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer2411.Add( self.J3min_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText1911 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1911.Wrap( -1 )
		bSizer2411.Add( self.m_staticText1911, 0, wx.ALL, 5 )
		
		self.J3max_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MAX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J3max_lbl.Wrap( -1 )
		self.J3max_lbl.SetToolTipString( u"Max" )
		self.J3max_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer2411.Add( self.J3max_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText1711 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1711.Wrap( -1 )
		bSizer2411.Add( self.m_staticText1711, 0, wx.ALL, 5 )
		
		self.J3def_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"DEF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3def_lbl.Wrap( -1 )
		self.J3def_lbl.SetToolTipString( u"Default" )
		
		bSizer2411.Add( self.J3def_lbl, 0, wx.ALL, 5 )
		
		
		bSizer2411.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer2311.Add( bSizer2411, 0, wx.EXPAND, 5 )
		
		bSizer2531 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16824 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16824.Wrap( -1 )
		self.m_staticText16824.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer2531.Add( self.m_staticText16824, 0, wx.ALL, 5 )
		
		self.J3initialized_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3initialized_lbl.Wrap( -1 )
		self.J3initialized_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J3initialized_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer2531.Add( self.J3initialized_lbl, 0, wx.EXPAND, 5 )
		
		self.m_staticText1231 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Initialized", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1231.Wrap( -1 )
		bSizer2531.Add( self.m_staticText1231, 0, wx.ALL, 5 )
		
		
		bSizer2311.Add( bSizer2531, 0, wx.EXPAND, 5 )
		
		bSizer25111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16825 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16825.Wrap( -1 )
		self.m_staticText16825.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer25111.Add( self.m_staticText16825, 0, wx.ALL, 5 )
		
		self.J3boundaries_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3boundaries_lbl.Wrap( -1 )
		self.J3boundaries_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J3boundaries_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer25111.Add( self.J3boundaries_lbl, 0, 0, 5 )
		
		self.M3boundariesA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Boundaries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M3boundariesA_lbl.Wrap( -1 )
		bSizer25111.Add( self.M3boundariesA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer2311.Add( bSizer25111, 0, wx.EXPAND, 5 )
		
		bSizer25211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16826 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16826.Wrap( -1 )
		self.m_staticText16826.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer25211.Add( self.m_staticText16826, 0, wx.ALL, 5 )
		
		self.J3fault_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3fault_lbl.Wrap( -1 )
		self.J3fault_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J3fault_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer25211.Add( self.J3fault_lbl, 0, 0, 5 )
		
		self.M3faultA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Fault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M3faultA_lbl.Wrap( -1 )
		bSizer25211.Add( self.M3faultA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer2311.Add( bSizer25211, 0, wx.EXPAND, 5 )
		
		
		bSizer22.Add( bSizer2311, 0, 0, 5 )
		
		self.m_staticline211 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer22.Add( self.m_staticline211, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer23111 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText6111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joint 4", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText6111.Wrap( -1 )
		self.m_staticText6111.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText6111.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_staticText6111.SetMinSize( wx.Size( 140,-1 ) )
		
		bSizer23111.Add( self.m_staticText6111, 0, wx.ALL, 5 )
		
		self.J4desc_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Flesso/estensione gomito", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J4desc_lbl.Wrap( -1 )
		self.J4desc_lbl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer23111.Add( self.J4desc_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.J4value_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"XX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.J4value_lbl.Wrap( -1 )
		self.J4value_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer23111.Add( self.J4value_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer24111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer24111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.J4min_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MIN", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J4min_lbl.Wrap( -1 )
		self.J4min_lbl.SetToolTipString( u"Min" )
		self.J4min_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24111.Add( self.J4min_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText19111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19111.Wrap( -1 )
		bSizer24111.Add( self.m_staticText19111, 0, wx.ALL, 5 )
		
		self.J4max_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MAX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J4max_lbl.Wrap( -1 )
		self.J4max_lbl.SetToolTipString( u"Max" )
		self.J4max_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer24111.Add( self.J4max_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText17111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17111.Wrap( -1 )
		bSizer24111.Add( self.m_staticText17111, 0, wx.ALL, 5 )
		
		self.J4def_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"DEF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4def_lbl.Wrap( -1 )
		self.J4def_lbl.SetToolTipString( u"Default" )
		
		bSizer24111.Add( self.J4def_lbl, 0, wx.ALL, 5 )
		
		
		bSizer24111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer23111.Add( bSizer24111, 0, wx.EXPAND, 5 )
		
		bSizer25311 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16827 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16827.Wrap( -1 )
		self.m_staticText16827.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer25311.Add( self.m_staticText16827, 0, wx.ALL, 5 )
		
		self.J4initialized_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4initialized_lbl.Wrap( -1 )
		self.J4initialized_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J4initialized_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer25311.Add( self.J4initialized_lbl, 0, wx.EXPAND, 5 )
		
		self.m_staticText12311 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Initialized", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12311.Wrap( -1 )
		bSizer25311.Add( self.m_staticText12311, 0, wx.ALL, 5 )
		
		
		bSizer23111.Add( bSizer25311, 0, wx.EXPAND, 5 )
		
		bSizer251111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16828 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16828.Wrap( -1 )
		self.m_staticText16828.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer251111.Add( self.m_staticText16828, 0, wx.ALL, 5 )
		
		self.J4boundaries_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4boundaries_lbl.Wrap( -1 )
		self.J4boundaries_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J4boundaries_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer251111.Add( self.J4boundaries_lbl, 0, 0, 5 )
		
		self.M4boundariesA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Boundaries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M4boundariesA_lbl.Wrap( -1 )
		bSizer251111.Add( self.M4boundariesA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer23111.Add( bSizer251111, 0, wx.EXPAND, 5 )
		
		bSizer252111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16829 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16829.Wrap( -1 )
		self.m_staticText16829.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer252111.Add( self.m_staticText16829, 0, wx.ALL, 5 )
		
		self.J4fault_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4fault_lbl.Wrap( -1 )
		self.J4fault_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J4fault_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer252111.Add( self.J4fault_lbl, 0, 0, 5 )
		
		self.M4faultA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Fault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M4faultA_lbl.Wrap( -1 )
		bSizer252111.Add( self.M4faultA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer23111.Add( bSizer252111, 0, wx.EXPAND, 5 )
		
		
		bSizer22.Add( bSizer23111, 0, 0, 5 )
		
		self.m_staticline2111 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer22.Add( self.m_staticline2111, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer231111 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText61111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joint 5", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText61111.Wrap( -1 )
		self.m_staticText61111.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText61111.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_staticText61111.SetMinSize( wx.Size( 140,-1 ) )
		
		bSizer231111.Add( self.m_staticText61111, 0, wx.ALL, 5 )
		
		self.J5desc_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Pronazione/supinaz. polso", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J5desc_lbl.Wrap( -1 )
		self.J5desc_lbl.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer231111.Add( self.J5desc_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.J5value_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"XX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.J5value_lbl.Wrap( -1 )
		self.J5value_lbl.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer231111.Add( self.J5value_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer241111 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer241111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.J5min_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MIN", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J5min_lbl.Wrap( -1 )
		self.J5min_lbl.SetToolTipString( u"Min" )
		self.J5min_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer241111.Add( self.J5min_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText191111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191111.Wrap( -1 )
		bSizer241111.Add( self.m_staticText191111, 0, wx.ALL, 5 )
		
		self.J5max_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MAX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.J5max_lbl.Wrap( -1 )
		self.J5max_lbl.SetToolTipString( u"Max" )
		self.J5max_lbl.SetMinSize( wx.Size( 30,-1 ) )
		
		bSizer241111.Add( self.J5max_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText171111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"|", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText171111.Wrap( -1 )
		bSizer241111.Add( self.m_staticText171111, 0, wx.ALL, 5 )
		
		self.J5def_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"DEF", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5def_lbl.Wrap( -1 )
		self.J5def_lbl.SetToolTipString( u"Default" )
		
		bSizer241111.Add( self.J5def_lbl, 0, wx.ALL, 5 )
		
		
		bSizer241111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer231111.Add( bSizer241111, 0, wx.EXPAND, 5 )
		
		bSizer253111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText168210 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText168210.Wrap( -1 )
		self.m_staticText168210.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer253111.Add( self.m_staticText168210, 0, wx.ALL, 5 )
		
		self.J5initialized_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5initialized_lbl.Wrap( -1 )
		self.J5initialized_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J5initialized_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer253111.Add( self.J5initialized_lbl, 0, wx.EXPAND, 5 )
		
		self.m_staticText123111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Initialized", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText123111.Wrap( -1 )
		bSizer253111.Add( self.m_staticText123111, 0, wx.ALL, 5 )
		
		
		bSizer231111.Add( bSizer253111, 0, wx.EXPAND, 5 )
		
		bSizer2511111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText168211 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText168211.Wrap( -1 )
		self.m_staticText168211.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer2511111.Add( self.m_staticText168211, 0, wx.ALL, 5 )
		
		self.J5boundaries_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5boundaries_lbl.Wrap( -1 )
		self.J5boundaries_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J5boundaries_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer2511111.Add( self.J5boundaries_lbl, 0, 0, 5 )
		
		self.M5boundariesA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Boundaries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M5boundariesA_lbl.Wrap( -1 )
		bSizer2511111.Add( self.M5boundariesA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer231111.Add( bSizer2511111, 0, wx.EXPAND, 5 )
		
		bSizer2521111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText168212 = wx.StaticText( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText168212.Wrap( -1 )
		self.m_staticText168212.SetMinSize( wx.Size( 0,-1 ) )
		
		bSizer2521111.Add( self.m_staticText168212, 0, wx.ALL, 5 )
		
		self.J5fault_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5fault_lbl.Wrap( -1 )
		self.J5fault_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.J5fault_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer2521111.Add( self.J5fault_lbl, 0, 0, 5 )
		
		self.M5faultA_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Fault", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.M5faultA_lbl.Wrap( -1 )
		bSizer2521111.Add( self.M5faultA_lbl, 0, wx.ALL, 5 )
		
		
		bSizer231111.Add( bSizer2521111, 0, wx.EXPAND, 5 )
		
		
		bSizer22.Add( bSizer231111, 0, 0, 5 )
		
		self.m_staticline21111 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer22.Add( self.m_staticline21111, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer2311111 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText611111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Saved Positions", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText611111.Wrap( -1 )
		self.m_staticText611111.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText611111.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self.m_staticText611111.SetMinSize( wx.Size( 120,-1 ) )
		
		bSizer2311111.Add( self.m_staticText611111, 0, wx.ALL|wx.EXPAND, 5 )
		
		SavedPositions_listChoices = []
		self.SavedPositions_list = wx.ListBox( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, SavedPositions_listChoices, 0 )
		bSizer2311111.Add( self.SavedPositions_list, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer22.Add( bSizer2311111, 1, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer22 )
		self.m_panel6.Layout()
		bSizer22.Fit( self.m_panel6 )
		bSizer21.Add( self.m_panel6, 0, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		bSizer72 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.connect_butt = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.connect_butt, 0, wx.ALL, 5 )
		
		self.disconnect_butt = wx.Button( self, wx.ID_ANY, u"Disconnect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.disconnect_butt, 0, wx.ALL, 5 )
		
		self.init_butt = wx.Button( self, wx.ID_ANY, u"Init Sys", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.init_butt, 0, wx.ALL, 5 )
		
		self.enableCtrl_butt = wx.Button( self, wx.ID_ANY, u"Enable Ctrl", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.enableCtrl_butt, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.disableCtrl_butt = wx.Button( self, wx.ID_ANY, u"Disable Ctrl", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.disableCtrl_butt, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.savePos_butt = wx.Button( self, wx.ID_ANY, u"Save Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.savePos_butt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.gotoPos_butt = wx.Button( self, wx.ID_ANY, u"Go to Saved Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.gotoPos_butt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.stop_butt = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.stop_butt, 0, wx.ALL, 5 )
		
		
		bSizer72.Add( bSizer17, 1, 0, 5 )
		
		
		bSizer2.Add( bSizer72, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.connect_command, id = self.m_menuItem1.GetId() )
		self.Bind( wx.EVT_MENU, self.exit, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.exo_setup_command, id = self.m_preferences.GetId() )
		self.Bind( wx.EVT_MENU, self.patient_setup_command, id = self.m_patient.GetId() )
		self.input_choice.Bind( wx.EVT_CHOICE, self.set_control_interface )
		self.displacement_entry.Bind( wx.EVT_SCROLL_THUMBRELEASE, self.set_displacement )
		self.speed_gain_entry.Bind( wx.EVT_SCROLL_THUMBRELEASE, self.set_speed_gain )
		self.m_button_save_ik_parameters.Bind( wx.EVT_BUTTON, self.save_ik_parameters )
		self.connect_butt.Bind( wx.EVT_BUTTON, self.connect_command )
		self.disconnect_butt.Bind( wx.EVT_BUTTON, self.disconnect_command )
		self.init_butt.Bind( wx.EVT_BUTTON, self.initialize_system_command )
		self.enableCtrl_butt.Bind( wx.EVT_BUTTON, self.enable_control_command )
		self.disableCtrl_butt.Bind( wx.EVT_BUTTON, self.disable_control_command )
		self.savePos_butt.Bind( wx.EVT_BUTTON, self.save_position_command )
		self.gotoPos_butt.Bind( wx.EVT_BUTTON, self.goto_position_command )
		self.stop_butt.Bind( wx.EVT_BUTTON, self.exit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def connect_command( self, event ):
		event.Skip()
	
	def exit( self, event ):
		event.Skip()
	
	def exo_setup_command( self, event ):
		event.Skip()
	
	def patient_setup_command( self, event ):
		event.Skip()
	
	def set_control_interface( self, event ):
		event.Skip()
	
	def set_displacement( self, event ):
		event.Skip()
	
	def set_speed_gain( self, event ):
		event.Skip()
	
	def save_ik_parameters( self, event ):
		event.Skip()
	
	
	def disconnect_command( self, event ):
		event.Skip()
	
	def initialize_system_command( self, event ):
		event.Skip()
	
	def enable_control_command( self, event ):
		event.Skip()
	
	def disable_control_command( self, event ):
		event.Skip()
	
	def save_position_command( self, event ):
		event.Skip()
	
	def goto_position_command( self, event ):
		event.Skip()
	
	

###########################################################################
## Class DialogDonning
###########################################################################

class DialogDonning ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Donning", pos = wx.DefaultPosition, size = wx.Size( 645,238 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer71 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer72 = wx.BoxSizer( wx.VERTICAL )
		
		self.error_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Please don the BRIDGE exoskeleton.\nPlease carefully follow the instructions reported on the user's manual.\nWhen donning is complete, press the OK button.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.error_lbl.Wrap( -1 )
		self.error_lbl.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.error_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer72.Add( self.error_lbl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer73 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer73.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.cancel_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer73.Add( self.cancel_butt, 0, wx.ALL, 5 )
		
		self.m_button27 = wx.Button( self.m_panel6, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer73.Add( self.m_button27, 0, wx.ALL, 5 )
		
		
		bSizer72.Add( bSizer73, 0, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer72 )
		self.m_panel6.Layout()
		bSizer72.Fit( self.m_panel6 )
		bSizer71.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer71 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_butt.Bind( wx.EVT_BUTTON, self.cancel_command )
		self.m_button27.Bind( wx.EVT_BUTTON, self.ok_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancel_command( self, event ):
		event.Skip()
	
	def ok_command( self, event ):
		event.Skip()
	

###########################################################################
## Class DialogExoSetup
###########################################################################

class DialogExoSetup ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Exoskeleton Setup", pos = wx.DefaultPosition, size = wx.Size( 396,605 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Joint 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText8.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer12.Add( self.m_staticText8, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText127 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Abduzione/adduzione spalla", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText127.Wrap( -1 )
		self.m_staticText127.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer12.Add( self.m_staticText127, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		choice_COM_M1Choices = []
		self.choice_COM_M1 = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), choice_COM_M1Choices, 0 )
		self.choice_COM_M1.SetSelection( 0 )
		bSizer12.Add( self.choice_COM_M1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.J1test_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer12.Add( self.J1test_butt, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Joint 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		self.m_staticText9.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText9.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer13.Add( self.m_staticText9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText128 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Flesso/estensione spalla", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText128.Wrap( -1 )
		self.m_staticText128.SetMinSize( wx.Size( 80,-1 ) )
		
		bSizer13.Add( self.m_staticText128, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		choice_COM_M2Choices = []
		self.choice_COM_M2 = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), choice_COM_M2Choices, 0 )
		self.choice_COM_M2.SetSelection( 0 )
		bSizer13.Add( self.choice_COM_M2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.J2test_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer13.Add( self.J2test_butt, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer13, 0, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Joint 3", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText10.Wrap( -1 )
		self.m_staticText10.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText10.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer15.Add( self.m_staticText10, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText129 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Intra/extra rotazione spalla", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText129.Wrap( -1 )
		self.m_staticText129.SetMinSize( wx.Size( 80,-1 ) )
		
		bSizer15.Add( self.m_staticText129, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		choice_COM_M3Choices = []
		self.choice_COM_M3 = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), choice_COM_M3Choices, 0 )
		self.choice_COM_M3.SetSelection( 0 )
		bSizer15.Add( self.choice_COM_M3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.J3test_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer15.Add( self.J3test_butt, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText11 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Joint 4", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText11.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer16.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText130 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Flesso/estensione gomito", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText130.Wrap( -1 )
		self.m_staticText130.SetMinSize( wx.Size( 80,-1 ) )
		
		bSizer16.Add( self.m_staticText130, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		choice_COM_M4Choices = []
		self.choice_COM_M4 = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), choice_COM_M4Choices, 0 )
		self.choice_COM_M4.SetSelection( 0 )
		bSizer16.Add( self.choice_COM_M4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.J4test_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer16.Add( self.J4test_butt, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Joint 5", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText12.Wrap( -1 )
		self.m_staticText12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText12.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer17.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText131 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Pronazione/supinazione polso", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )
		self.m_staticText131.SetMinSize( wx.Size( 80,-1 ) )
		
		bSizer17.Add( self.m_staticText131, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		choice_COM_M5Choices = []
		self.choice_COM_M5 = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 80,-1 ), choice_COM_M5Choices, 0 )
		self.choice_COM_M5.SetSelection( 0 )
		bSizer17.Add( self.choice_COM_M5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.J5test_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.J5test_butt.Enable( False )
		
		bSizer17.Add( self.J5test_butt, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer17, 0, wx.EXPAND, 5 )
		
		
		bSizer11.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer95 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline14 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer95.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer901 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1501 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"JOINT", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText1501.Wrap( -1 )
		self.m_staticText1501.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText1501.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer901.Add( self.m_staticText1501, 0, wx.ALL, 5 )
		
		self.m_staticText161 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"MIN", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText161.Wrap( -1 )
		self.m_staticText161.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText161.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer901.Add( self.m_staticText161, 0, wx.ALL, 5 )
		
		self.m_staticText162 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"MAX", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText162.Wrap( -1 )
		self.m_staticText162.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText162.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer901.Add( self.m_staticText162, 0, wx.ALL, 5 )
		
		self.m_staticText166 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"OFFSET", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText166.Wrap( -1 )
		self.m_staticText166.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText166.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer901.Add( self.m_staticText166, 0, wx.ALL, 5 )
		
		self.m_staticText167 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"RATIO", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText167.Wrap( -1 )
		self.m_staticText167.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText167.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer901.Add( self.m_staticText167, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer901, 0, wx.EXPAND, 5 )
		
		bSizer9011 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15011 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"J1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15011.Wrap( -1 )
		self.m_staticText15011.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9011.Add( self.m_staticText15011, 0, wx.ALL, 5 )
		
		self.J1min_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1min_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9011.Add( self.J1min_entry, 0, wx.ALL, 5 )
		
		self.J1max_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1max_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9011.Add( self.J1max_entry, 0, wx.ALL, 5 )
		
		self.J1offset_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1offset_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9011.Add( self.J1offset_entry, 0, wx.ALL, 5 )
		
		self.J1ratio_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1ratio_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9011.Add( self.J1ratio_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9011, 0, wx.EXPAND, 5 )
		
		bSizer9012 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15012 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"J2", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15012.Wrap( -1 )
		self.m_staticText15012.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9012.Add( self.m_staticText15012, 0, wx.ALL, 5 )
		
		self.J2min_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2min_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9012.Add( self.J2min_entry, 0, wx.ALL, 5 )
		
		self.J2max_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2max_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9012.Add( self.J2max_entry, 0, wx.ALL, 5 )
		
		self.J2offset_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2offset_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9012.Add( self.J2offset_entry, 0, wx.ALL, 5 )
		
		self.J2ratio_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2ratio_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9012.Add( self.J2ratio_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9012, 0, wx.EXPAND, 5 )
		
		bSizer9013 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15013 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"J3", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15013.Wrap( -1 )
		self.m_staticText15013.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9013.Add( self.m_staticText15013, 0, wx.ALL, 5 )
		
		self.J3min_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3min_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9013.Add( self.J3min_entry, 0, wx.ALL, 5 )
		
		self.J3max_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3max_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9013.Add( self.J3max_entry, 0, wx.ALL, 5 )
		
		self.J3offset_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3offset_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9013.Add( self.J3offset_entry, 0, wx.ALL, 5 )
		
		self.J3ratio_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3ratio_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9013.Add( self.J3ratio_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9013, 0, wx.EXPAND, 5 )
		
		bSizer9014 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15014 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"J4", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15014.Wrap( -1 )
		self.m_staticText15014.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9014.Add( self.m_staticText15014, 0, wx.ALL, 5 )
		
		self.J4min_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4min_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9014.Add( self.J4min_entry, 0, wx.ALL, 5 )
		
		self.J4max_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4max_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9014.Add( self.J4max_entry, 0, wx.ALL, 5 )
		
		self.J4offset_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4offset_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9014.Add( self.J4offset_entry, 0, wx.ALL, 5 )
		
		self.J4ratio_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4ratio_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer9014.Add( self.J4ratio_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9014, 0, wx.EXPAND, 5 )
		
		bSizer90141 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText150141 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"J5", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText150141.Wrap( -1 )
		self.m_staticText150141.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer90141.Add( self.m_staticText150141, 0, wx.ALL, 5 )
		
		self.J5min_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5min_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer90141.Add( self.J5min_entry, 0, wx.ALL, 5 )
		
		self.J5max_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5max_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer90141.Add( self.J5max_entry, 0, wx.ALL, 5 )
		
		self.J5offset_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5offset_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer90141.Add( self.J5offset_entry, 0, wx.ALL, 5 )
		
		self.J5ratio_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5ratio_entry.SetMinSize( wx.Size( 60,-1 ) )
		
		bSizer90141.Add( self.J5ratio_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer90141, 0, wx.EXPAND, 5 )
		
		
		bSizer95.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer95, 1, wx.EXPAND, 5 )
		
		bSizer171 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.error_lbl = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Error", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.error_lbl.Wrap( -1 )
		self.error_lbl.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.error_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		self.error_lbl.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer171.Add( self.error_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer171, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer18.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.ok_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.ok_butt, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_button5 = wx.Button( self.m_panel4, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_button5, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer18, 0, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer11 )
		self.m_panel4.Layout()
		bSizer11.Fit( self.m_panel4 )
		bSizer10.Add( self.m_panel4, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.J1test_butt.Bind( wx.EVT_BUTTON, self.test_command )
		self.J2test_butt.Bind( wx.EVT_BUTTON, self.test_command )
		self.J3test_butt.Bind( wx.EVT_BUTTON, self.test_command )
		self.J4test_butt.Bind( wx.EVT_BUTTON, self.test_command )
		self.J5test_butt.Bind( wx.EVT_BUTTON, self.test_command )
		self.J1min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J1max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J1offset_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J1ratio_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2offset_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2ratio_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3offset_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3ratio_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4offset_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4ratio_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5offset_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5ratio_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.ok_butt.Bind( wx.EVT_BUTTON, self.ok_command )
		self.m_button5.Bind( wx.EVT_BUTTON, self.cancel_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def test_command( self, event ):
		event.Skip()
	
	
	
	
	
	def onText_command( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	def ok_command( self, event ):
		event.Skip()
	
	def cancel_command( self, event ):
		event.Skip()
	

###########################################################################
## Class Dialog_PatientSetup
###########################################################################

class Dialog_PatientSetup ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Patient Setup", pos = wx.DefaultPosition, size = wx.Size( 384,565 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer89 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel6.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer95 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer90 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText150 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Patient Name", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText150.Wrap( -1 )
		self.m_staticText150.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText150.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer90.Add( self.m_staticText150, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.patientName_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer90.Add( self.patientName_entry, 1, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer90, 0, wx.EXPAND, 5 )
		
		bSizer902 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer95.Add( bSizer902, 1, wx.EXPAND, 5 )
		
		self.m_staticline14 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer95.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer901 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1501 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joint", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText1501.Wrap( -1 )
		self.m_staticText1501.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText1501.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_staticText1501.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer901.Add( self.m_staticText1501, 0, wx.ALL, 5 )
		
		self.m_staticText161 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Min", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText161.Wrap( -1 )
		self.m_staticText161.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText161.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer901.Add( self.m_staticText161, 0, wx.ALL, 5 )
		
		self.m_staticText162 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Max", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText162.Wrap( -1 )
		self.m_staticText162.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText162.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer901.Add( self.m_staticText162, 0, wx.ALL, 5 )
		
		self.m_staticText163 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Donning", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText163.Wrap( -1 )
		self.m_staticText163.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText163.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer901.Add( self.m_staticText163, 0, wx.ALL, 5 )
		
		self.m_staticText167 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Rest", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText167.Wrap( -1 )
		self.m_staticText167.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText167.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer901.Add( self.m_staticText167, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer901, 0, wx.EXPAND, 5 )
		
		bSizer9011 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15011 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"J1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15011.Wrap( -1 )
		self.m_staticText15011.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9011.Add( self.m_staticText15011, 0, wx.ALL, 5 )
		
		self.J1min_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1min_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9011.Add( self.J1min_entry, 0, wx.ALL, 5 )
		
		self.J1max_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1max_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9011.Add( self.J1max_entry, 0, wx.ALL, 5 )
		
		self.J1def_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J1def_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9011.Add( self.J1def_entry, 0, wx.ALL, 5 )
		
		self.J1rest_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.J1rest_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9011.Add( self.J1rest_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9011, 0, wx.EXPAND, 5 )
		
		bSizer9012 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15012 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"J2", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15012.Wrap( -1 )
		self.m_staticText15012.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9012.Add( self.m_staticText15012, 0, wx.ALL, 5 )
		
		self.J2min_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2min_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9012.Add( self.J2min_entry, 0, wx.ALL, 5 )
		
		self.J2max_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2max_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9012.Add( self.J2max_entry, 0, wx.ALL, 5 )
		
		self.J2def_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J2def_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9012.Add( self.J2def_entry, 0, wx.ALL, 5 )
		
		self.J2rest_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.J2rest_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9012.Add( self.J2rest_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9012, 0, wx.EXPAND, 5 )
		
		bSizer9013 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15013 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"J3", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15013.Wrap( -1 )
		self.m_staticText15013.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9013.Add( self.m_staticText15013, 0, wx.ALL, 5 )
		
		self.J3min_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3min_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9013.Add( self.J3min_entry, 0, wx.ALL, 5 )
		
		self.J3max_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3max_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9013.Add( self.J3max_entry, 0, wx.ALL, 5 )
		
		self.J3def_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J3def_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9013.Add( self.J3def_entry, 0, wx.ALL, 5 )
		
		self.J3rest_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.J3rest_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9013.Add( self.J3rest_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9013, 0, wx.EXPAND, 5 )
		
		bSizer9014 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15014 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"J4", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText15014.Wrap( -1 )
		self.m_staticText15014.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer9014.Add( self.m_staticText15014, 0, wx.ALL, 5 )
		
		self.J4min_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4min_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9014.Add( self.J4min_entry, 0, wx.ALL, 5 )
		
		self.J4max_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4max_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9014.Add( self.J4max_entry, 0, wx.ALL, 5 )
		
		self.J4def_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J4def_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9014.Add( self.J4def_entry, 0, wx.ALL, 5 )
		
		self.J4rest_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.J4rest_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9014.Add( self.J4rest_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer9014, 0, wx.EXPAND, 5 )
		
		bSizer90141 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText150141 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"J5", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText150141.Wrap( -1 )
		self.m_staticText150141.SetMinSize( wx.Size( 50,-1 ) )
		
		bSizer90141.Add( self.m_staticText150141, 0, wx.ALL, 5 )
		
		self.J5min_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, u"N.A.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5min_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer90141.Add( self.J5min_entry, 0, wx.ALL, 5 )
		
		self.J5max_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, u"N.A.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5max_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer90141.Add( self.J5max_entry, 0, wx.ALL, 5 )
		
		self.J5def_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, u"N.A.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.J5def_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer90141.Add( self.J5def_entry, 0, wx.ALL, 5 )
		
		self.J5rest_entry = wx.TextCtrl( self.m_panel6, wx.ID_ANY, u"N.A.", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.J5rest_entry.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer90141.Add( self.J5rest_entry, 0, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer90141, 0, wx.EXPAND, 5 )
		
		self.m_staticline141 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer95.Add( self.m_staticline141, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer99 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer99.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText1631 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"L1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1631.Wrap( -1 )
		self.m_staticText1631.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer99.Add( self.m_staticText1631, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.l1_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.l1_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer99.Add( self.l1_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText164 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"L2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText164.Wrap( -1 )
		self.m_staticText164.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer99.Add( self.m_staticText164, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.l2_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.l2_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer99.Add( self.l2_lbl, 0, wx.ALL, 5 )
		
		self.m_staticText165 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"L3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText165.Wrap( -1 )
		self.m_staticText165.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer99.Add( self.m_staticText165, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.l3_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.l3_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer99.Add( self.l3_lbl, 0, wx.ALL, 5 )
		
		
		bSizer99.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer95.Add( bSizer99, 0, wx.EXPAND, 5 )
		
		self.m_staticline1411 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer95.Add( self.m_staticline1411, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer901411 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1501411 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joystick ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText1501411.Wrap( -1 )
		self.m_staticText1501411.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText1501411.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_staticText1501411.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer901411.Add( self.m_staticText1501411, 1, wx.ALL, 5 )
		
		
		bSizer95.Add( bSizer901411, 0, wx.EXPAND, 5 )
		
		bSizer991 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer991.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText16311 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Forward", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText16311.Wrap( -1 )
		self.m_staticText16311.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer991.Add( self.m_staticText16311, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.joystick_forward_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.joystick_forward_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer991.Add( self.joystick_forward_lbl, 0, wx.ALL, 5 )
		
		
		bSizer991.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText1641 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Backward", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText1641.Wrap( -1 )
		self.m_staticText1641.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer991.Add( self.m_staticText1641, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.joystick_backward_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.joystick_backward_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer991.Add( self.joystick_backward_lbl, 0, wx.ALL, 5 )
		
		
		bSizer991.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer95.Add( bSizer991, 0, wx.EXPAND, 5 )
		
		bSizer9911 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer9911.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText163111 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Left", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText163111.Wrap( -1 )
		self.m_staticText163111.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer9911.Add( self.m_staticText163111, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.joystick_left_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.joystick_left_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9911.Add( self.joystick_left_lbl, 0, wx.ALL, 5 )
		
		
		bSizer9911.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText16411 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Right", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText16411.Wrap( -1 )
		self.m_staticText16411.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer9911.Add( self.m_staticText16411, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.joystick_right_lbl = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.joystick_right_lbl.SetMinSize( wx.Size( 70,-1 ) )
		
		bSizer9911.Add( self.joystick_right_lbl, 0, wx.ALL, 5 )
		
		
		bSizer9911.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer95.Add( bSizer9911, 0, wx.EXPAND, 5 )
		
		bSizer118 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer118.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText179 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Joystick Control:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText179.Wrap( -1 )
		bSizer118.Add( self.m_staticText179, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.joystick_calibration_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Calibration", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer118.Add( self.joystick_calibration_butt, 1, wx.ALL, 5 )
		
		
		bSizer118.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer95.Add( bSizer118, 0, wx.EXPAND, 5 )
		
		self.m_staticline1412 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer95.Add( self.m_staticline1412, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer116 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer116.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.load_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.load_butt.SetMaxSize( wx.Size( 80,-1 ) )
		
		bSizer116.Add( self.load_butt, 0, wx.ALL, 5 )
		
		self.save_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.save_butt.SetMaxSize( wx.Size( 80,-1 ) )
		
		bSizer116.Add( self.save_butt, 0, wx.ALL, 5 )
		
		self.ok_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_butt.SetMaxSize( wx.Size( 80,-1 ) )
		
		bSizer116.Add( self.ok_butt, 0, wx.ALL, 5 )
		
		self.cancel_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cancel_butt.SetMaxSize( wx.Size( 80,-1 ) )
		
		bSizer116.Add( self.cancel_butt, 0, wx.ALL, 5 )
		
		
		bSizer116.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer95.Add( bSizer116, 1, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer95 )
		self.m_panel6.Layout()
		bSizer95.Fit( self.m_panel6 )
		bSizer89.Add( self.m_panel6, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer89 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.J1min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J1max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J1def_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J2def_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J3def_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J4def_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5min_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5max_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.J5def_entry.Bind( wx.EVT_TEXT, self.onText_command )
		self.joystick_calibration_butt.Bind( wx.EVT_BUTTON, self.joystick_calibration_command )
		self.load_butt.Bind( wx.EVT_BUTTON, self.load_command )
		self.save_butt.Bind( wx.EVT_BUTTON, self.save_command )
		self.ok_butt.Bind( wx.EVT_BUTTON, self.ok_command )
		self.cancel_butt.Bind( wx.EVT_BUTTON, self.cancel_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onText_command( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	def joystick_calibration_command( self, event ):
		event.Skip()
	
	def load_command( self, event ):
		event.Skip()
	
	def save_command( self, event ):
		event.Skip()
	
	def ok_command( self, event ):
		event.Skip()
	
	def cancel_command( self, event ):
		event.Skip()
	

###########################################################################
## Class Dialog_Alert
###########################################################################

class Dialog_Alert ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Alert", pos = wx.DefaultPosition, size = wx.Size( 400,160 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer71 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer72 = wx.BoxSizer( wx.VERTICAL )
		
		self.alert_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.alert_lbl.Wrap( -1 )
		self.alert_lbl.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.alert_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer72.Add( self.alert_lbl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer73 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer73.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.cancel_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer73.Add( self.cancel_butt, 0, wx.ALL, 5 )
		
		
		bSizer72.Add( bSizer73, 0, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer72 )
		self.m_panel6.Layout()
		bSizer72.Fit( self.m_panel6 )
		bSizer71.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer71 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_butt.Bind( wx.EVT_BUTTON, self.cancel_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancel_command( self, event ):
		event.Skip()
	

###########################################################################
## Class Dialog_Error
###########################################################################

class Dialog_Error ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Error", pos = wx.DefaultPosition, size = wx.Size( 400,160 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer71 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer72 = wx.BoxSizer( wx.VERTICAL )
		
		self.error_lbl = wx.StaticText( self.m_panel6, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.error_lbl.Wrap( -1 )
		self.error_lbl.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.error_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		
		bSizer72.Add( self.error_lbl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer73 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer73.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.cancel_butt = wx.Button( self.m_panel6, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer73.Add( self.cancel_butt, 0, wx.ALL, 5 )
		
		
		bSizer72.Add( bSizer73, 0, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer72 )
		self.m_panel6.Layout()
		bSizer72.Fit( self.m_panel6 )
		bSizer71.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer71 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_butt.Bind( wx.EVT_BUTTON, self.cancel_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def cancel_command( self, event ):
		event.Skip()
	

###########################################################################
## Class BridgeTerminal
###########################################################################

class BridgeTerminal ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"BRIDGE - Terminal", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer75 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel7 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel7.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer76 = wx.BoxSizer( wx.VERTICAL )
		
		self.show_terminal = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.show_terminal.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.show_terminal.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer76.Add( self.show_terminal, 1, wx.EXPAND, 5 )
		
		
		self.m_panel7.SetSizer( bSizer76 )
		self.m_panel7.Layout()
		bSizer76.Fit( self.m_panel7 )
		bSizer75.Add( self.m_panel7, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer75 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class Dialog_Joint
###########################################################################

class Dialog_Joint ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Joint", pos = wx.DefaultPosition, size = wx.Size( 249,203 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer144 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText224 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Joint Manual Setup", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText224.Wrap( -1 )
		self.m_staticText224.SetFont( wx.Font( 12, 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer144.Add( self.m_staticText224, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.joint_lbl = wx.StaticText( self.m_panel4, wx.ID_ANY, u"J", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.joint_lbl.Wrap( -1 )
		bSizer144.Add( self.joint_lbl, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer144, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button44 = wx.Button( self.m_panel4, wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer12.Add( self.m_button44, 0, wx.ALL, 5 )
		
		self.angle_entry = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		bSizer12.Add( self.angle_entry, 0, wx.ALL, 5 )
		
		self.m_button45 = wx.Button( self.m_panel4, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		bSizer12.Add( self.m_button45, 0, wx.ALL, 5 )
		
		self.J1test_butt = wx.Button( self.m_panel4, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer12.Add( self.J1test_butt, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		
		bSizer11.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer171 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.error_lbl = wx.StaticText( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.error_lbl.Wrap( -1 )
		self.error_lbl.SetFont( wx.Font( 11, 70, 90, 92, False, wx.EmptyString ) )
		self.error_lbl.SetForegroundColour( wx.Colour( 255, 0, 0 ) )
		self.error_lbl.SetMinSize( wx.Size( 40,-1 ) )
		
		bSizer171.Add( self.error_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer171, 1, wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer18.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button5 = wx.Button( self.m_panel4, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_button5, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer18, 0, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer11 )
		self.m_panel4.Layout()
		bSizer11.Fit( self.m_panel4 )
		bSizer10.Add( self.m_panel4, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button44.Bind( wx.EVT_BUTTON, self.minus_command )
		self.m_button45.Bind( wx.EVT_BUTTON, self.plus_command )
		self.J1test_butt.Bind( wx.EVT_BUTTON, self.go_command )
		self.m_button5.Bind( wx.EVT_BUTTON, self.cancel_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def minus_command( self, event ):
		event.Skip()
	
	def plus_command( self, event ):
		event.Skip()
	
	def go_command( self, event ):
		event.Skip()
	
	def cancel_command( self, event ):
		event.Skip()
	

###########################################################################
## Class Dialog_JoystickCalibration
###########################################################################

class Dialog_JoystickCalibration ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bridge - Joystick Calibration", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Forward: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer12.Add( self.m_staticText8, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer12.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.JoystickCalibrationValues0_lbl = wx.StaticText( self, wx.ID_ANY, u"--", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibrationValues0_lbl.Wrap( -1 )
		self.JoystickCalibrationValues0_lbl.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer12.Add( self.JoystickCalibrationValues0_lbl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.JoystickCalibration0_lbl = wx.StaticText( self, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibration0_lbl.Wrap( -1 )
		self.JoystickCalibration0_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.JoystickCalibration0_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer12.Add( self.JoystickCalibration0_lbl, 0, wx.ALL, 5 )
		
		self.calib_butt1 = wx.Button( self, wx.ID_ANY, u"Calibrate", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer12.Add( self.calib_butt1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText81 = wx.StaticText( self, wx.ID_ANY, u"Backward:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )
		self.m_staticText81.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer121.Add( self.m_staticText81, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer121.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.JoystickCalibrationValues1_lbl = wx.StaticText( self, wx.ID_ANY, u"--", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibrationValues1_lbl.Wrap( -1 )
		self.JoystickCalibrationValues1_lbl.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer121.Add( self.JoystickCalibrationValues1_lbl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.JoystickCalibration1_lbl = wx.StaticText( self, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibration1_lbl.Wrap( -1 )
		self.JoystickCalibration1_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.JoystickCalibration1_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer121.Add( self.JoystickCalibration1_lbl, 0, wx.ALL, 5 )
		
		self.calib_butt2 = wx.Button( self, wx.ID_ANY, u"Calibrate", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer121.Add( self.calib_butt2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer121, 1, wx.EXPAND, 5 )
		
		bSizer122 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText82 = wx.StaticText( self, wx.ID_ANY, u"Left:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82.Wrap( -1 )
		self.m_staticText82.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer122.Add( self.m_staticText82, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer122.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.JoystickCalibrationValues2_lbl = wx.StaticText( self, wx.ID_ANY, u"--", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibrationValues2_lbl.Wrap( -1 )
		self.JoystickCalibrationValues2_lbl.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer122.Add( self.JoystickCalibrationValues2_lbl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.JoystickCalibration2_lbl = wx.StaticText( self, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibration2_lbl.Wrap( -1 )
		self.JoystickCalibration2_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.JoystickCalibration2_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer122.Add( self.JoystickCalibration2_lbl, 0, wx.ALL, 5 )
		
		self.calib_butt3 = wx.Button( self, wx.ID_ANY, u"Calibrate", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer122.Add( self.calib_butt3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer122, 1, wx.EXPAND, 5 )
		
		bSizer123 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText83 = wx.StaticText( self, wx.ID_ANY, u"Right:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText83.Wrap( -1 )
		self.m_staticText83.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer123.Add( self.m_staticText83, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer123.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.JoystickCalibrationValues3_lbl = wx.StaticText( self, wx.ID_ANY, u"--", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibrationValues3_lbl.Wrap( -1 )
		self.JoystickCalibrationValues3_lbl.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer123.Add( self.JoystickCalibrationValues3_lbl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.JoystickCalibration3_lbl = wx.StaticText( self, wx.ID_ANY, u"○", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.JoystickCalibration3_lbl.Wrap( -1 )
		self.JoystickCalibration3_lbl.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		self.JoystickCalibration3_lbl.SetForegroundColour( wx.Colour( 128, 255, 128 ) )
		
		bSizer123.Add( self.JoystickCalibration3_lbl, 0, wx.ALL, 5 )
		
		self.calib_butt4 = wx.Button( self, wx.ID_ANY, u"Calibrate", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer123.Add( self.calib_butt4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer123, 1, wx.EXPAND, 5 )
		
		self.m_staticline14 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer171 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer171.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button34 = wx.Button( self, wx.ID_ANY, u"Ok ", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_button34, 0, wx.ALL, 5 )
		
		
		bSizer171.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer171, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer11 )
		self.Layout()
		bSizer11.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.calib_butt1.Bind( wx.EVT_BUTTON, self.joystick_calibration_command_axis )
		self.calib_butt2.Bind( wx.EVT_BUTTON, self.joystick_calibration_command_axis )
		self.calib_butt3.Bind( wx.EVT_BUTTON, self.joystick_calibration_command_axis )
		self.calib_butt4.Bind( wx.EVT_BUTTON, self.joystick_calibration_command_axis )
		self.m_button34.Bind( wx.EVT_BUTTON, self.ok_command )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def joystick_calibration_command_axis( self, event ):
		event.Skip()
	
	
	
	
	def ok_command( self, event ):
		event.Skip()
	

