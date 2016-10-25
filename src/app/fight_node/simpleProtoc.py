#encoding:utf8
from gtwisted.utils import log
import struct
import traceback

class DataPackError(Exception):
    """An error occurred binding to an interface"""

    def __str__(self):
        s = self.__doc__
        if self.args:
            s = '%s: %s' % (s, ' '.join(self.args))
        s = '%s.' % s
        return s

#test
"""
public   enum MsgHeader : byte
    {
        //to server
        NewPlayerMsg,
        ReconnectMsg,
        UserInputMsg,

        //to client >40
        InitRoomMsg=40,
        PlayerJionMsg,
        ReadyMsg,
        StepRoomMsg
    }
"""
msg_len = {
    0: 0,
    1: 0,
    2: 2,
    40: 12,
    41: 4,
    42: 0,
    43: 5
}

class SimpleProtoc:
    """
    战斗服务器专用简单数据包协议
    """
    def __init__(self):
        '''
        初始化
        '''
        self.maxLen = 100*1024

    def getHeadlength(self):
        """
        获取数据包的长度
        """
        return 8

    def unpack(self,dpack):
        '''解包
        '''
        try:
            ud = struct.unpack('<II', dpack)
        except struct.error,de:
            log.err(de,traceback.format_exc())
            return {'result':False, 'command': 0, 'length': 0}

        length = ud[0]
        command = ud[1]
        #TODO
        #这里做包体长度校验大于200KB的包直接丢弃
        if length < self.maxLen:
            return {'result':True,'command':command,'length':length}
        else:
            log.err("invalid message. command: %s.length: %s" % (command, length))
            return {'result':False,'command':command,'length':length}

    def pack(self, command, response):
        '''
        打包数据包
        '''
        if response:
            serialData = response.SerializeToString()
            length = serialData.__len__()
        else:
            serialData = ""
            length = 0

        data = struct.pack('<II', length, command)
        return data + serialData