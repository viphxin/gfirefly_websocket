#encoding:utf8
"""
战斗服务器流程测试
"""
import gevent, sys, os, json, time
sys.path.append(
        os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
)

from simpleProtoc import SimpleProtoc, msg_len
from gtwisted.core.protocols import BaseProtocol, ClientFactory
from gtwisted.core import reactor

dataprotocl = SimpleProtoc()

#pb import
from app.pb import Common_pb2
from app.pb import FightBefore_pb2
from app.pb import Oauth_pb2
from app.pb import Fighting_pb2

class MyClientProtocol(BaseProtocol):
    buff = ""
    length = dataprotocl.getHeadlength()
    needSSL = False
    st_ping = time.time()

    def userInput(self):
        userInputData = Fighting_pb2.UserInput()
        userInputData.data = 12
        self.safeToWriteData(userInputData, 10)
        self.st_rping = time.time()
        reactor.callLater(1, self.userInput)


    def connectionMade(self):
        """当连接建立时的处理\n
        """
        print "connectioned. server massage: %s" % (self.transport.getAddress(),)
        self.ping_test()
        #login
        loginMsg = Oauth_pb2.UserLogin()
        loginMsg.userId = "%s" % self.factory.uid
        loginMsg.accesstocken = self.factory.tocken
        self.safeToWriteData(loginMsg, 1)
        # cuiMsg = Fighting_pb2.CollectUsersInput()
        # cuiMsg.step = 100
        # for i in range(200*1024):
        #     userInputData = cuiMsg.usersInputData.add()
        #     userInputData.ID = 1
        #     userInputData.data = 1
        # self.safeToWriteData(cuiMsg, 20)

    def connectionLost(self,reason):
        """当连接断开时的处理\n
        @param reason: Exception 端口连接的原因\n
        """
        print "lost connection. reason: %s" % reason

    @property
    def isNeedSSL(self):
        if 0 and self.needSSL:
            return True
        else:
            return False

    def dataReceived(self, data):
        """当连接数据到达时的处理\n
        @param data: str 接收到的数据\n
        """
        # print "receive: ", data
        self.buff += data
        while self.buff.__len__() >= self.length:
            unpackdata = dataprotocl.unpack(self.buff[:self.length])
            if not unpackdata.get('result'):
                self.factory.loseConnection()
                break
            command = unpackdata.get('command')
            rlength = unpackdata.get('length')


            request = self.buff[self.length:self.length+rlength]
            if request.__len__()< rlength:
                print('some data lose')
                break
            self.buff = self.buff[self.length+rlength:]
            #解密
            if self.isNeedSSL:
                response = self.doMsg(command, self.factory.cipher.decrypt(request))
            else:
                response = self.doMsg(command, request)

            if not response:
                continue
            self.safeToWriteData(response, command)

    def ping_test(self):
        self.safeToWriteData("", 0)
        self.st_ping = time.time()
        reactor.callLater(5, self.ping_test)



    def doMsg(self, command, data):
        """
        do
        :param data:
        :return:
        """
        if command == 1:
            msg = Common_pb2.CommonResponse()
            msg.ParseFromString(data)
            if msg.state:
                #send 2
                self.safeToWriteData("", 2)
                pass
        elif command == 2:
            self.safeToWriteData("", 4)
        elif command == 3:
            print "received: ", command, data
            self.userInput()

        elif command == 5:
            msg = FightBefore_pb2.InitRoomMsg()
            msg.ParseFromString(data)
            self.localId = msg.localID

        elif command == 11:
            msg = Fighting_pb2.CollectUsersInput()
            msg.ParseFromString(data)
            # print command, len(data)
            # print "time: %s.step: %s. data: %s" % (time.time(), msg.step, msg.usersInputData)
            # print time.time()
            for i in msg.usersInputData:
                if i.ID == self.localId:
                    print "%s==%s" % (i.ID, self.localId)
                    print "rping %s ms." % ((time.time() - self.st_rping)*1000, )
        elif command == 0:
            print "ping %s ms." % ((time.time() - self.st_ping)*1000, )
        else:
            print "received: ", command, data


    def safeToWriteData(self,data,command):
        '''线程安全的向客户端发送数据
        @param data: str 要向客户端写的数据
        '''
        # print "send: ", data, "==", command
        if self.isNeedSSL == False:
            senddata = dataprotocl.pack(command, data)
        else:
            senddata = dataprotocl.pack(command, self.factory.cipher.encrypt(data))
        self.transport.sendall(senddata)

def do_gameserver(uid, tocken):
    """
    gameserver test
    :return:
    """
    clientfactory = ClientFactory()
    setattr(clientfactory, 'uid', uid)
    setattr(clientfactory, 'tocken', tocken)
    clientfactory.protocol = MyClientProtocol
    # reactor.connectTCP('127.0.0.1', 18109, clientfactory)
    # reactor.connectTCP('115.29.138.246', 8109, clientfactory)
    # ucloud
    # reactor.connectTCP('106.75.76.157', 8109, clientfactory)
    reactor.connectTCP('127.0.0.1', 8109, clientfactory)

if __name__ == "__main__":
    #房间号
    for i in range(1, 101, 1):
        do_gameserver(i, "tocken_%s" % i)
    reactor.run()
