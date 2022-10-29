import mod.client.extraClientApi as clientApi
import zpdScripts.modConfig as modConfig
from zpdScripts.modConfig import *
import uuid
from zpdScripts.RPC import RPC

PID = clientApi.GetLocalPlayerId()
ClientSystem = clientApi.GetClientSystemCls()
CompFactory = clientApi.GetEngineCompFactory()

class zpdClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        super(ClientSystem, self).__init__(namespace, systemName)
        self.ListenEvent()
        self.LoadClientData()

    def LoadClientData(self):
        localConfig = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId()).GetConfigData("fhs_zpd_data")
        if not (localConfig == {}):
            self.ly = localConfig["ly"]
            self.level = localConfig["level"]
        else:
            self.ly = 100
            self.level = 1
    
    def ListenEvent(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.OnUiInit)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", self, self.OnTick)

    def Destroy(self):
        self.UnListenAllEvents()

    def OnUiInit(self):
        clientApi.RegisterUI(ModName, "skillPanel", "zpdScripts.ui.skillPanel.skillPanel", "skillPanel.main")
        clientApi.RegisterUI(ModName, "attributePanel", "zpdScripts.ui.attributePanel.attributePanel", "attributePanel.main")

        clientApi.CreateUI(ModName, "attributePanel", {"isHud": 1})

    def OnTick(self):
        
        uiNode = clientApi.GetUI(ModName, "attributePanel")

        uiNode.UpdateData(ly=self.ly, level=self.level)


    def OnShowZpdItemPanel(self, args):

        uiNode = clientApi.CreateUI(ModName, "skillPanel")

        # 初始化
    def RPCInit(self):
        self.CallBackCache = {}  #缓存回调
        self.ListenForEvent(ModName, ServerSystemName, "ServerToClient", self, self.FromServer)
        self.Server = RPC(self.GoServer)

    # 给服务端发送事件
    def GoServer(self, EventName, *args, **kwargs):
        value = {}
        if kwargs.get("back"):
            uid = uuid.uuid1().hex
            backfun = kwargs["back"]
            self.CallBackCache[uid] = backfun
            value = {
                "clientBack": {
                    "backuid": uid,
                    "playerId": PID
                }
            }
        # 广播到服务端
        self.NotifyToServer("ClientToServer", (EventName, args, value))
        
    # 接收服务端事件
    def FromServer(self, Data):
        name, args, value = Data
        fun = None
        if value.get("clientBack"):
            uid = value["clientBack"]["backuid"]
            fun = self.CallBackCache.pop(uid)  # 是回调 从回调列表取
        else:
            try:
                fun = getattr(self, name)
            except:
                print ("客户端未找到事件: %s"%name)
        if fun:
            backargs = fun(*args) if isinstance(args, (list, tuple)) else fun(args)
            # 若服务端需要回调，则发送事件
            if value.get("serverBack"):
                self.NotifyToServer("ClientToServer", ("", backargs, value))
