import os, shutil
import time
import unittest

from lib.report import HTMLTestRunner
from config.common_path import report_path
import sys, getopt


class WGTestLoader(unittest.TestLoader):
    @staticmethod
    def _get_cases_from_suites(suites):
        final_suite = unittest.TestSuite()
        for sub_item in suites:
            if isinstance(sub_item, unittest.TestCase):
                final_suite.addTest(sub_item)
            else:
                for sub_case in WGTestLoader._get_cases_from_suites(sub_item):
                    final_suite.addTest(sub_case)
        return final_suite

    @staticmethod
    def find_cases_by_files(files, find_path):
        if type(files) == str:
            files = [files]
        final_suite = unittest.TestSuite()
        for file in files:
            final_suite.addTests(WGTestLoader().discover(start_dir=find_path, pattern=file, top_level_dir=find_path))
        final_suite = WGTestLoader._get_cases_from_suites(final_suite)
        return final_suite

    @staticmethod
    def suite_filter(suite, tags=None):
        """根据标签过滤要执行的用例"""
        if not tags:
            return suite
        if type(tags) == str:
            tags = [tags]
        new_suite = unittest.TestSuite()
        for test_case in suite:
            for tag in tags:
                if tag == '' or (test_case._testMethodDoc and tag in test_case._testMethodDoc):
                    new_suite.addTest(test_case)
                    break
        return new_suite

    @staticmethod
    def run_suite(suite, report_path=report_path):
        t_start = time.time()
        # time_str = time.strftime('_%Y%m%d_%H_%M_%S', time.localtime(int(t_start)))
        time_str = ''
        report_name = '{}{}report{}.html'.format(report_path, os.sep, time_str)
        runner = HTMLTestRunner(stream=open(report_name, 'wb'), title='Auto Api Report', verbosity=2)
        result = runner.run(suite)
        t_end = time.time()
        dt = str('%.4f' % (t_end - t_start))
        # print('test over!\nuse time:{} S\npass:{}\nfail:{}\nerror:{}'
        #       .format(dt, result.success_count, result.failure_count, result.error_count))

    # @staticmethod
    # def run_test(dir_name, file_names=['test*.py'], tags=None):
    #     suite_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], dir_name)
    #     suite = WGTestLoader.find_cases_by_files(files=file_names, find_path=suite_dir)
    #     final_suite = WGTestLoader.suite_filter(suite, tags)
    #     WGTestLoader.run_suite(suite=final_suite, report_path=report_path)

    @staticmethod
    def run_test(dir_names, file_names=['test*.py'], tags=None):
        suite_all = unittest.TestSuite()
        for dir_name in dir_names:
            suite_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'suites', dir_name)
            suite = WGTestLoader.find_cases_by_files(files=file_names, find_path=suite_dir)
            suite_all.addTests(suite)
        final_suite = WGTestLoader.suite_filter(suite_all, tags)
        WGTestLoader.run_suite(suite=final_suite, report_path=report_path)


def clear_reports():
    if os.path.exists(report_path):
        shutil.rmtree(report_path)
    os.mkdir(report_path)
    os.mkdir('{}{}picture'.format(report_path, os.path.sep))


def main(argv):
    suite_dirs = None
    file_names = None
    tags = None
    environment = None
    try:
        opts, args = getopt.getopt(argv, "hd:s:t:e:x", ["help", "dir", "suite", "tag", "environment"])
    except getopt.GetoptError as e:
        # print(e)
        # print('test.py -d <dir> -s <suite> -t <tag> -e <environment>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            # print('test.py -d <dir> -s <suite> -t <tag> -e <environment>')
            sys.exit()
        elif opt in ("-e", "--environment"):
            environment = arg
        elif opt in ("-d", "--dir"):
            suite_dirs = arg.split(';')
        elif opt in ("-s", "--suite"):
            file_names = arg.split(';')
        elif opt in ("-t", "--tag"):
            tags = arg.split(';')
    if not suite_dirs:
        # suite_dirs = ['bup', 'opdm', 'opb', 'opd', 'opn', 'iadm', 'inpi', 'inpd', 'umc']
        suite_dirs = ['demo']
    if not file_names:
        file_names = ['**.py']
    if not tags:
        tags = ['']
    if not environment:
        environment = 'test'
    return suite_dirs, file_names, tags, environment


if __name__ == '__main__':
    clear_reports()
    suite_dirs, file_names, tags, environment = main(sys.argv[1:])
    # suite_dirs = ['inpd']
    # file_names = ['suite_02_inpdOrder.py']
    tags = ['']
    # environment = 'test'
    print('测试目录:', suite_dirs)
    print('测试文件:', file_names)
    print('测试标签:', tags)
    print('测试环境:', environment)
    # sys.path.append('environment tag:{}'.format(environment))
    # assert environment in ['test', 'dev'], '-e --environment must in ["test","dev"]'
    WGTestLoader.run_test(dir_names=suite_dirs, file_names=file_names, tags=tags)
