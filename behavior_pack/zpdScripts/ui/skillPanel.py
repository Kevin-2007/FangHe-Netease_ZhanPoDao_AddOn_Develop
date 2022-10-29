# -*- coding=utf-8 -*-

from zpdScripts.modConfig import *
import mod.client.extraClientApi as clientApi
from zpdScripts.uiPathMgr import *


ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
CF = clientApi.GetEngineCompFactory()

class skillPanel(ScreenNode):
    def __init__(self, namespace, name, param):
        super(skillPanel, self).__init__(namespace, name, param)
        
        self.skillPath = PanelPath.SkillPanel
        self.skillPresetPath = PresetPath.skill

    def Create(self):
        pass

    def Update(self):
        pass

    def Destroy(self):
        pass