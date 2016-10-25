#encoding:utf8
from app.common.server_loop import LoopFactory

import clear_deadconn
import gamestatistic

loop_factory = LoopFactory()
#add 定时清除死链接
loop_factory.add(clear_deadconn.ClearDeadConn(60, name="clear_deadconn"))
#战斗服务器统计信息
loop_factory.add(gamestatistic.GameStatistic(60, name="gamestatistic"))

#test
# from gtwisted.core import reactor
# reactor.run()