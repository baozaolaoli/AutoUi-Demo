from lib.edu_request import *
from config.common_config import *


def get_shixun_info(shixun_id, headers=user_header_1):
    url = host + '/api/shixuns/{}.json'.format(shixun_id)
    data = {}
    res = req_get(url=url, params=data, desc="获取实训基本信息", headers=headers)
    return res.json()


def new(headers=user_header_1):
    url = host + '/api/shixuns/new.json'
    data = {}
    res = req_get(url=url, params=data, desc="获取新建实训信息", headers=headers)
    return res.json()


def environment_info(mirror_repository_id, headers=user_header_1):
    url = host + '/api/shixuns/environment_info.json'
    data = {'mirror_repository_id': mirror_repository_id}
    res = req_get(url=url, params=data, desc="获取实训镜像信息", headers=headers)
    return res.json()


def choose_environment_or_skip(image_id, headers=user_header_1):
    url = host + '/api/shixuns/choose_environment_or_skip.json'
    data = {'image_id': image_id}
    res = req_post(url=url, params=data, desc="选择镜像", headers=headers)
    return res.json()


def base_info_save(shixun_id, name, description='description', tag_name=api_code_root, headers=user_header_1):
    url = host + '/api/shixuns/{}/base_info_save.json'.format(shixun_id)
    data = {
        "shixun": {
            "name": name,
            "description": description,
            "shixun_tags": [
                {"id": None, "name": tag_name}
            ],
            "attachment_id": "",
            "cover_image_id": "",
            "attachment_id_b": ""
        }
    }
    res = req_post(url=url, params=data, desc="修改实训基本信息", headers=headers)
    return res.json()


def init_repository(id, headers=user_header_1):
    url = host + '/api/shixuns/{}/init_repository.json'.format(id)
    data = {"id": id}
    res = req_post(url=url, params=data, desc="实训仓库初始化", headers=headers)
    return res.json()


def repository(id, headers=user_header_1):
    url = host + '/api/shixuns/{}/repository.json'.format(id)
    data = {"id": id, "path": ""}
    res = req_post(url=url, params=data, desc="实训仓库查询", headers=headers)
    return res.json()


def challenges_new(shixun_id, headers=user_header_1):
    url = host + '/api/shixuns/{}/challenges/new.json'.format(shixun_id)
    data = {}
    res = req_get(url=url, params=data, desc="获取新建实训信息", headers=headers)
    return res.json()


def challenges(shixun_id, subject, task_pass, difficulty=1, challenge_tag=["AUTO_TEST"], st=0, score=100,
               headers=user_header_1):
    url = host + '/api/shixuns/{}/challenges.json'.format(shixun_id)
    data = {
        "subject": subject,  # 任务标题
        "task_pass": task_pass,  # 任务描述
        "difficulty": difficulty,
        "challenge_tag": challenge_tag,
        "score": score,
        "identifier": shixun_id,
        "st": st  # 类型 0:评测题  1:选择题
    }
    res = req_post(url=url, params=data, desc="新建实训", headers=headers)
    return res.json()


def challenges_edit(shixun_id, challenge_id, path, exec_path, test_set, tab=1, headers=user_header_1):
    url = host + '/api/shixuns/{}/challenges/{}.json'.format(shixun_id, challenge_id)
    data = {
        "id": shixun_id,
        "challengesId": challenge_id,
        "tab": tab,
        "challenge": {
            "exec_time": 20,
            "show_type": -1,
            "path": path,
            "exec_path": exec_path,
            "test_set_rules": 0,
            "ignore_space": 1,
            "test_set_score": True,
            "is_file": False,
            "test_set_average": True,
            "test_set_rules_expression": None
        },
        "test_set": test_set
    }
    res = req_put(url=url, params=data, desc="修改关卡评测设置", headers=headers)
    return res.json()


def open_or_close_rank_list(shixun_id, challenge_id, rank, challenge_extend={}, headers=user_header_1):
    url = host + '/api/shixuns/{}/challenges/{}/open_or_close_rank_list.json'.format(shixun_id, challenge_id)
    data = {
        "challenge_extend": challenge_extend,
        "rank": rank
    }
    res = req_post(url=url, params=data, desc="修改关卡排行榜设置", headers=headers)
    return res.json()


def add_file(shixun_id, path, message='自动化测试提交', content='', headers=user_header_1):
    url = host + '/api/shixuns/{}/add_file.json'.format(shixun_id)
    data = {
        "id": shixun_id,
        "message": message,
        "content": content,
        "path": path
    }
    res = req_post(url=url, params=data, desc="git新增文件", headers=headers)
    return res.json()


def update_file(shixun_id, path, content, secret_repository=None, headers=user_header_1):
    url = host + '/api/shixuns/{}/update_file.json'.format(shixun_id)
    data = {
        "id": shixun_id,
        "path": path,
        "content": content,
        "secret_repository": secret_repository
    }
    res = req_post(url=url, params=data, desc="git编辑文件", headers=headers)
    return res.json()


def publish(shixun_id, headers=user_header_1):
    url = host + '/api/shixuns/{}/publish.json'.format(shixun_id)
    data = {}
    res = req_get(url=url, params=data, desc="发布实训", headers=headers)
    return res.json()


def shixun_exec(shixun_id, headers=user_header_1):
    url = host + '/api/shixuns/{}/shixun_exec.json'.format(shixun_id)
    data = {'id':shixun_id}
    res = req_get(url=url, params=data, desc="开始挑战", headers=headers)
    return res.json()


