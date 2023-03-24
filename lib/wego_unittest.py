from unittest.case import _Outcome
import unittest
import time


class WegoUnittest(unittest.TestCase):
    use_time = None

    def __call__(self, *args, **kwds):
        """记录执行时间"""
        t0 = int(time.time() * 1000)
        res = self.run(*args, **kwds)
        t1 = int(time.time() * 1000)
        self.use_time = str(int(t1 - t0))
        return res

    def run(self, result=None):
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return
        expecting_failure_method = getattr(testMethod,
                                           "__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,
                                          "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)
        try:
            self._outcome = outcome

            with outcome.testPartExecutor(self):
                self.setUp()
            if outcome.success:
                outcome.expecting_failure = expecting_failure
                with outcome.testPartExecutor(self, isTest=True):
                    testMethod()
                outcome.expecting_failure = False
                with outcome.testPartExecutor(self):
                    self.tearDown()

            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None

    def get_running_errors(self):
        error_list = []
        for methodInfo,errorInfo in self._outcome.errors:
            if errorInfo is not None:
                error_list.append(errorInfo)
        return error_list

    def shortDescription(self):
        """用例描述自动加上执行时间"""
        # space_num = 50 - len(str(self._testMethodDoc)) if len(str(self._testMethodDoc))<=50 else 0
        doc = '{}{}-({} ms)'.format(self._testMethodDoc, '&nbsp;' * 8, self.use_time)
        return doc and doc.split("\n")[0].strip() or None

    def get_title(self):
        """用例描述"""
        doc = self._testMethodDoc
        return doc and doc.split("\n")[0].strip() or None
