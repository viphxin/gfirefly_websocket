#coding=utf-8
import sys, os
sys.path.append(
        os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
)
from app.pb import Fighting_pb2
import time

st = time.time()
stepnum = 0
for i in range(30000):
    stepnum += 1
    cuiMsg = Fighting_pb2.CollectUsersInput()
    cuiMsg.step = stepnum
    userInputData = cuiMsg.usersInputData.add()
    userInputData.ID = 1
    userInputData.data = 2
    data = cuiMsg.SerializeToString()
    cuiMsg_t = Fighting_pb2.CollectUsersInput()
    cuiMsg_t.ParseFromString(data)


print time.time() - st
