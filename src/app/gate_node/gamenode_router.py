#coding:utf8
import binascii
from app.common.utils import selectTypeNode

class GameNodeRouterException(Exception):pass

class GameNodeRouter(object):
    """
    这是一个无状态的router(算法决定)
    """
    def __init__(self, identity):
        self.identity = identity

    def get_node(self):
        """
        获取节点
        :return:
        """
        vnode = self.get_vnode()
        #这里的规则是每个物理节点平均分配玩家
        nodes = selectTypeNode("game")
        n = len(nodes)
        p = 1024/n
        for i in range(n, 0, -1):
            if vnode >= p*(i - 1):
                return nodes[i-1]

        raise GameNodeRouterException("GameNodeRouter get_node error. vnode %s" % vnode)


    def get_vnode(self):
        """
        获取虚拟节点
        :return: 0-1023
        """
        return binascii.crc32(self.identity) % 1024


