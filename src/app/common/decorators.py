#coding:utf8
from gfirefly.server.globalobject import GlobalObject
from gtwisted.utils import log

def wsServiceHandle(target):
    """供h5客户端连接调用的接口描述符
    """
    GlobalObject().wsapp.service.mapTarget(target)

class myRemoteserviceHandle:
    """作为remote节点，供某个root节点调用的接口描述符
    """
    def __init__(self, remotename):
        """
        """
        self.remotename = remotename

    def __call__(self,target):
        """
        """
        for key in GlobalObject().remote.keys():
            if self.remotename in key:
                GlobalObject().remote[key]._reference._service.mapTarget(target)

def gameServiceHandle(target):
    """
    game节点服务器通道(自定义的哦)
    """
    GlobalObject().gamecommandservice.mapTarget(target)

class myProfile:
    """
    性能分析
    from app.common.decorators import myProfile
    @myProfile()
    """
    def __init__(self):
        """
        """
        pass

    def __call__(self, func):
        """
        """
        def d_f(*args, **kwargs):
            import cProfile, StringIO, pstats
            # datafn = func.__name__ + ".profile" # Name the data file
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            #prof.dump_stats(datafn)
            s = StringIO.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(prof, stream=s).sort_stats(sortby)
            ps.print_stats()
            log.msg(s.getvalue())
            return retval
        return d_f

class myTimeit:
    """
    性能分析
    from app.common.decorators import myTimeit
    @myTimeit()
    """
    def __init__(self):
        """
        """
        pass

    def __call__(self, func):
        """
        """
        def d_f(*args, **kwargs):
            import time
            st = time.clock()
            retval = func(*args, **kwargs)
            log.msg("Totol time: %8.6f" % (time.clock() - st, ))
            return retval
        return d_f