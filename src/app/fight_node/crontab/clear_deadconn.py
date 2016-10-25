#encoding:utf8
from app.common.base_task import BaseTask
import datetime, time
from gfirefly.server.logobj import log
from gfirefly.server.globalobject import GlobalObject

class ClearDeadConn(BaseTask):
    """
    清除死链接
    """
    # def __init__(self, *args, **kwargs):
    #     super(ClearDeadConn, self).__init__(*args, **kwargs)

    def task(self):
        """
        任务
        :param kwargs:
        :return:
        """
        log.msg(datetime.datetime.now())
        log.msg('do task. %s' % self.kwargs['name'])
        try:
            n = time.time()
            for conn in GlobalObject().netfactory.connmanager._connections.values():
                log.msg("uid: %s. ctime:%s. room_id: %s." % (getattr(conn.instance,'uid',None),
                                                             getattr(conn.instance, "ctime", None),
                                                             getattr(conn.instance,'room_id',None)))

                if (getattr(conn.instance,'uid',None) is None or getattr(conn.instance,'room_id', None) is None) and\
                    getattr(conn.instance, "ctime", None) is not None:
                    if (n - conn.instance.ctime) > 30:
                        GlobalObject().netfactory.loseConnection(conn.id)
                        log.msg("%s dead conn %s delete" % (GlobalObject().json_config['name'], conn.id))
        except BaseException, e:
            log.err("=======================fight dead conn error")
            log.err("%s" % e)
