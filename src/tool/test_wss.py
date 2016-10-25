#coding=utf-8
import sys, json, requests, hashlib, time
from optparse import OptionParser

from twisted.python import log
from twisted.internet import reactor, ssl

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS


PASSPORT_URL = "http://127.0.0.1:18008/"

def add_md5(params):
    # 不需要加入签名的参数
    NO_MD5_PARAMS = ['rt', 'flag']
    ALL_NEEDMD5_PARAMS = [k for k, v in params.items() if k not in NO_MD5_PARAMS and v != '']
    # 参数按照字母排序
    ALL_NEEDMD5_PARAMS.sort()
    ALL_NEEDMD5_VALUES = [("%s" % params[k]).encode('utf8') for k in ALL_NEEDMD5_PARAMS]
    md5_str1 = hashlib.md5()
    md5_str1.update("%s%s" % (''.join(ALL_NEEDMD5_VALUES), "dasdasfff"))
    params.update({'flag': md5_str1.hexdigest(), "rt": time.time()})

def do_passport(username):
    """
    passport inteface test
    :return:
    """
    session = requests.Session()
    #登陆
    while 1:#muti clients flag rt may timeout
        #do test m=1 --------start
        params_m1 = {"username": username, "token":"", "pt": 0, 'pw': '123456'}

        add_md5(params_m1)
        resp = session.post("%soauth/login/" % PASSPORT_URL,params_m1, json=True, verify=False)
        print resp.content
        m1_resp = json.loads(resp.content)
        assert m1_resp['success'] == True
        #do test m=1 --------end
        break

    #获取服务器列表
    # add cert=('/path/server.crt', '/path/key')
    resp = session.post("%sgameserver/getallserver/" % PASSPORT_URL, {}, json=True, verify=False)
    print resp.content
    m1_resp = json.loads(resp.content)
    assert m1_resp['success'] == True

    #获取tocken
    params_m2 = {'s': m1_resp['data'][0]['id']}
    add_md5(params_m2)
    resp = session.post("%soauth/gettocken/" % PASSPORT_URL, params_m2, json=True, verify=False)
    print resp.content
    m2_resp = json.loads(resp.content)
    assert m2_resp['success'] == True

    #验证tocken
    # params_m3 = {'t': m2_resp['data']}
    # add_md5(params_m3)
    # resp = session.post("%soauth/checkouttocken/" % PASSPORT_URL, params_m3, json=True, verify=False)
    # print resp.content
    # m3_resp = json.loads(resp.content)
    # assert m3_resp['success'] == True
    return m2_resp['data'], m1_resp['data'][0]['s']


class EchoClientProtocol(WebSocketClientProtocol):


    def sendMsg(self, data):
        self.sendMessage(json.dumps(data))

    def sendHeatData(self):
        self.ping_st = time.time()
        self.sendMsg({'m': 0})
        reactor.callLater(60, self.sendHeatData)

    def onOpen(self):
        self.sendHeatData()
        #用户登陆
        self.sendMsg({'m': 1, 't': self.factory.extra_data['tocken']})

    def onMessage(self, data, isBinary):
        print data
        if not isBinary:
            print("Text message received: {}".format(data.decode('utf8')))

            data = json.loads(data)
            if data['m'] == 0:
                print "ping: %s ms" % ((time.time() - self.ping_st)*1000)
            elif data['m'] == 1 and data['s'] == 1:
                self.sendMsg({'m': 2})
            elif data['m'] == 2:

                # self.sendMsg({'m': 2})
                reactor.callLater(1, self.sendMsg, {'m': 2})


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="The WebSocket URL", default="wss://192.168.2.225:18102/chat")
    (options, args) = parser.parse_args()

    k = 0
    for i in xrange(1, 1000):
        # create a WS server factory with our protocol
        ##
        tocken, dis = do_passport("huangxin")
        # factory = WebSocketClientFactory(options.url)
        factory = WebSocketClientFactory("wss://%s/chat" % dis)
        factory.extra_data = {"nickname": "huangxin_%s" % i, "tocken": tocken}
        factory.protocol = EchoClientProtocol

        # SSL client context: default
        ##
        if factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None
        # connectWS(factory, contextFactory)
        reactor.callLater(k, connectWS, factory, contextFactory)
        k += 0.05
    reactor.run()