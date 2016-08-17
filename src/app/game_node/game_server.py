#coding=utf-8
from gfirefly.server.globalobject import GlobalObject
from gfirefly.utils.services import CommandService
from gfirefly.server.logobj import log
from app.game_node.core.playermanager import PlayerManager

#自定义服务器通道
gamecommandservice = CommandService("gamecommandservice")
setattr(GlobalObject(), "gamecommandservice", gamecommandservice)

#导入逻辑接口
from api import common_api

def stopHandler():
    """
    服务器关闭处理
    :return:
    """
    log.msg(u'server %s is stop ing...' % GlobalObject().json_config['name'])
    log.msg(u'syncdb...')
    for player in PlayerManager().getAllPlayers().values():
        log.msg("%s sync player %s" % (GlobalObject().json_config['name'], player.uid))
        player.saveDataToDb()


GlobalObject().stophandler = stopHandler

log.msg("game api: %s" % gamecommandservice._targets.keys())
