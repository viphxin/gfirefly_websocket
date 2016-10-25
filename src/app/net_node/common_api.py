#coding:utf8
import time, requests
import ujson as json
from app.common.decorators import wsServiceHandle
from gfirefly.server.globalobject import GlobalObject
from app.common.utils import add_md5, getOneRootByType
from global_configs import PASSPORT_IP, PASSPORT_PORT


@wsServiceHandle
def heatBeat_0(conn, data):
    """
    心跳数据包
    :param conn: client
    :param data: 请求数据
    :return:
    """
    setattr(conn, "heatbeat_t", time.time())
    #不返回!!!!!!
    conn.sendData({'m': 0, 's': 1})#测试返回

@wsServiceHandle
def userLogin_1(conn, data):
    """
    用户登陆
    :param conn: client
    :param data: 请求数据
    :return:
    """
    if 0:
        #远程到passport验证用户有效性并且换取userID
        params = {'t': data['t']}
        add_md5(params)
        resp = requests.post("http://%s:%s/oauth/checkouttocken/" % (PASSPORT_IP, PASSPORT_PORT), params, json=True, verify=False)
        resp = json.loads(resp.content)
        if resp['success']:
            pid = resp['data']
            #这只全局变量pid
            setattr(conn, "pid", pid)
            #验证通过分配gameserver node
            getOneRootByType("gate").callRemoteNotForResult("allocGameNode", {'m': 1, 'pid': pid, 'sid': conn.GlobalSessionno})#调用root服务器(gate)
            # conn.sendData({'m': 1, 's': 1})
        else:
            #用户登陆失败,啥也不说主动断开连接
            conn.loseConnection()
    else:
        #just a test
        #这只全局变量pid
        setattr(conn, "pid", data['t'])
        #验证通过分配gameserver node
        getOneRootByType("gate").callRemoteNotForResult("allocGameNode", {'m': 1, 'pid': data['t'], 'sid': conn.GlobalSessionno})

@wsServiceHandle
def proxyToGate_200(conn, data):
    """
    转发到gate
    :param conn: client
    :param data: 请求数据
    :return:
    """
    #所有消息都加上这两个字段方便gate路由到gamenode
    data.update({'pid': conn.pid, 'sid': conn.GlobalSessionno})
    getOneRootByType("gate").callRemoteNotForResult("forwarding", data)
