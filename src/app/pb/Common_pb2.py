# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Common.proto

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
  name='Common.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0c\x43ommon.proto\"\x1f\n\x0e\x43ommonResponse\x12\r\n\x05state\x18\x01 \x01(\x05\x42\x08\xaa\x02\x05Protob\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_COMMONRESPONSE = _descriptor.Descriptor(
  name='CommonResponse',
  full_name='CommonResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='CommonResponse.state', index=0,
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
  serialized_start=16,
  serialized_end=47,
)

DESCRIPTOR.message_types_by_name['CommonResponse'] = _COMMONRESPONSE

CommonResponse = _reflection.GeneratedProtocolMessageType('CommonResponse', (_message.Message,), dict(
  DESCRIPTOR = _COMMONRESPONSE,
  __module__ = 'Common_pb2'
  # @@protoc_insertion_point(class_scope:CommonResponse)
  ))
_sym_db.RegisterMessage(CommonResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\005Proto'))
# @@protoc_insertion_point(module_scope)
