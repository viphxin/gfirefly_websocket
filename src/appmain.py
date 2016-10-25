#coding:utf8
from gevent import monkey
monkey.patch_all()
#日志系统支持日志级别---start
import logging, sys
from twisted.python import log
from twisted.logger import globalLogBeginner

class LevelFileLogObserver(log.FileLogObserver):
    def __init__(self, f, level=logging.INFO):
        log.FileLogObserver.__init__(self, f)
        self.logLevel = level

    def emit(self, eventDict):
        if eventDict['isError']:
            level = logging.ERROR
        elif 'level' in eventDict:
            level = eventDict['level']
        else:
            level = logging.INFO
        if level >= self.logLevel:
            log.FileLogObserver.emit(self, eventDict)

#!!!!!上线把日志级别改成error
logger = LevelFileLogObserver(sys.stderr, logging.ERROR)
globalLogBeginner.beginLoggingTo([logger.emit])
#日志系统支持日志级别---start#日志系统支持日志级别---end

# from gevent import monkey; monkey.patch_os()
import json,sys, os
# from gfirefly.server.server import FFServer
#换成支持websocket的FFServer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from websocket_hacker.fgserver import FFServer
from gfirefly.server.logobj import log


if __name__ == "__main__":
    #这里可以捕获全局异常!!!!!
    def excepthook(type, value, trace):
        '''''write the unhandle exception to log'''
        log.err('Unhandled Error: %s: %s'%(str(type), str(value)))
        sys.__excepthook__(type, value, trace)
    sys.excepthook = excepthook
    args = sys.argv
    try:#设置进程名字
        from setproctitle import setproctitle, getproctitle
        setproctitle("gfirefly: %s" % args[1])
    except Exception, e:
        log.err(e)

    servername = None
    config = None
    if len(args)>2:
        servername = args[1]
        config = json.load(open(args[2],'r'))
    else:
        raise ValueError
    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers',{})
    masterconf = config.get('master',{})
    serconfig = sersconf.get(servername)
    ser = FFServer()
    ser.config(serconfig, servername=servername, dbconfig=dbconf, memconfig=memconf, masterconf=masterconf)
    ser.start()
    
    