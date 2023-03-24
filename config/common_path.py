import os

# 常用路径
config_path = os.path.split(os.path.realpath(__file__))[0]
report_path = '{}{}..{}report'.format(config_path, os.sep, os.sep)
pic_path = '{}{}picture'.format(report_path, os.sep)
if not os.path.exists(report_path):
    os.mkdir(report_path)
if not os.path.exists(pic_path):
    os.mkdir(pic_path)
