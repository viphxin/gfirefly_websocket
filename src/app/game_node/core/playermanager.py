#coding:utf8
from gfirefly.utils.singleton import Singleton
from gfirefly.server.logobj import log


class PlayerManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._players = {}

    def addPlayer(self, player):
        """添加一个用户
        """
        if self._players.has_key(player.pid):
            log.msg("reconnectioned, pid: %s" % player.pid)
            self.getPlayerByID(player.pid).reconnection(player.sid)
            return
        log.msg("game add player %s" % player.sessionno)
        self._players[player.pid] = player

    def getAllPlayers(self):
        return self._players

    def getPlayerByID(self, pid):
        """根据ID获取用户信息
        """
        return self._players.get(pid, None)

    def getPlayerBySessionno(self, sessionno):
        '''根据客户端的动态ID获取user实例'''
        for player in self._players.values():
            if player.sessionno == sessionno:
                return player
        return None

    def dropPlayer(self, player):
        """处理用户下线
        """
        userId = player.pid
        try:
            #保存数据
            player.saveDataToDb()
            del self._players[userId]
            log.msg("removed player %s from PlayerManager" % userId)
        except Exception,e:
             log.err(e)

    def dropPlayerBySessionno(self, sessionno):
        player = self.getPlayerBySessionno(sessionno)
        if player:
            self.dropUser(player)

    def dropPlayerByID(self, userId):
        """根据用户ID处理用户下线
        """
        player = self.getPlayerByID(userId)
        if player:
            self.dropPlayer(player)