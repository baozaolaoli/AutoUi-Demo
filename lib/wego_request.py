import json, os, time
from urllib.parse import quote, unquote
import requests
from workflow.common_config import default_headers, global_configs
from lib.data_convert import get_time_str
import copy, traceback
from datetime import datetime


def req_post(url, params, client, headers=default_headers, timeout=300, verify=False,
             desc='请求接口', check_status=200, check_code='0', sys_uri=None, pathCode=None, orgCode=None, token=None):
    try:
        if sys_uri is not None:
            headers.update({'systemUri': sys_uri})
        if global_configs['pathCode'] is not None:
            headers.update({'pathCode': global_configs['pathCode']})
        elif 'pathCode' in headers.keys():
            headers.pop('pathCode')
        if global_configs['X-Preference'] is not None:
            headers.update({'X-Preference': quote(global_configs['X-Preference'])})
        elif 'X-Preference' in headers.keys():
            headers.pop('X-Preference')
        if pathCode is not None:
            headers.update({'pathCode': pathCode})
        if orgCode is not None:
            cfg = copy.deepcopy(global_configs)
            Preference = eval(cfg['X-Preference'])
            Preference.update({'orgCode': orgCode})
            cfg['X-Preference'] = str(Preference)
            headers.update({'X-Preference': quote(cfg['X-Preference'])})
        if token is not None:
            headers.update({'X-Auth-Token': token})
        params_str = '非json格式入参,解析失败'
        params_str = json.dumps(params, ensure_ascii=False)
        params = json.dumps(params)
        t1 = time.time()
        if client is requests:
            res = requests.post(headers=headers, url=url, data=params, timeout=timeout, verify=verify)
        else:
            res = client.post(headers=headers, url=url, data=params, timeout=timeout, verify=verify, name='{}({})'.format(desc, url))
        t2 = time.time()
    except Exception as e:
        msg = '--------\n{}\ntime:{}\nmethod:POST\nurl:{}\nheaders:{}\nbody:{}\n接口调用异常:{}\n--------\n'.format(desc, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), url, headers, params_str, str(e))
        if hasattr(client, 'fileName'):
            with open(client.fileName, 'a+') as f:
                f.write(msg)
        print(msg)
        assert False, '{}, 接口调用异常:{}'.format(url, str(e))
    dt = str('%.4f' % (t2 - t1))
    result = res.content.decode()
    try:
        result = json.dumps(res.json(), ensure_ascii=False)
    except Exception:
        pass
    msg = '--------\n{}\ntime:{}\nmethod:POST\nuse_time:{}\nurl:{}\nstatus_code:{}\nheaders:\n{}\nbody:\n{}\nreturn:\n{}\n--------\n'.format(desc, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), dt, url, res.status_code, json.dumps(headers, ensure_ascii=False), params_str, result)
    if hasattr(client, 'fileName'):
        with open(client.fileName, 'a+') as f:
            f.write(msg)
    else:
        print(msg)
    if check_status is not None:
        assert res.status_code == check_status, '{},返回错误状态码错误,预期:{},实际:{}'.format(url, check_status, res.status_code)
    if check_code is not None:
        assert res.json()['code'] == check_code, '{},返回code错误,预期:{},实际:{}'.format(url, check_code, res.json()['code'])
    return res


def req_get(url, client, params={}, headers=default_headers, timeout=300, verify=False,
            desc='请求接口', check_status=200, check_code='0', sys_uri=None, pathCode=None, orgCode=None, token=None):
    try:
        if sys_uri is not None:
            headers.update({'systemUri': sys_uri})
        if global_configs['pathCode'] is not None:
            headers.update({'pathCode': global_configs['pathCode']})
        elif 'pathCode' in headers.keys():
            headers.pop('pathCode')
        if global_configs['X-Preference'] is not None:
            headers.update({'X-Preference': quote(global_configs['X-Preference'])})
        elif 'X-Preference' in headers.keys():
            headers.pop('X-Preference')
        if pathCode is not None:
            headers.update({'pathCode': pathCode})
        if orgCode is not None:
            cfg = copy.deepcopy(global_configs)
            Preference = eval(cfg['X-Preference'])
            Preference.update({'orgCode': orgCode})
            cfg['X-Preference'] = str(Preference)
            headers.update({'X-Preference': quote(cfg['X-Preference'])})
        if token is not None:
            headers.update({'X-Auth-Token': token})
        t1 = time.time()
        if client is requests:
            res = requests.get(headers=headers, url=url, params=params, timeout=timeout, verify=verify)
        else:
            res = client.get(headers=headers, url=url, params=params, timeout=timeout, verify=verify, name='{}({})'.format(desc, url.split('?')[0]))
        t2 = time.time()
    except Exception as e:
        msg = '\n--------\n{}\ntime:{}\nmethod:GET\nurl:{}\nheaders:{}\n接口调用异常:{}\n--------\n'.format(desc, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), url, headers, str(e))
        print(msg)
        if hasattr(client, 'fileName'):
            with open(client.fileName, 'a+') as f:
                f.write(msg)
        assert False, '接口调用异常:{}'.format(str(e))
    dt = str('%.4f' % (t2 - t1))
    result = res.content.decode()
    try:
        result = json.dumps(res.json(), ensure_ascii=False)
    except Exception:
        pass
    msg = '\n--------\n{}\ntime:{}\nmethod:GET\nuse_time:{}\nurl:{}\nstatus_code:{}\nheaders:\n{}\nreturn:\n{}\n--------\n' \
        .format(desc, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), dt, unquote(res.url), res.status_code, json.dumps(headers, ensure_ascii=False), result)
    if hasattr(client, 'fileName'):
        with open(client.fileName, 'a+') as f:
            f.write(msg)
    else:
        print(msg)
    if check_status is not None:
        assert res.status_code == check_status, '返回错误状态码错误,预期:{},实际:{}'.format(check_status, res.status_code)
    if check_code is not None:
        assert res.json()['code'] == check_code, '返回code错误,预期:{},实际:{}'.format(check_code, res.json()['code'])
    return res


if __name__ == '__main__':
    # req_post(url='http://www.baidu.com', params={})
    # req_get(url='http://127.0.0.1:4523/mock/655081/XXX/DETAIL', params={"ID":1})
    print(get_time_str())
