#coding=utf-8
import time
from gfirefly.server.logobj import log
from gfirefly.server.globalobject import GlobalObject
from simpleProtoc import SimpleProtoc
from app.fight_node.core.roommanager import RoomManager
from app.common.utils import getcurrentconn

#修改数据协议
#自定义的简单协议头部会少9个字节（只保留command(4字节)和length(4字节)字段）
dataprotocl = SimpleProtoc()
GlobalObject().netfactory.setDataProtocl(dataprotocl)
#end--修改数据协议
import opration_api

#定时任务
from app.fight_node import crontab

def doConnectionMade(conn):
    '''当连接建立时调用的方法'''
    #有一个判断当前是否该断开连接的方法
    #设置链接开始时间
    setattr(conn, "ctime", time.time())

def doConnectionLost(conn):
    '''当连接断开时调用的方法'''
    #掉线需要看房间里是否还有其他人，没有其他人则需要删除房间
    uid = getattr(conn, 'uid', None)
    room_id = getattr(conn, "room_id", None)
    if uid:
        #玩家在房间内才处理
        room = RoomManager().getRoom(room_id)
        log.msg("user %s lostconnection" % uid)
        if room.doLostConnection(uid):
            log.msg("delete room. reason: room empty!!!")
            RoomManager().leaveRoom(room_id, uid)


GlobalObject().netfactory.doConnectionMade = doConnectionMade#将自定义的登陆后执行的方法绑定到框架
GlobalObject().netfactory.doConnectionLost = doConnectionLost#将自定义的下线后执行的方法绑定到框架


log.msg("fighting api: %s" % GlobalObject().netfactory.service._targets.keys())