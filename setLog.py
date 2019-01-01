# 这里为了简便，同时处理：输出控制台和保存到文件中
import logging

from logging import handlers

class Logger(object):

    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self, filename, fhLevel = logging.INFO, chLevel = logging.WARNING,  when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        # 第一步，创建一个logger  
        self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)  # Log等级总开关

        # 第二步，创建一个handler，用于写入日志文件  
        fh = logging.FileHandler(filename, mode='a')  # open的打开模式这里可以进行参考
        fh.setLevel(fhLevel)  # 输出到file的log等级的开关  

        # 第三步，再创建一个handler，用于输出到控制台  
        ch = logging.StreamHandler()
        ch.setLevel(chLevel)  # 输出到console的log等级的开关  

        # 第四步，定义handler的输出格式  
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨

        format_str = logging.Formatter(fmt)  # 设置日志格式
        th.setFormatter(format_str)  # 设置文件里写入的格式
        ch.setFormatter(format_str)

        # 第五步，将logger添加到handler里面  
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # 忽略警告
        logging.captureWarnings(True)


        # self.logger = logging.getLogger(filename)
        # format_str = logging.Formatter(fmt)  # 设置日志格式
        # self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        # sh = logging.StreamHandler()  # 往屏幕上输出
        # sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
        #                                        encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # # 实例化TimedRotatingFileHandler
        # # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # # S 秒
        # # M 分
        # # H 小时、
        # # D 天、
        # # W 每星期（interval==0时代表星期一）
        # # midnight 每天凌晨
        # th.setFormatter(format_str)  # 设置文件里写入的格式
        # self.logger.addHandler(sh)  # 把对象加到logger里
        # self.logger.addHandler(th)

        # 忽略警告
        # logging.captureWarnings(True)


# # 第一步，创建一个logger  
# logger = logging.getLogger()
# logger.setLevel(logging.INFO) # Log等级总开关  
#
# # 第二步，创建一个handler，用于写入日志文件  
# logfile = './log.txt'
# fh = logging.FileHandler(logfile, mode='a') # open的打开模式这里可以进行参考
# fh.setLevel(logging.DEBUG) # 输出到file的log等级的开关  
#
# # 第三步，再创建一个handler，用于输出到控制台  
# ch = logging.StreamHandler()
# ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关  
#
# # 第四步，定义handler的输出格式  
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
#
# # 第五步，将logger添加到handler里面  
# logger.addHandler(fh)
# logger.addHandler(ch)
