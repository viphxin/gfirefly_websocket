#coding=utf-8
"""
这里实现自定义协议的编解码
"""
import ujson as json

class CustProtc(object):
    @classmethod
    def encoder(cls, message):
        """
        编码
        :param message:
        :return:
        """
        return json.dumps(message)

    @classmethod
    def decoder(cls, message):
        """
        解码
        :param message:
        :return:
        """
        return json.loads(message)