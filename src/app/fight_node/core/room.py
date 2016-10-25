#coding:utf8
from gtwisted.core import reactor
import gevent
import itertools, time
from player import Player
from gtwisted.utils import log
from gevent.lock import Semaphore
from gevent.queue import Queue

import random

#import pb
from app.pb import Fighting_pb2
from app.pb import FightBefore_pb2

class Room(object):
    """
    战斗房间/房间逻辑都在这里
    """
    def __init__(self, roomId, cc=2):
        """
        :param roomId: 房间号
        :param cc: 房间人数上限
        :return:
        """
        self.playerNumGen = itertools.count(1, 1)
        self.roomId = roomId
        self.propertyBag = {}#保存房间属性
        self.cc = cc
        self.players = {}
        self.isPush = False
        self.tick = None
        self.roomLock = Semaphore()
        #step queue
        self.seed = random.randint(0, 1000)
        self.stepQueueLock = Semaphore()
        self.stepQueue = Queue()
        self.stepnum = -1
        self.room_state = 0 #0 waiting 1 runing 2 end
        #返回给客户端的per step message
        self.cuiMsg = Fighting_pb2.CollectUsersInput()
        #step 补偿
        self.mSendTime = None
        self.frameSpeed = 30#每秒30次同步
        self.frameTickLength = long(1.0/self.frameSpeed*10000000)

    @property
    def full(self):
        if self.playerCount < self.cc:
            return False
        else:
            return True

    def getStateNState(self, n):
        if len([p for p in self.players.values() if p.playerState == n]) == self.cc:
            return True
        else:
            return False

    @property
    def hasPlayer(self):
        if self.playerCount > 0:
            return True
        else:
            return False

    @property
    def offLineCount(self):
        """
        当前房间掉线玩家数量
        :return:
        """
        return len([p for p in self.players.values() if p.sid is None])

    @property
    def playerCount(self):
        """
        当前房间玩家数量
        :return:
        """
        return len(self.players)

    @property
    def isAllReady(self):
        """
        是否可以开始游戏
        :return:
        """
        if self.full and self.getStateNState(3):
            return True
        else:
            return False

    def getRid(self, uid):
        """

        :param uid:
        :return:
        """
        p = self.players.get(uid, None)
        if p:
            return p.rid
        else:
            return None

    def getPlayer(self, uid):
        """
        获取玩家
        :param uid:
        :return:
        """
        return self.players.get(uid, None)

    def sendReady(self):
        """
        房间满发送ready消息
        :return:
        """
        self.broadcast(3, "")

    def joinRoom(self, conn):
        """
        加入房间/判断重新链接
        :param conn:
        :return:
        """
        uid = getattr(conn, "uid", None)
        if uid in self.players:
            #断线重连
            p = self.players[uid]
            p.reConnection(conn)
            log.msg("reconnectioned ======== %s" % uid)
        else:
            if self.playerCount < self.cc:
                p = Player(conn, self.playerNumGen.next())
                self.players[uid] = p
                #test发送PlayerJionMsg, InitRoomMsg
                playerInitRoomMsg = FightBefore_pb2.InitRoomMsg()
                playerInitRoomMsg.seed = self.seed
                playerInitRoomMsg.localID = p.rid
                playerInitRoomMsg.maxPlayer = self.cc
                self.sendMsg(uid, 5, playerInitRoomMsg)

                playerJoinMsg = FightBefore_pb2.PlayerJionMsg()
                playerJoinMsg.playerLocalID = p.rid
                self.multicast(6, playerJoinMsg, excludes=[uid])

                for i in self.players.values():
                    playerJoinMsg = FightBefore_pb2.PlayerJionMsg()
                    playerJoinMsg.playerLocalID = i.rid
                    self.sendMsg(uid, 6, playerJoinMsg)
            else:
                raise Exception('player cc limit!!!')
        # if self.full:
        #     #人满了, 开启steploop
        #     self.sendReady()
        #     self.loopPush()

    def leaveRoom(self, uid):
        """
        离开房间
        :param uid:
        :return:
        """
        if uid in self.players:
            del self.players[uid]
            log.msg("%s leaveRoom" % self.roomId)

    def addRoomProperty(self, k, v):
        """
        添加房间属性
        :param k:
        :param v:
        :return:
        """
        self.propertyBag[k] = v

    def removeRoomProperty(self, k):
        """
        移除房间属性
        :param k:
        :return:
        """
        del self.propertyBag[k]

    def getRoomProperty(self, k):
        """
        获取房间属性
        :param k:
        :return:
        """
        return self.propertyBag.get(k, None)

    def addPlayerProperty(self, k, v, uid):
        """
        添加玩家属性
        :param k:
        :param v:
        :param uid:
        :return:
        """
        p = self.players.get(uid, None)
        if p:
            p.addProperty(k, v)


    def removePlayerProperty(self, k, uid):
        """
        移除玩家属性
        :param k:
        :return:
        """
        p = self.players.get(uid, None)
        if p:
            p.removeProperty(k)

    def getPlayerProperty(self, k, uid):
        """
        获取玩家属性
        :param k:
        :return:
        """
        p = self.players.get(uid, None)
        if p:
            return p.getProperty(k)

    def multicast(self, command, data=None, excludes=None):
        """
        房间内组播消息
        :param excludes: 排除的ID
        :param data: 数据
        :return:
        """
        for p in (self.players.values() if excludes is None else
                  [i for i in self.players.values() if i.uid not in excludes]):
            p.sendMsg(command, data)

    def broadcast(self, command, data=None):
        """
        房间内广播消息
        :param data: 数据
        :return:
        """
        for p in self.players.values():
            p.sendMsg(command, data)

    def sendMsg(self, uid, command, data):
        """
        向指定用户发送消息
        :param uid:
        :param command:
        :param data:
        :return:
        """
        user = self.players.get(uid, None)
        if user:
            user.sendMsg(command, data)

    def stopLoopPush(self):
        """
        停止定时器
        :return:
        """
        if self.tick:
            self.tick.cancel()
            self.tick = None
            log.msg("canceled loopPush of room %s" % self.roomId)

    def loopPush(self):
        if not self.isPush:
            log.msg('start loopPush!!!!')
            #发送ready的消息
            self.sendReady()
            self.mSendTime = long(time.time() * 10000000) + 20 * 10000
            self.isPush = True#每个房间只启动一个定时器
            self._loopPush()

    # def _loopPush(self):
    #     """
    #     数据同步loop
    #     :return:
    #     """
    #     # log.msg("roomid %s. time: %s" % (self.roomId, time.time()))
    #     if self.playerCount > self.offLineCount:
    #         self.stepLoop()
    #         self.tick = reactor.callLater(0.02, self._loopPush)
    #     else:#没有玩家后需要清除定时器
    #         self.stopLoopPush()

    def _loopPush(self):
        """
        数据同步loop
        :return:
        """
        while 1:
            if self.playerCount > self.offLineCount:
                self.stepLoop()
                gevent.sleep(0.002)
            else:#没有玩家后需要清除定时器
                self.stopLoopPush()
                break

    def doLostConnection(self, uid):
        """
        用户掉线处理（支持断线重连）
        :param uid:
        :return:
        """
        p = self.players.get(uid, None)
        if p:
            log.msg("room doLostConnection %s" % uid)
            p.lostConnection()
            log.msg("%s====%s" % (self.playerCount, self.offLineCount))

            if self.playerCount == self.offLineCount:
                #所有玩家都掉线了, 玩个屁啊, 直接删除房间得了
                return True
            else:
                return False
        else:
            return False

    def delRoomHandle(self):
        """
        删除房间前回收房间用过的资源
        :return:
        """
        self.stopLoopPush()

    def addUserInput(self, local_id, data):
        """
        添加用户输入
        :param data:
        :return:
        """
        self.stepQueue.put_nowait([local_id, data])

    def clearCuiMsg(self):
        """
        清空消息内容
        :return:
        """
        self.cuiMsg.Clear()


    # def stepLoop(self):
    #     """
    #     loop
    #     :return:
    #     """
    #     step_data = self.prepareStepData()
    #     self.clearCuiMsg()
    #     if step_data:
    #         #有数据才发送
    #         self.stepnum += 1
    #         cuiMsg = Fighting_pb2.CollectUsersInput()
    #         cuiMsg.step = self.stepnum
    #         for i in step_data:
    #             userInputData = cuiMsg.usersInputData.add()
    #             userInputData.ID = i[0]
    #             userInputData.data = i[1]
    #
    #         self.broadcast(11, cuiMsg)
    #         # log.msg(time.time())
    #         # log.msg("step data:")
    #         # log.msg(step_data)
    #     else:
    #         c_count = (long(time.time()*10000000) - self.mSendTime)/self.frameTickLength
    #
    #         cuiMsg = Fighting_pb2.CollectUsersInput()
    #         while c_count > self.stepnum:
    #             self.stepnum += 1
    #             cuiMsg.step = self.stepnum
    #             self.broadcast(11, cuiMsg)

    # from app.common.decorators import myProfile
    # @myProfile()
    # from app.common.decorators import myTimeit
    # @myTimeit()
    def stepLoop(self):
        """
        loop
        :return:
        """
        step_data = self.prepareStepData()
        self.clearCuiMsg()
        if step_data:
            #有数据才发送
            self.stepnum += 1
            self.cuiMsg.step = self.stepnum
            for i in step_data:
                userInputData = self.cuiMsg.usersInputData.add()
                userInputData.ID = i[0]
                userInputData.data = i[1]

            self.broadcast(11, self.cuiMsg)
        else:
            c_count = (long(time.time()*10000000) - self.mSendTime)/self.frameTickLength
            while c_count > self.stepnum:
                self.stepnum += 1
                self.cuiMsg.step = self.stepnum
                self.broadcast(11, self.cuiMsg)


    def prepareStepData(self):
        """
        准备step数据
        :return:
        """
        return [self.stepQueue.get() for _ in range(self.stepQueue.qsize())]
