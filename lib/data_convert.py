import hashlib, time, copy
import datetime
from datetime import timedelta


def get_md5(data: str, encoding='utf-8'):
    md5 = hashlib.md5()
    md5.update(data.encode(encoding=encoding))
    return md5.hexdigest()


def get_html_code_detail(summary='detail', detail='msg'):
    """
    获取<details>标签代码
    :param summary: 
    :param detail: 
    :return: 
    """
    final_string = '{} \nresult:{}'.format(summary, detail)
    return final_string


def get_dict_by_key(data: list, key, value):
    if data is None:
        return None
    for dict_item in data:
        if dict_item[key] == value:
            return dict_item
    return None


def get_dict_by_key_list(data: list, key_list: list, value_list: list):
    if data is None:
        return None
    for dict_item in data:
        flag = True
        for index in range(len(key_list)):
            if dict_item[key_list[index]] != value_list[index]:
                flag = False
                break
        if flag is True:
            return dict_item
    return None


def get_value_list_by_key(data: list, key):
    valut_list = []
    for dict_item in data:
        if key in dict_item.keys():
            valut_list.append(dict_item[key])
    return valut_list


def get_value_set_by_key(data: list, key):
    value_list = get_value_list_by_key(data, key)
    return set(value_list)


def get_time_str(format='_%Y%m%d_%H_%M_%S', time_stamp=None):
    if time_stamp is None:
        time_stamp = time.time()
    return time.strftime(format, time.localtime(int(time_stamp)))


def list_contains(a: list, b: list):
    """判断数组包含"""
    if not (isinstance(a, list) and isinstance(b, list)):
        print('入参不是数组!')
        return False
    if len(b) > len(a):
        return False
    for item in b:
        if item not in a:
            print('数组不包含: {}'.format(item))
            return False
    return True


def list_equals(a: list, b: list):
    """判断数组相等(忽略排序与重复)"""
    return list_contains(a, b) and list_contains(b, a)


def get_date_str(days=0, format="%Y-%m-%d", minutes=0):
    date = datetime.datetime.now() + timedelta(days=days) + timedelta(minutes=minutes)
    return date.strftime(format)


def get_week_begin_str(date_str, format="%Y-%m-%d"):
    """获取当周星期一日期"""
    date = datetime.datetime.strptime(date_str, format)
    week_begin = (date - timedelta(days=date.weekday())).strftime(format)
    return week_begin


def get_week_end_str(date_str, format="%Y-%m-%d"):
    """获取当周星期天日期"""
    date = datetime.datetime.strptime(date_str, format)
    week_end = (date + timedelta(days=6 - date.weekday())).strftime(format)
    return week_end


def get_week_day_by_index(date_str, index, format="%Y-%m-%d"):
    date = datetime.datetime.strptime(date_str, format)
    week_begin = (date - timedelta(days=date.weekday()))
    final_date = (week_begin + timedelta(days=index - 1)).strftime(format)
    return final_date


def get_week_day_index(date_str, format="%Y-%m-%d"):
    """获取传入日期是星期几"""
    date = datetime.datetime.strptime(date_str, format)
    return date.weekday() + 1


def delete_empty_item(params: dict):
    """删除字典中空的项"""
    key_list = params.copy().keys()
    for key in key_list:
        if params.get(key) is None:
            params.pop(key)
