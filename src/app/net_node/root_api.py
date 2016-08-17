#coding:utf8
"""
供root调用的api写在这里
"""
import time
from app.common.decorators import myRemoteserviceHandle
from gfirefly.server.globalobject import GlobalObject

@myRemoteserviceHandle("gate")
def pushMsg(data, sessionno):
    """
    给客户端推送消息
    :param session:
    :param data:
    :return:
    """
    client = GlobalObject().wsapp.getClientBySessionno(int(sessionno))
    if client:
        client.sendData(data)