import time

def log_err(text):
    # 打印错误信息
    print('[%s ERR ]: %s' % (time.strftime('%H:%M:%S'), text))

def log_info(text):
    # 打印信息
    print('[%s INFO]: %s' % (time.strftime('%H:%M:%S'), text))

def log_warn(text):
    # 打印警告信息
    print('[%s WARN]: %s' % (time.strftime('%H:%M:%S'), text))

