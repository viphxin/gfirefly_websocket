#coding:utf8
from gfirefly.server.globalobject import GlobalObject
from gfirefly.server.logobj import log

#导入逻辑接口
import common_api

log.msg("gate_node api: %s" % GlobalObject().root.service._targets.keys())