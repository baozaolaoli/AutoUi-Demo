from lib.edu_request import *
from config.common_config import *


def rep_content(game_id, path, headers=user_header_1):
    url = host + '/api/tasks/{}/rep_content.json'.format(game_id)
    data = {
        'path': path
    }
    res = req_get(url=url, params=data, headers=headers, desc="获取实训关卡文件内容")
    return res.json()


def tasks_info(game_id, headers=user_header_1):
    url = host + '/api/tasks/{}.json'.format(game_id)
    data = {}
    res = req_get(url=url, params=data, headers=headers, desc="获取实训关卡信息")
    return res.json()


def cost_time(game_id, cost_time, headers=user_header_1):
    url = host + '/api/tasks/{}/cost_time.json?time={}'.format(game_id, cost_time)
    data = {}
    res = req_post(url=url, params=data, headers=headers, desc="获取myshixun_id")
    return res.json()


def game_build(game_id, sec_key, commitID, headers=user_header_1):
    url = host + '/api/tasks/{}/game_build.json'.format(game_id)
    data = {
        "sec_key": sec_key,
        "resubmit": "",
        "first": 1,
        "content_modified": 0,
        "extras": {"commitID": commitID}
    }
    res = req_post(url=url, params=data, headers=headers, desc="实训关卡执行评测")
    return res.json()


def game_status(game_id,challenge_id,resubmit,sec_key,time_out='false', headers=user_header_1):
    url = host + '/api/tasks/{}/game_status.json'.format(game_id)
    data = {
        'resubmit':resubmit,
        'time_out':time_out,
        'port':'-1',
        'sec_key':sec_key,
        'challenge_id':challenge_id,
        'subject_id':''
    }
    res = req_get(url=url, params=data, headers=headers, desc="获取评测状态")
    return res.json()
