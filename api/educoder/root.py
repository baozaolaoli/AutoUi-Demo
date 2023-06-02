from lib.edu_request import *
from config.common_config import *


def setting():
    url = host + '/api/setting.json'
    data = {}
    res = req_get(url=url, params=data, desc="获取设置接口")
    return res


def courses(course_list_name, name, school, class_period='30', allowed_quit=False, credit='3', end_date="2026-06-04",
            is_public=0, set=0, is_show_conceal=False, student_join_approve=False,
            course_module_types=["announcement", "shixun_homework"],headers=user_header_1):
    """
    新建课堂接口
    :param course_list_name: 
    :param name: 
    :param class_period: 
    :param allowed_quit: 
    :param credit: 
    :param end_date: 
    :param is_public: 
    :param set: 
    :param is_show_conceal: 
    :param student_join_approve: 
    :param course_module_types: 
    :return: 
    """
    url = host + '/api/courses.json'
    data = {
        "course_list_name": course_list_name,
        "name": name,
        "class_period": class_period,
        "allowed_quit": allowed_quit,
        "credit": credit,
        "end_date": end_date,
        "is_public": is_public,
        "course_module_types": course_module_types,
        "school": school,
        "set": set,
        "is_show_conceal": is_show_conceal,
        "student_join_approve": student_join_approve
    }
    res = req_post(url=url, params=data, desc="创建课堂接口",headers=headers)
    return res


if __name__ == '__main__':
    pass
    # setting()
