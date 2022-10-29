# -*- coding: utf-8 -*-

# 返回一个可以直接调用的远程函数
class RPC(object):
    def __init__(self, broadFun):
        self.attr_name = None
        self.broadFun = broadFun

    def __getattr__(self, attr_name, *args):
        self.attr_name = attr_name
        return self.rpc

    def rpc(self, *args, **value):
        self.broadFun(self.attr_name, *args, **value)

class RPCHasPlayerId(object):
    def __init__(self, broadFun, playerId):
        self.broadFun = broadFun
        self.playerId = playerId
        self.attr_name = None

    def __getattr__(self, attr_name, *args):
        self.attr_name = attr_name
        return self.rpc

    def rpc(self, *args, **value):
        self.broadFun(self.playerId, self.attr_name, *args, **value)

def RPCServerToClient(broadFun):
    def rpc(playerId):
        return RPCHasPlayerId(broadFun, playerId)
    return rpc
