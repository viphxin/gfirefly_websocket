#coding:utf8

from gfirefly.utils.singleton import Singleton
from gevent.lock import Semaphore
from room import Room
from gfirefly.server.logobj import log

import itertools

class RoomManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.rooms = {}
        self.managerLock = Semaphore()#同步
        self.roomGen = itertools.count(1, 1)

    @property
    def count(self):
        """
        房间数
        :return:
        """
        return len(self.rooms)

    def joinRandomRoom(self, conn, cc):
        """
        加入随机房间
        :param conn:
        :return:
        """
        try:
            self.managerLock.acquire()
            can_rooms = [r for r in self.rooms.values() if not r.full]
            if can_rooms:
                room = can_rooms[0]
                room.joinRoom(conn)
            else:
                #create
                room = Room(self.roomGen.next(), cc)
                room.joinRoom(conn)
                self.rooms[room.roomId] = room
            return room.roomId
        except Exception, e:
            log.err(e)
            return None
        finally:
            self.managerLock.release()

    def joinOrCreateRoom(self, roomId, sid, uid, cc):
        """
        加入或创建房间
        :param roomId: 房间号
        :param sid: 客户端动态ID
        :param uid: 玩家ID
        :param cc: 房间人数上限
        :return:
        """
        try:
            self.managerLock.acquire()
            if roomId in self.rooms:
                #join
                room = self.rooms[roomId]
            else:
                #create
                room = Room(roomId, sid, uid, cc)

            room.joinRoom(sid, uid)
            self.rooms[roomId] = room
            return True
        except:
            return False
        finally:
            self.managerLock.release()

    def leaveRoom(self, roomId, uid):
        """
        :param roomId: 房间号
        :param uid: 用户ID
        :return:
        """
        room = self.rooms.get(roomId, None)
        if room:
            room.leaveRoom(uid)
            #如果房间内没有玩家了，需要删除房间
            if room.playerCount == room.offLineCount:
                #停止计时器
                room.stopLoopPush()
                del self.rooms[roomId]

    def getRoom(self, roomId):
        """
        获取房间
        :param roomId:
        :return:
        """
        return self.rooms.get(roomId, None)