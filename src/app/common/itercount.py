#coding:utf8

import itertools
from gfirefly.utils.singleton import Singleton

class IterCountBase(object):
    """
    所有的计数器
    room_identity 游戏房间号
    net sessionno wsnet_c
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.allCountGenerator = {"wsnet_c": itertools.count(1, 1), "room_identity": itertools.count(1, 1)}

    def getNext(self, key):
        """
        @des: 获取指定标示的计数
        :param key:
        :return:
        """
        countGenerator = self.allCountGenerator.get(key, None)
        if countGenerator is None:
            countGenerator = itertools.count(1, 1)
            self.allCountGenerator[key] = countGenerator

        return countGenerator.next()
