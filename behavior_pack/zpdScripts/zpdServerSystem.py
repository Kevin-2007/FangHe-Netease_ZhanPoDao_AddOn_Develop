import mod.server.extraServerApi as serverApi
from zpdScripts.modConfig import *
from zpdScripts.RPC import RPCServerToClient
import uuid 

ServerSystem = serverApi.GetServerSystemCls()
CompFactory = serverApi.GetEngineCompFactory()

class zpdServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(namespace, systemName)
        self.ListenEvent()
    
    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.OnPlayerJoin)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnCarriedNewItemChangedServerEvent", self, self.OnChangeItem)
    
    def OnChangeItem(self, args):

        def eventdef(w):
            print("Server回调"+w)

        playerId = args["playerId"]
        newItemDict = args["newItemDict"]
        if newItemDict != None:
            itemName = newItemDict["newItemName"]

            if itemName in zpdName:
                self.Client(playerId).ShowZpdItemPanel("ShowZpdItemPanel", back=eventdef)

    def OnPlayerJoin(self, args):
        playerId = args["id"]

    def Destroy(self):
        self.UnListenAllEvents()
    

    
        # 初始化
    def RPCInit(self):
        self.CallBackCache = {}  #缓存回调
        self.ListenForEvent(ModName, ClientSystemName, "ClientToServer", self, self.FromClient)
        self.Client = RPCServerToClient(self.GoClient)

    # 给服务端发送事件
    def GoClient(self, playerId, EventName, *args, **kwargs):
        value = {}
        if kwargs.get("back"):
            uid = uuid.uuid1().hex
            backfun = kwargs["back"]
            self.CallBackCache[uid] = backfun
            value = {
                "serverBack": {
                    "backuid": uid
                }
            }
        # 广播到服务端
        self.NotifyToClient(playerId, "ServerToClient", (EventName, args, value))
        
    # 接收服务端事件
    def FromClient(self, Data):
        name, args, value = Data
        fun = None
        if value.get("serverBack"):
            uid = value["serverBack"]["backuid"]
            fun = self.CallBackCache.pop(uid)  # 是回调 从回调列表取
        else:
            try:
                fun = getattr(self, name)
            except:
                print ("服务端未找到事件: %s"%name)
        if fun:
            backargs = fun(*args) if isinstance(args, (list, tuple)) else fun(args)
            # 若服务端需要回调，则发送事件
            if value.get("clientBack"):
                playerId = value["clientBack"]["playerId"]
                self.NotifyToClient(playerId, "ServerToClient", ("", backargs, value))
