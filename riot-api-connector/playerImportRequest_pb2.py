# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: playerImportRequest.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19playerImportRequest.proto\"\x1e\n\rImportRequest\x12\r\n\x05puuid\x18\x01 \x01(\t\":\n\x0bImportReply\x12\x16\n\x0egames_imported\x18\x01 \x01(\x05\x12\x13\n\x0btotal_games\x18\x02 \x01(\x05\x32=\n\x08Importer\x12\x31\n\rimport_player\x12\x0e.ImportRequest\x1a\x0c.ImportReply\"\x00\x30\x01\x62\x06proto3')



_IMPORTREQUEST = DESCRIPTOR.message_types_by_name['ImportRequest']
_IMPORTREPLY = DESCRIPTOR.message_types_by_name['ImportReply']
ImportRequest = _reflection.GeneratedProtocolMessageType('ImportRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMPORTREQUEST,
  '__module__' : 'playerImportRequest_pb2'
  # @@protoc_insertion_point(class_scope:ImportRequest)
  })
_sym_db.RegisterMessage(ImportRequest)

ImportReply = _reflection.GeneratedProtocolMessageType('ImportReply', (_message.Message,), {
  'DESCRIPTOR' : _IMPORTREPLY,
  '__module__' : 'playerImportRequest_pb2'
  # @@protoc_insertion_point(class_scope:ImportReply)
  })
_sym_db.RegisterMessage(ImportReply)

_IMPORTER = DESCRIPTOR.services_by_name['Importer']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _IMPORTREQUEST._serialized_start=29
  _IMPORTREQUEST._serialized_end=59
  _IMPORTREPLY._serialized_start=61
  _IMPORTREPLY._serialized_end=119
  _IMPORTER._serialized_start=121
  _IMPORTER._serialized_end=182
# @@protoc_insertion_point(module_scope)
