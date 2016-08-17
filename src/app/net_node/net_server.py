#coding:utf8
from gfirefly.server.globalobject import GlobalObject
from gfirefly.server.logobj import log

#导入逻辑接口
import common_api
import root_api

def doConnectionMade(conn):
    '''当连接建立时调用的方法'''
    print 'do some thing. 1111111'

def doConnectionLost(conn):
    '''当连接断开时调用的方法'''
    print 'do some thing. 2222222'


GlobalObject().wsapp.doConnectionMade = doConnectionMade#将自定义的登陆后执行的方法绑定到框架
GlobalObject().wsapp.doConnectionLost = doConnectionLost#将自定义的下线后执行的方法绑定到框架

log.msg("net_node api: %s" % GlobalObject().wsapp.service._targets.keys())