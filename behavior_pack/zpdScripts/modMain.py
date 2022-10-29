# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import zpdScripts.modConfig as modConfig


@Mod.Binding(name=modConfig.ModName, version=modConfig.ModVersion)
class zpdMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def zpdModServerInit(self):
        serverApi.RegisterSystem(modConfig.ModName, modConfig.ServerSystemName, modConfig.ServerSystemClsPath)

    @Mod.DestroyServer()
    def zpdModServerDestroy(self):
        pass

    @Mod.InitClient()
    def zpdModClientInit(self):
        clientApi.RegisterSystem(modConfig.ModName, modConfig.ClientSystemName, modConfig.ClientSystemClsPath)

    @Mod.DestroyClient()
    def zpdModClientDestroy(self):
        pass
