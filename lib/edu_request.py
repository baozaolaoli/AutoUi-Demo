import json, os, time, html
from urllib.parse import quote, unquote
import requests
from config.common_config import default_headers, host
from lib.data_convert import get_time_str
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def req_post(url, params, headers=default_headers, timeout=30, verify=False,
             desc='请求接口', check_status=200, check_code=None):
    try:
        params_str = '非json格式入参,解析失败'
        params_str = json.dumps(params, ensure_ascii=False, indent=4)
        params = json.dumps(params)
        t1 = time.time()
        res = requests.post(headers=headers, url=url, data=params, timeout=timeout, verify=verify)
        t2 = time.time()
    except Exception as e:
        print(str(e))
        print(
            '<pre><details><summary>▼{}</summary>method:POST\nurl:{}\n<pre>headers:{}</pre><pre>body:{}</pre><pre>接口调用异常:{}</pre></details></pre>'
            .format(desc, url, headers, params_str, str(e)))
        assert False, '接口调用异常:{}'.format(str(e))
    dt = str('%.4f' % (t2 - t1))
    result = res.content.decode()
    try:
        result = json.dumps(res.json(), ensure_ascii=False, indent=4)
    except Exception:
        pass
    print(
        '<pre><details><summary>▼{}</summary>method:POST\nuse_time:{}\nurl:{}\nstatus_code:{}\nheaders:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre>body:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre>return:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre></details></pre>'
        .format(desc, dt, url, res.status_code, json.dumps(headers, ensure_ascii=False, indent=4), params_str, result))
    # if t2 - t1 > 1:
    #     with open('{}{}slow_api.html'.format(report_path,os.path.sep), 'a') as f:
    #         msg = '<pre><details><summary>▼{}</summary>method:POST\nuse_time:{}\nurl:{}\nstatus_code:{}\nheaders:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre>body:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre>return:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre></details></pre>' \
    #             .format(desc, dt, url, res.status_code, json.dumps(headers, ensure_ascii=False, indent=4), params_str, result)
    #         f.write(msg)
    if check_status is not None:
        assert res.status_code == check_status, '返回错误状态码错误,预期:{},实际:{}'.format(check_status, res.status_code)
    if check_code is not None:
        assert res.json()['code'] == check_code, '返回code错误,预期:{},实际:{}'.format(check_code, res.json()['code'])
    return res


def req_get(url, params={}, headers=default_headers, timeout=300, verify=False,
            desc='请求接口', check_status=200, check_code=None):
    try:
        t1 = time.time()
        res = requests.get(headers=headers, url=url, params=params, timeout=timeout, verify=verify)
        t2 = time.time()
    except Exception as e:
        print(
            '<pre><details><summary>▼{}</summary>method:GET\nurl:{}\n<pre>headers:{}</pre><pre>接口调用异常:{}</pre></details></pre>'
            .format(desc, url, headers, str(e)))
        assert False, '接口调用异常:{}'.format(str(e))
    dt = str('%.4f' % (t2 - t1))
    result = res.content.decode()
    try:
        result = json.dumps(res.json(), ensure_ascii=False, indent=4)
    except Exception:
        pass
    print(
        '<pre><details><summary>▼{}</summary>method:GET\nuse_time:{}\nurl:{}\nstatus_code:{}\nheaders:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre>return:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre></details></pre>'
        .format(desc, dt, html.escape(unquote(res.url)), res.status_code,
                json.dumps(headers, ensure_ascii=False, indent=4), result))
    # if t2 - t1 > 1:
    #     with open('{}{}slow_api.html'.format(report_path,os.path.sep), 'a') as f:
    #         msg = '<pre><details><summary>▼{}</summary>method:GET\nuse_time:{}\nurl:{}\nstatus_code:{}\nheaders:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre>return:\n<pre class="json-renderer" style="padding: 0px 20px">{}</pre></details></pre>' \
    #             .format(desc, dt, html.escape(unquote(res.url)), res.status_code, json.dumps(headers, ensure_ascii=False, indent=4), result)
    #         f.write(msg)
    if check_status is not None:
        assert res.status_code == check_status, '返回错误状态码错误,预期:{},实际:{}'.format(check_status, res.status_code)
    if check_code is not None:
        assert res.json()['code'] == check_code, '返回code错误,预期:{},实际:{}'.format(check_code, res.json()['code'])
    return res
