# -*- coding: utf-8 -*-

import os
import sys
from functools import wraps

from tornado.ioloop import IOLoop
from tornado.stack_context import ExceptionStackContext
from tornado.util import raise_exc_info

from mamba import describe, context, before
from sure import expect

from viper import mappers, errors


def tornado(instance):
    def get_async_test_timeout():
        """Get the global timeout setting for async tests.

        Returns a float, the timeout in seconds.
        """
        try:
            return float(os.environ.get('ASYNC_TEST_TIMEOUT'))
        except (ValueError, TypeError):
            return 5

    class async(object):
        def __init__(self):
            self.__stopped = False
            self.__running = False
            self.__failure = None
            self.__stop_args = None
            self.__timeout = None

        def before_each(self):
            self.io_loop = self.get_new_ioloop()
            self.io_loop.make_current()

        def after_each(self):
            self.io_loop.clear_current()
            if (not IOLoop.initialized() or
                    self.io_loop is not IOLoop.instance()):
                # Try to clean up any file descriptors left open in the ioloop.
                # This avoids leaks, especially when tests are run repeatedly
                # in the same process with autoreload (because curl does not
                # set FD_CLOEXEC on its file descriptors)
                self.io_loop.close(all_fds=True)
            # In case an exception escaped or the StackContext caught an exception
            # when there wasn't a wait() to re-raise it, do so here.
            # This is our last chance to raise an exception in a way that the
            # unittest machinery understands.
            self.__rethrow()

        def get_new_ioloop(self):
            """Creates a new `.IOLoop` for this test.  May be overridden in
            subclasses for tests that require a specific `.IOLoop` (usually
            the singleton `.IOLoop.instance()`).
            """
            return IOLoop()#.instance()

        def _handle_exception(self, typ, value, tb):
            self.__failure = (typ, value, tb)
            self.stop()
            return True

        def __rethrow(self):
            if self.__failure is not None:
                failure = self.__failure
                self.__failure = None
                raise_exc_info(failure)

        def run(self, function, result=None):
            @wraps(function)
            def wrapped():
                with ExceptionStackContext(self._handle_exception):
                    self.before_each()
                    function()
                    self.after_each()
                # As a last resort, if an exception escaped super.run() and wasn't
                # re-raised in tearDown, raise it here.  This will cause the
                # unittest run to fail messily, but that's better than silently
                # ignoring an error.
                self.__rethrow()
            return wrapped

        def stop(self, _arg=None, **kwargs):
            """Stops the `.IOLoop`, causing one pending (or future) call to `wait()`
            to return.

            Keyword arguments or a single positional argument passed to `stop()` are
            saved and will be returned by `wait()`.
            """
            assert _arg is None or not kwargs
            self.__stop_args = kwargs or _arg
            if self.__running:
                self.io_loop.stop()
                self.__running = False
            self.__stopped = True

        def wait(self, condition=None, timeout=None):
            """Runs the `.IOLoop` until stop is called or timeout has passed.

            In the event of a timeout, an exception will be thrown. The default
            timeout is 5 seconds; it may be overridden with a ``timeout`` keyword
            argument or globally with the ASYNC_TEST_TIMEOUT environment variable.

            If ``condition`` is not None, the `.IOLoop` will be restarted
            after `stop()` until ``condition()`` returns true.
            """
            if timeout is None:
                timeout = get_async_test_timeout()

            if not self.__stopped:
                if timeout:
                    def timeout_func():
                        try:
                            raise Exception(
                                'Async operation timed out after %s seconds' %
                                timeout)
                        except Exception:
                            self.__failure = sys.exc_info()
                        self.stop()
                    self.__timeout = self.io_loop.add_timeout(self.io_loop.time() + timeout, timeout_func)
                while True:
                    self.__running = True
                    self.io_loop.start()
                    if (self.__failure is not None or
                            condition is None or condition()):
                        break
                if self.__timeout is not None:
                    self.io_loop.remove_timeout(self.__timeout)
                    self.__timeout = None
            assert self.__stopped
            self.__stopped = False
            self.__rethrow()
            result = self.__stop_args
            self.__stop_args = None
            return result

    instance.context = async()
    return instance


with describe('PythonPackageIndex') as _:
    @before.all
    def create_pypi():
        _.pypi = mappers.PythonPackageIndex()

    with context('when package exists in pypi'):
        @before.all
        def query_for_tornado():
            _.package = _.pypi.get_by_name('tornado')

        def it_should_be_marked_is_being_from_pypi():
            expect(_.package.is_from_pypi).to.be.true

        def it_should_match_name():
            expect(_.package.name).to.be.equal('tornado')

        def it_should_have_releases_info():
            expect(_.package.releases()).to.have.length_of(1)
            expect(_.package.releases()[0]).to.have.property('author').to.be.equal('Facebook')

    def it_should_raise_an_error_if_package_does_not_exist():
        expect(_.pypi.get_by_name).when.called_with(u'I-really-hope-this-package-does-not-exist').to.throw(errors.NotFoundError)

    with context('when specify a version'):
        @before.all
        def query_for_tornado_2dot1():
            _.package = _.pypi.get_by_name(u'tornado', u'2.1')

        def it_should_contain_specific_release():
            expect(_.package.release('2.1')).to.not_be.none

    with tornado(context('when downloading files')) as async:
        @async.run
        def it_should_download_files_if_present_on_url_list():
            _.pypi.download_files(u'Flask', on_file_downloaded=_expect_flask_was_downloaded)
            async.wait()

        def _expect_flask_was_downloaded(file_, content):
            expect(file_.name.startswith('Flask')).to.be.true
            expect(file_).to.have.property('filetype').to.be.equal('sdist')
            expect(file_).to.have.property('md5_digest').to.not_be.none
            expect(content).to.not_be.none
            async.stop()

        @async.run
        def it_should_download_files_if_url_list_is_empty():
            _.pypi.download_files(u'tornado', version=u'2.1', on_file_downloaded=_expect_tornado_was_downloaded)
            async.wait()

        def _expect_tornado_was_downloaded(file_, content):
            expect(file_.name.startswith('tornado')).to.be.true
            expect('2.1' in file_.name)
            expect(file_).to.have.property('filetype').to.be.equal('sdist')
            expect(file_).to.have.property('md5_digest').to.be.none
            expect(content).to.not_be.none
            async.stop()
