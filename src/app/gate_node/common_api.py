#coding:utf8
import time
from gamenode_router import GameNodeRouter, GameNodeRouterException
from gfirefly.server.globalobject import GlobalObject, rootserviceHandle
from gfirefly.server.logobj import log

@rootserviceHandle
def allocGameNode(data):
    """
    用户登陆成功后分配一个game node服务节点
    :param userId:
    :return:
    """
    #用户ID做key
    try:
        gamenode = GameNodeRouter().get_node(data['pid'])
        if gamenode:
            log.msg("allocGameNode successful. node: %s" % gamenode.getName())
            gamenode.callbackChildNotForResult("gameMsgRouter", data)
        else:
            log.err("can't find gamenode. data: %s" % data)
    except GameNodeRouterException:
        log.err("GameNodeRouterException no gamenode to use. data: %s" % data)

@rootserviceHandle
def forwarding(data):
    """
    转发数据到对应节点
    :param data:
    :return:
    """
    #用户ID做key
    try:
        gamenode = GameNodeRouter().get_node(data['pid'])
        if gamenode:
            log.msg("forwarding data. node: %s" % gamenode.getName())
            gamenode.callbackChildNotForResult("gameMsgRouter", data)
        else:
            log.err("can't find gamenode. data: %s" % data)
    except GameNodeRouterException:
        log.err("GameNodeRouterException no gamenode to use. data: %s" % data)

@rootserviceHandle
def sendMsg(data, sessionnos):
    """
    发送消息到net
    :param sessionno:
    :return:
    """
    for sessionno in sessionnos:
        net, session = sessionno.split("_")
        GlobalObject().root.callChildNotForResult(net, "pushMsg", data, session)
