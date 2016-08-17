#coding=utf-8
from websocket import create_connection
import ujson as json
import sys, time
if 'threading' in sys.modules:
    del sys.modules['threading']
import gevent
from gevent import monkey; monkey.patch_all()
import requests, hashlib

PASSPORT_URL = "http://127.0.0.1:9991/"

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

def do_receive(sck, nick):
    print "Receiving..."
    ping_st = time.time()
    while 1:
        result = sck.recv()
        print "%s Received '%s'." % (nick, result)

        print "ping: %s ms" % ((time.time() - ping_st)*1000)
        #test
        sck.send(json.dumps({'m': 2}))
        ping_st = time.time()

def do_task(ws_url, nick, tocken):
    ws = create_connection(ws_url)
    gevent.spawn(do_receive, ws, nick)
    message = {
        "m": 1,
        "t": tocken
    }
    ws.send(json.dumps(message))
    while 1:
        #发心跳包
        ws.send(json.dumps({'m': 0}))
        gevent.sleep(60)
    #ws.close()


if __name__ == "__main__":
    jobs = []
    for i in range(2000):
        tocken, dis = do_passport("huangxin")
        jobs = [gevent.spawn(do_task, "ws://%s/chat" % dis, "huangxin", tocken)]
        # jobs = [gevent.spawn(do_task, "ws://127.0.0.1:3002/chat", "nick-%s" % (i, )) for i in range(1,2000,1)]
    gevent.wait(jobs)
