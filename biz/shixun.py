"""实训相关业务函数"""

from api.educoder import shixuns, tasks, progress_homeworks, myshixuns
from config.common_config import *
from lib.data_convert import *


def create_shixun(shixun_name, environment_name, git_file_list, challenge_list, headers=user_header_1):
    """
    1.新建实训
    2.选择镜像
    3.开启仓库、初始化文件
    4.添加关卡、修改关卡评测设置
    """

    # 创建实训并修改基本信息
    image_list = shixuns.new(headers=headers)['data']['other_image']
    image_id = get_dict_by_key(image_list, 'name', environment_name)['id']
    shixuns.environment_info(image_id, headers=headers)
    create_info = shixuns.choose_environment_or_skip(image_id=image_id, headers=headers)
    assert create_info['status'] == 0, "创建实训失败,返回status不为0"
    shixun_id = create_info['data']['identifier']
    save_info = shixuns.base_info_save(shixun_id=shixun_id, name=shixun_name, headers=headers)
    assert save_info['status'] == 0, '修改实训信息失败,返回status不为0'

    # 初始化git仓库
    git_info = init_git_for_shixun(shixun_id=shixun_id,
                                   file_list=git_file_list,
                                   headers=headers)

    # 添加关卡
    add_challenges_for_shixun(shixun_id=shixun_id, challenge_list=challenge_list, headers=headers)
    publish_info = shixuns.publish(shixun_id=shixun_id, headers=headers)
    assert publish_info.get('status') == 0, '发布实训失败'
    return create_info, git_info


def init_git_for_shixun(shixun_id, file_list=[], headers=user_header_1):
    """初始化实训仓库"""
    init_info = shixuns.init_repository(headers=headers, id=shixun_id)
    assert init_info['status'] == 0, '实训仓库初始化失败,返回status不为0'
    for file_path, content in file_list:
        res = shixuns.add_file(shixun_id=shixun_id, path=file_path, headers=headers)
        assert res.get('url'), 'git添加文件异常'
        res = shixuns.update_file(shixun_id=shixun_id, path=file_path,
                                  content=content, headers=headers)
        assert res.get('content'), 'git修改文件异常'
    git_repository = shixuns.repository(headers=headers, id=shixun_id)
    git_url = git_repository.get('git_url')
    assert git_url, "获取到仓库地址为空！"
    return git_repository


def add_challenges_for_shixun(shixun_id, challenge_list=[], headers=user_header_1):
    for subject, task_pass, path, exec_path, test_set in challenge_list:
        res = shixuns.challenges_new(shixun_id=shixun_id, headers=headers)
        assert res.get('go_back_url'), '获取新建实训信息异常'

        challenge_info = shixuns.challenges(shixun_id=shixun_id,
                                            subject=subject,
                                            task_pass=task_pass,
                                            headers=headers)
        assert challenge_info.get('status') == 1, '新建实训失败'
        res = shixuns.challenges_edit(shixun_id=shixun_id, challenge_id=challenge_info['challenge_id'],
                                      path=path, exec_path=exec_path,
                                      test_set=test_set,
                                      headers=headers)
        assert res.get('status') == 0, '修改实训评测设置失败'
        res = shixuns.open_or_close_rank_list(shixun_id=shixun_id,
                                              challenge_id=challenge_info['challenge_id'],
                                              rank='DEFAULT',
                                              headers=headers)
        assert res.get('status') == 0, '开启关卡排行榜失败'


def start_challenge(shixun_id, file_content_list, headers=user_header_1):
    result_urls = []
    game_id = shixuns.shixun_exec(shixun_id=shixun_id, headers=headers)['game_identifier']
    for file_content,expect_status in file_content_list:
        assert game_id, '关卡数量小于传入的文件数量!'
        task_info = tasks.tasks_info(game_id=game_id, headers=headers)
        tasks.rep_content(game_id=game_id, path=task_info['challenge']['path'], headers=headers)
        tasks.cost_time(game_id=game_id, cost_time=0, headers=headers)
        my_shixun_id = task_info['myshixun']['identifier']

        res = myshixuns.update_file(myshixun_id=my_shixun_id, game_id=task_info['game']['id'],
                                    path=task_info['challenge']['path'], content=file_content)
        sec_key, commitID = res['sec_key'], res['content']['commitID']
        build_res = tasks.game_build(game_id=game_id, sec_key=sec_key, commitID=commitID)
        assert build_res.get('status') == 1, '执行评测报错'

        check_over = False
        check_count = 20
        while check_count > 0 and not check_over:
            check_count -= 1
            time.sleep(2)
            res = tasks.game_status(game_id=game_id, challenge_id=task_info['challenge']['id'],
                                    resubmit=build_res['resubmit'], sec_key=sec_key)
            if res.get('status') == expect_status:
                check_over = True
                print('评测结果轮询完成')
        assert check_over, '轮询评测结果失败'
        result_urls.append('https://www.educoder.net/tasks/{}'.format(game_id))
        game_id = task_info['next_game']
    return result_urls


if __name__ == '__main__':
    from biz.home_page import login_educoder

    login_educoder(headers=user_header_1)
    # create_shixun(environment_name='Python3.6', shixun_name='自动化测试demo' + get_time_str())
