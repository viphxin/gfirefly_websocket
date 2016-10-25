#coding:utf8
import random, hashlib, time
from global_configs import MD5_PASSPORT_KEY
from gfirefly.server.globalobject import GlobalObject

def selectNode(nodes):
    """
    这里自定义选择nodes的规则, 默认规则随机
    :param nodes:
    :return:
    """
    return random.choice(nodes)

def add_md5(params):
    # 不需要加入签名的参数
    NO_MD5_PARAMS = ['rt', 'flag']
    ALL_NEEDMD5_PARAMS = [k for k, v in params.items() if k not in NO_MD5_PARAMS and v != '']
    # 参数按照字母排序
    ALL_NEEDMD5_PARAMS.sort()
    ALL_NEEDMD5_VALUES = [("%s" % params[k]).encode('utf8') for k in ALL_NEEDMD5_PARAMS]
    md5_str1 = hashlib.md5()
    md5_str1.update("%s%s" % (''.join(ALL_NEEDMD5_VALUES), MD5_PASSPORT_KEY))
    params.update({'flag': md5_str1.hexdigest(), "rt": time.time()})


def getOneRootByType(tp):
    """
    获取某一种Root的一个
    :param tp:
    :return:
    """
    return selectNode([v for k, v in GlobalObject().remote.items() if tp in k])

def selectTypeNode(nodetype):
    """
    选出所有的同类型节点getName
    :param nodetype:
    :return:
    """
    nodes = [i for i in GlobalObject().root.childsmanager._childs.values() if i.getName().find(nodetype) >= 0]
    return nodes

def getcurrentconn(sessionno):
    """
    注意链接对象和protocol 链接对象封装了protocol
    @des: 根据连接ID，获取连接对象, sessionno=conn.transport.sessionno
    """
    connobj = GlobalObject().netfactory.connmanager.getConnectionByID(sessionno)
    return connobj