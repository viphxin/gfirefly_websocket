#encoding:utf8
import datetime, time
from gtwisted.core import reactor

class LoopFactory(object):
    """
    定时任务管理类
    """
    def __init__(self, *tasks):
        for task in tasks:
            self.run(task)
        # task1 = clear_deadconn.ClearDeadConn(5, name="task_1")
        # self.run(task1)
        # task2 = clear_deadconn.ClearDeadConn(5, name="task_2")
        # self.run(task2)
        # task1 = clear_deadconn.ClearDeadConn("10:32:00", isloop=False, name="task_1")
        # self.run(task1)

    def add(self, task):
        """
        添加定时任务
        :param task:
        :return:
        """
        self.run(task)

    def getLater(self, everytime="00:00:01"):
        """
        得到call later的时间
        :param everytime:
        :return:
        """
        now = datetime.datetime.now()
        torrow = now + datetime.timedelta(days=1)
        runtime = "%s %s" % (torrow.strftime("%Y-%m-%d"), everytime)
        runtime = datetime.datetime.strptime(runtime, "%Y-%m-%d %H:%M:%S")
        # end--得到运行的时间
        # 算出延迟多久执行
        now = time.mktime(now.timetuple())
        runtime = time.mktime(runtime.timetuple())
        later = runtime - now
        # end--算出延迟多久执行
        later = 5
        return later

    def looptask(self, current_task):
        """
        loop 化任务
        :param current_task:
        :return:
        """
        current_task.task()
        if current_task.isloop:
            reactor.callLater(current_task.t, self.looptask, current_task)
        else:
            reactor.callLater(self.getLater(everytime=current_task.t), self.looptask, current_task)

    def run(self, current_task):
        """
        入口
        :return:
        """
        if current_task.isloop:
            current_task.task()
            if type(current_task.t) not in [int, float]:
                raise Exception("invalid loop task time. %s" % current_task.t)
            reactor.callLater(current_task.t, self.looptask, current_task)
        else:
            #定时任务
            if current_task.isstartcall:
                #服务器开启时执行一次
                current_task.task()
            if type(current_task.t) != str:
                raise Exception("invalid cron task time. %s" % current_task.t)
            reactor.callLater(self.getLater(everytime=current_task.t), self.looptask, current_task)

if __name__ == "__main__":
    from app.fight_node.crontab import clear_deadconn
    t = clear_deadconn.ClearDeadConn(5, name="task_1")
    a = LoopFactory()
    a.add(t)
    reactor.run()