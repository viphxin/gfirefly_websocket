#coding=utf-8
from websocket import create_connection
import ujson as json
import sys, time
if 'threading' in sys.modules:
    del sys.modules['threading']
import gevent
from gevent import monkey; monkey.patch_all()
ping_st = time.time()

def do_receive(sck, nick):
    print "Receiving..."
    while 1:
        result = sck.recv()
        print "%s Received '%s'." % (nick, result)
        result_json = json.loads(result)
        if result_json['nickname'] == nick:
            print "ping: %s ms" % ((time.time() - ping_st)*1000)

def do_task(ws_url, nick):
    global ping_st
    ws = create_connection(ws_url)
    gevent.spawn(do_receive, ws, nick)
    i = 0
    while 1:
        # print "Sending 'Hello, World'..."
        message = {
            "msg_type": 'message',
            "nickname": nick,
            "message": "2222text %s" % i,
        }
        ws.send(json.dumps(message))
        ping_st = time.time()
        i += 1
        # print "Sent"

        gevent.sleep(1)
    ws.close()


if __name__ == "__main__":
    # do_task("ws://127.0.0.1:3001/chat", "huangxin")
    jobs = [gevent.spawn(do_task, "ws://127.0.0.1:3001/chat", "nick-%s" % (i, )) for i in range(1,20,1)]
    gevent.wait(jobs)