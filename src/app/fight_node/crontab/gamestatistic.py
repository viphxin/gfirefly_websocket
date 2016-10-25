#encoding:utf8
from app.common.base_task import BaseTask
import datetime, time
from gfirefly.server.logobj import log
from gfirefly.server.globalobject import GlobalObject
from app.fight_node.core.roommanager import RoomManager

class GameStatistic(BaseTask):
    """
    游戏运行时统计信息
    """
    def task(self):
        """
        任务
        :param kwargs:
        :return:
        """
        log.err(datetime.datetime.now())
        log.err("current room count: %s." % RoomManager().count)

