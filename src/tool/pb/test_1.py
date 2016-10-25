import addressbook_pb2

test_msg = addressbook_pb2.TestMsg()
print dir(test_msg)
test_msg.name1 = "hx1111"
test_msg.name2 = "hx22222"
test_msg.test_list.extend(["dasd", 'ssss', '111'])
test_msg.test_dict.update({"a": "b", "v": "d"})

data = test_msg.SerializeToString()
print len(data)
print data
print "#"*30
test_msg_1 = addressbook_pb2.TestMsg()
test_msg_1.ParseFromString(data)
print dir(test_msg_1.WhichOneof)
print test_msg_1.WhichOneof.im_self
print test_msg_1.name1
print test_msg_1.name2
print test_msg_1.test_list
print test_msg_1.test_dict
