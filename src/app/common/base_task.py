#encoding:utf8
class BaseTask(object):
    """
    基类
    """
    def __init__(self, t, isloop=True, isstartcall=False, **kwargs):
        """
        初始化参数
        :param t: 时间(s) 定时任务为datetime
        :param isloop: 是否循环任务
        :return:
        """
        self.t = t
        self.isloop = isloop
        self.isstartcall = isstartcall
        self.kwargs = kwargs

    def task(self):
        """
        任务
        :param kwargs:
        :return:
        """
        pass
