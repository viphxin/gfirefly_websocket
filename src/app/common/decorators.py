#coding:utf8
from gfirefly.server.globalobject import GlobalObject

def wsServiceHandle(target):
    """供h5客户端连接调用的接口描述符
    """
    GlobalObject().wsapp.service.mapTarget(target)

class myRemoteserviceHandle:
    """作为remote节点，供某个root节点调用的接口描述符
    """
    def __init__(self, remotename):
        """
        """
        self.remotename = remotename

    def __call__(self,target):
        """
        """
        for key in GlobalObject().remote.keys():
            if self.remotename in key:
                GlobalObject().remote[key]._reference._service.mapTarget(target)

def gameServiceHandle(target):
    """
    game节点服务器通道(自定义的哦)
    """
    GlobalObject().gamecommandservice.mapTarget(target)