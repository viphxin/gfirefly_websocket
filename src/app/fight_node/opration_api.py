#coding=utf-8
"""
这里实现所有战斗服务器的自定义操作
"""
from gfirefly.server.globalobject import netserviceHandle
from app.fight_node.core.roommanager import RoomManager
from gtwisted.utils import log
from gfirefly.server.globalobject import GlobalObject

#import pb
from app.pb import Oauth_pb2
from app.pb import Common_pb2
from app.pb import Fighting_pb2

@netserviceHandle
def msg_0(_conn, data):
    """
    ping
    :param _conn: 链接对象
    :param data: 客户端数据包
    :return:
    """
    _conn.safeToWriteData("", 0)

@netserviceHandle
def msg_1(_conn, data):
    """
    用户登陆
    :param _conn: 链接对象
    :param data: 客户端数据包
    :return:
    """
    #数据解析
    msg = Oauth_pb2.UserLogin()
    msg.ParseFromString(data)
    #检测tocken有效性
    # TODO
    userId = msg.userId
    tocken = msg.accesstocken
    log.msg(userId)
    log.msg(tocken)
    log.msg("client IP:%s Port: %s." % _conn.transport.getAddress())
    #重复登陆
    if userId:
        setattr(_conn, 'uid', userId)
        resp = Common_pb2.CommonResponse()
        resp.state = True
        # GlobalObject().netfactory.pushObject(1, resp, [_conn.transport.sessionno])
        _conn.safeToWriteData(resp, 1)
    else:
        #掉线
        GlobalObject().netfactory.loseConnection(_conn.transport.sessionno)

@netserviceHandle
def msg_2(_conn, data):
    """
    NewPlayerMsg
    :param _conn: 链接对象
    :param data: 客户端数据包
    :return:
    """
    uid = getattr(_conn, "uid", None)
    #分配房间
    room_id = RoomManager().joinRandomRoom(_conn, 2)
    if room_id:
        setattr(_conn, 'room_id', room_id)
        room = RoomManager().getRoom(room_id)
        if room:
            player = room.getPlayer(uid)
            if player:
                player.setState(1)
                resp = Common_pb2.CommonResponse()
                resp.state = True
                # GlobalObject().netfactory.pushObject(2, resp, [_conn.transport.sessionno])
                _conn.safeToWriteData(resp, 2)
    else:
        log.err("add room error!!!")
        return

@netserviceHandle
def msg_4(_conn, data):
    """
    资源加载完成
    :param _conn: 链接对象
    :param data: 客户端数据包
    :return:
    """
    uid = getattr(_conn, "uid", None)
    room_id = getattr(_conn, 'room_id', None)
    if room_id:
        room = RoomManager().getRoom(room_id)
        if room:
            p = room.getPlayer(uid)
            if p:
                p.setState(3)
                resp = Common_pb2.CommonResponse()
                resp.state = True
                _conn.safeToWriteData(resp, 4)
                #检测是否所有客户端资源加载完成
                if room.isAllReady:
                    room.loopPush()

@netserviceHandle
def msg_10(_conn, data):
    """
    UserInputMsg
    :param _conn: 链接对象
    :param data: 客户端数据包
    :return:
    """
    #数据解析
    msg = Fighting_pb2.UserInput()
    msg.ParseFromString(data)

    #add to step queue
    room_id = getattr(_conn, "room_id", None)
    uid = getattr(_conn, "uid", None)
    # import time
    # log.msg(time.time())
    # log.msg('user_input: ')
    # log.msg(msg.data)
    room = RoomManager().getRoom(room_id)
    if room:
        local_id = room.getRid(uid)
        if local_id:
            room.addUserInput(local_id, msg.data)

# @netserviceHandle
# def msg_20(_conn, data):
#     """
#     test
#     :param _conn: 链接对象
#     :param data: 客户端数据包
#     :return:
#     """
#     cuiMsg = Fighting_pb2.CollectUsersInput()
#     cuiMsg.step = 100
#     for i in range(1024):
#         userInputData = cuiMsg.usersInputData.add()
#         userInputData.ID = 1
#         userInputData.data = 1
#     log.msg("20 send done!!!")
#     _conn.safeToWriteData(cuiMsg, 20)