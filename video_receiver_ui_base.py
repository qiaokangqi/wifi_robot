# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class video
###########################################################################

class video ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.video_sizer = wx.BoxSizer( wx.VERTICAL )
        '''
        self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.video_sizer.Add( self.m_bitmap2, 0, wx.ALL, 5 )
        '''

        self.SetSizer( self.video_sizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass

