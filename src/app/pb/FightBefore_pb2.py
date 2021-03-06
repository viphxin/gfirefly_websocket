# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: FightBefore.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='FightBefore.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x11\x46ightBefore.proto\"?\n\x0bInitRoomMsg\x12\x0c\n\x04seed\x18\x01 \x01(\x05\x12\x0f\n\x07localID\x18\x02 \x01(\x05\x12\x11\n\tmaxPlayer\x18\x03 \x01(\x05\"&\n\rPlayerJionMsg\x12\x15\n\rplayerLocalID\x18\x01 \x01(\x05\x42\x08\xaa\x02\x05Protob\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_INITROOMMSG = _descriptor.Descriptor(
  name='InitRoomMsg',
  full_name='InitRoomMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='seed', full_name='InitRoomMsg.seed', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='localID', full_name='InitRoomMsg.localID', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maxPlayer', full_name='InitRoomMsg.maxPlayer', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=84,
)


_PLAYERJIONMSG = _descriptor.Descriptor(
  name='PlayerJionMsg',
  full_name='PlayerJionMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playerLocalID', full_name='PlayerJionMsg.playerLocalID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=86,
  serialized_end=124,
)

DESCRIPTOR.message_types_by_name['InitRoomMsg'] = _INITROOMMSG
DESCRIPTOR.message_types_by_name['PlayerJionMsg'] = _PLAYERJIONMSG

InitRoomMsg = _reflection.GeneratedProtocolMessageType('InitRoomMsg', (_message.Message,), dict(
  DESCRIPTOR = _INITROOMMSG,
  __module__ = 'FightBefore_pb2'
  # @@protoc_insertion_point(class_scope:InitRoomMsg)
  ))
_sym_db.RegisterMessage(InitRoomMsg)

PlayerJionMsg = _reflection.GeneratedProtocolMessageType('PlayerJionMsg', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERJIONMSG,
  __module__ = 'FightBefore_pb2'
  # @@protoc_insertion_point(class_scope:PlayerJionMsg)
  ))
_sym_db.RegisterMessage(PlayerJionMsg)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\005Proto'))
# @@protoc_insertion_point(module_scope)
