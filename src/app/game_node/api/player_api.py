#coding:utf8
import time
from app.common.decorators import gameServiceHandle
from gfirefly.server.globalobject import GlobalObject
from app.game_node.core.playermanager import PlayerManager
from app.game_node.core.player import Player

@gameServiceHandle
def handle_1(data):
    """
    用户/玩家登陆game node
    :param data:
    :return:
    """
    player = Player(data['pid'], data['sid'])
    PlayerManager().addPlayer(player)
    player.sendMsg({'m': 1, 's': 1})

@gameServiceHandle
def handle_2(data):
    """
    用户/玩家离线处理(断线重连预处理)
    :param data:
    :return:
    """
    player = PlayerManager().getPlayerByID(data['pid'])
    player.sendMsg({'m': 2, 's': 1})

