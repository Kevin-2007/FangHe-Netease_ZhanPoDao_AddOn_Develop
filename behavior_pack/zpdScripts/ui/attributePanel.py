# -*- coding=utf-8 -*-

from behavior_pack.zpdScripts.utils.calculate import levelToLyMax
import zpdScripts.modConfig as modConfig
import mod.client.extraClientApi as clientApi
from zpdScripts.uiPathMgr import *
from zpdScripts.utils import *

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
CF = clientApi.GetEngineCompFactory()

class attributePanel(ScreenNode):
    def __init__(self, namespace, name, param):
        super(attributePanel, self).__init__(namespace, name, param)
        
        self.attributePath = PanelPath.AttributePanel
        self.attrPresetPath = PresetPath.attribute

    def UpdateData(self, **kwargs):
        self.ly = kwargs["ly"]
        self.level = kwargs["level"]
        

    def Create(self):
        pass

    def Update(self):
        self.GetBaseUIControl(self.attributePath.testData+self.attrPresetPath.progress_bar).asProgressBar().SetValue(float(self.ly)/levelToLyMax(self.level))
        self.GetBaseUIControl(self.attributePath.testData+self.attrPresetPath.text).asLabel().SetText("{} / {}".format(float(self.ly),levelToLyMax(self.level)))

    def Destroy(self):
        pass