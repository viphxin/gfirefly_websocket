#coding:utf8
"""
供root调用的api写在这里
"""
from app.common.decorators import myRemoteserviceHandle
from gfirefly.server.globalobject import GlobalObject
import player_api

@myRemoteserviceHandle("gate")
def gameMsgRouter(data):
    """
    game节点消息路由
    :param data: 请求数据
    :return:
    """
    print 'game received: %s' % data
    GlobalObject().gamecommandservice.callTarget(data['m'], data)
