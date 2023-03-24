import time
import cx_Oracle as cx
from pymssql import connect
from lib.data_convert import get_html_code_detail

'''
数据库操作
'''


def exec_query_sql(sql, user, password, host, instance, desc='未写描述'):
    """执行orcle查询语句"""
    t0 = time.time()
    try:
        with cx.connect('{}/{}@{}/{}'.format(user, password, host, instance)) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            all_keys = [x[0] for x in cursor.description]
            res = [dict(zip(all_keys, row)) for row in res]
    except Exception as e:
        dt = str('%.4f' % (time.time() - t0))
        print(get_html_code_detail(summary='QUERY SQL:{}'.format(desc), detail='{}\n执行时长:{}\n执行失败:{}'.format(sql, dt, str(e))))
        assert False, str(e)
    dt = str('%.4f' % (time.time() - t0))
    print(get_html_code_detail(summary='QUERY SQL:{}'.format(desc), detail='{}\n执行时长:{}\n结果行数:{}'.format(sql, dt, len(res))))
    return res


def exec_update_sql(sql, user, password, host, instance, desc='未写描述'):
    """执行orcle修改语句"""
    t0 = time.time()
    try:
        with cx.connect('{}/{}@{}/{}'.format(user, password, host, instance)) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            row_count = cursor.rowcount
            # assert row_count < 100, '批量操作数据超过100条'
            conn.commit()
    except Exception as e:
        dt = str('%.4f' % (time.time() - t0))
        print(get_html_code_detail(summary='UPDATE_SQL:{}'.format(desc), detail='{}\n执行时长:{}\n执行失败:{}'.format(sql, dt, str(e))))
        assert False, str(e)
    dt = str('%.4f' % (time.time() - t0))
    print(get_html_code_detail(summary='UPDATE_SQL:{}'.format(desc), detail='{}\n执行时长:{}\n影响行数:{}'.format(sql, dt, row_count)))
    return row_count


if __name__ == "__main__":
    # 查询
    res = exec_query_sql(sql='SELECT * FROM HIS.PIX_PATIENT_INFO',
                         host='172.26.0.14',
                         user='TEST_DBA_RW',
                         password='rEuLRN9qnq',
                         instance='wghistest')
    print(res)
    # 修改
    res = exec_update_sql(sql="UPDATE HIS.PIX_PATIENT_INFO SET PY_CODE='ZXF' WHERE PATIENT_NAME like '张新发%'",
                          host='172.26.0.14',
                          user='TEST_DBA_RW',
                          password='rEuLRN9qnq',
                          instance='wghistest')
    print(res)
