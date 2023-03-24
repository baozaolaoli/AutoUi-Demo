from  lib.data_convert import get_time_str
#
print(get_time_str(format='_%Y%m%d_%H_%M_%S_%f'))
#

import datetime

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))