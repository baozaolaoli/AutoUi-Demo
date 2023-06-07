from lib.edu_request import *
from config.common_config import *


def update_file(myshixun_id,game_id, path, content,evaluate=1,exercise_id=None, windows='code',secret_repository=None, headers=user_header_1):
    url = host + '/api/myshixuns/{}/update_file.json'.format(myshixun_id)
    data = {
        "path":path,
        "evaluate":evaluate,
        "content":content,
        "game_id":game_id,
        "exercise_id":exercise_id,
        "windows":windows
    }
    res = req_post(url=url, params=data, desc="编辑实训文件", headers=headers)
    return res.json()

