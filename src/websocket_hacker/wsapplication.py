#coding=utf-8
import sys, os
# if 'threading' in sys.modules:
#     del sys.modules['threading']
import ujson as json
import itertools
import gevent
from gevent import Greenlet, queue

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from protc import CustProtc
from gfirefly.server.globalobject import GlobalObject
from gtwisted.utils import log

class MySender(Greenlet):
    """
    发送数据放在一个协程里面
    """
    def __init__(self,skt):
        """基础连接通道\n
        @param skt: socket socket实例，所有的Transport通信通过它来实现\n

        """
        Greenlet.__init__(self)
        self.inbox = queue.Queue()
        self.skt = skt

    def close(self):
        """关闭通道连接\n
        """
        try:
            self.skt.close()
        except:pass
        #销毁greenlet
        self.kill()

    def sendall(self, data):
        """发送消息\n
        """
        self.inbox.put(data)

    def _run(self):
        """启动write协程\n
        """
        while 1:
            message = self.inbox.get()
            self.skt.send(message)

class MyApplication(WebSocketApplication):

    def __init__(self, ws):
        #sessionno
        self.sessionno = GlobalObject().wsapp.countGenerator.next()
        WebSocketApplication.__init__(self, ws)

    @property
    def GlobalSessionno(self):
        return "%s_%s" % (GlobalObject().json_config['name'], self.sessionno)

    def getCurrentClient(self):
        """
        获取当前client
        :return:
        """
        return self.ws.handler.active_client

    def on_open(self):
        log.msg("Some websocket client connected!")
        #self绑定自己的sender
        self.mysender = MySender(self.getCurrentClient().ws)
        self.mysender.start()
        #设置sessionno并且保存所有的client到字典
        GlobalObject().wsapp.allClients[self.sessionno] = self
        #节点自己实现
        GlobalObject().wsapp.doConnectionMade(self)

    def on_message(self, message):
        gevent.spawn(self.doDataReceived, message)
        # self.doDataReceived(message)

    def doDataReceived(self, message):
        if message is None:
            return
        try:
            message = CustProtc.decoder(message)
            if message['m'] > 1 and getattr(self, "pid", None):
                #用户登陆成功后其他消息全部转发到gate
                GlobalObject().wsapp.service.callTarget(200, self, message)
            elif message['m'] == 1 or message['m'] == 0:
                GlobalObject().wsapp.service.callTarget(message['m'], self, message)
            else:
                raise Exception("invalid message. data: %s" % message)
        except Exception, e:
            log.err(e)
            self.loseConnection()



    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def sendData(self, data):
        log.msg("send: %s" % data)
        self.mysender.sendall(CustProtc.encoder(data))

    def safeWriteMsg(self, client, message):
        client.mysender.sendall(CustProtc.encoder(message))

    def broadcast(self, message):
        log.msg('broadcast')
        for client in GlobalObject().wsapp.allClients.values():
            self.safeWriteMsg(client, {
                'msg_type': 'message',
                'nickname': message['nickname'],
                'message': message['message']
            })


    def on_close(self, reason):
        log.msg("websocket Connection closed! ")
        #kill 当前客户端的sender
        self.mysender.close()
        #移除client
        del GlobalObject().wsapp.allClients[self.sessionno]
        #掉线节点自己处理
        GlobalObject().wsapp.doConnectionLost(self)

    def loseConnection(self):
        """
        主动断开链接
        :return:
        """
        self.ws.close()


class MyWebSocketServer(Greenlet):
    """
    websocket服务器/当factory用吧
    """
    def __init__(self, port, urls, app, debug=False, **ssl_options):
        """端口监听器\n
        @param port: int 监听的端口\n
        @param urls: 链接的正则表达式列表\n
        @param apps: gevent-websocket封装的applications
        @param ssl_options: ssl参数
        """
        Greenlet.__init__(self)
        self.port = port
        self.urls = urls
        self.apps = app
        self.factory = None
        #sessionno生成器
        self.countGenerator = itertools.count(1, 1)
        self.allClients = {}
        #服务通道
        self.service = None
        #ssl_options
        root_ca = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ca")
        if ssl_options:
            self.ssl_options = ssl_options
            self.ssl_options.update({"keyfile": os.path.join(root_ca, self.ssl_options['keyfile']),
                                     "certfile": os.path.join(root_ca, self.ssl_options['certfile'])})
        else:
            self.ssl_options = {}
        log.msg(self.ssl_options)
        self.debug = debug

    def addServiceChan(self, service):
        """
        添加服务通道
        :return:
        """
        self.service = service


    def getHost(self):
        """获取主机地址\n
        """
        return "0.0.0.0", self.port

    def getClientBySessionno(self, sessionno):
        """
        根据sessionno获取client
        :param sessionno:
        :return:
        """
        return self.allClients.get(sessionno, None)

    def _run(self):
        """启动监听器\n
        """
        log.msg('WebSocketServer on %s' % self.port)
        self.factory = WebSocketServer(
            self.getHost(),

            Resource([(i, self.apps) for i in self.urls]),

            debug=self.debug,

            **self.ssl_options
        )
        self.factory.serve_forever()