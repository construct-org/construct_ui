# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import inspect
import logging
import sys
import time
import traceback
from Qt import QtCore, QtWidgets


_log = logging.getLogger('construct.async')



def event_reporter(event_name, task):
    def reporter(*args, **kwargs):
        _log.debug('%s | %s | %s, %s' % (task, event_name, args, kwargs))
    return reporter


def submit_async(task, *args, **kwargs):
    '''Submit a function to run in the global QThreadPool.

    Arguments:
        task (callable or iterable): A Function to call or generator to consume
        *args: Arguments to pass to task
        **kwargs: Keyword Arguments to pass to task

    Returns:
        AsyncTask

    Examples:
        # Start a long running background task
        def print_result(result):
            print(result)

        def long_running_query():
            for i in range(100):
                yield i
                time.sleep(1)

        task = submit_async(long_running_query)
        task.on_result(print_result)
        task.start()

        # Wait for results
        task.wait()
    '''

    # task is a generator function
    # meaning we have to actually initialize it by calling it
    if inspect.isgeneratorfunction(task):
        qrunnable = AsyncIterator(task(*args, **kwargs))

    # Task is not a generator function but is iterable
    elif hasattr(task, '__iter__'):
        # if args and kwargs are passed we assumed that it is an object
        # that needs to be initialized with those params then consumed
        if args or kwargs:
            qrunnable = AsyncIterator(task(*args, **kwargs))
        # assume that the object has already been initialized and we
        # just need to consume it
        else:
            qrunnable = AsyncIterator(task)

    # We've got a callable task, either a function or object with a __call__
    # method
    elif callable(task):
        qrunnable = AsyncCallable(task, *args, **kwargs)
    else:
        raise TypeError('Unsupport type: %s %s' % (task, type(task)))

    pool = QtCore.QThreadPool.globalInstance()
    task = AsyncTask(qrunnable, pool)

    # Inject reporters
    task.on_started(event_reporter('started', task))
    task.on_error(event_reporter('error', task))
    task.on_finished(event_reporter('finished', task))

    return task


class AsyncSignals(QtCore.QObject):

    started = QtCore.Signal()
    finished = QtCore.Signal()
    result = QtCore.Signal(object)
    error = QtCore.Signal(object)
    wait = QtCore.QWaitCondition()
    wait_mutex = QtCore.QMutex()


class AsyncCallable(QtCore.QRunnable):
    '''Async function executor'''

    def __init__(self, fn, *args, **kwargs):
        super(AsyncCallable, self).__init__()
        self.signals = AsyncSignals()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.running = False
        self.finished = False
        self.result = None
        self.error = None

    def started(self):
        return self.running

    def stopped(self):
        return self.finished

    def stop_later(self):
        self.signals.result.disconnect()

    def stop(self):
        self.signals.result.disconnect()

    def wait(self):
        app = QtWidgets.QApplication.instance()
        if not self.finished:
            self.signals.wait_mutex.lock()
            while True:
                done = self.signals.wait.wait(self.signals.wait_mutex, 1)
                if done:
                    break
                else:
                    app.processEvents()
            self.signals.wait_mutex.unlock()

    def run(self):
        self.running = True
        self.signals.started.emit()
        try:
            self.result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            self.error = sys.exc_info()
            self.signals.error.emit(self.error)
        else:
            self.signals.result.emit(self.result)
        finally:
            self.running = False
            self.finished = True
            self.signals.wait.wakeAll()
            self.signals.finished.emit()


class AsyncIterator(QtCore.QRunnable):
    '''Consumes an iterator and emits each result yielded.'''

    def __init__(self, iterator):
        super(AsyncIterator, self).__init__()
        self.signals = AsyncSignals()
        self.iterator = iterator
        self.shutdown = False
        self.running = False
        self.finished = False
        self.result = None
        self.error = None

    def started(self):
        return self.running

    def stopped(self):
        return self.finished

    def stop_later(self):
        self.signals.result.disconnect()
        self.shutdown = True

    def stop(self):
        self.signals.result.disconnect()
        self.shutdown = True
        self.wait()

    def wait(self):
        app = QtWidgets.QApplication.instance()
        if not self.finished:
            self.signals.wait_mutex.lock()
            while True:
                done = self.signals.wait.wait(self.signals.wait_mutex, 1)
                if done:
                    break
                else:
                    app.processEvents()
            self.signals.wait_mutex.unlock()

    def run(self):
        self.running = True
        self.signals.started.emit()
        self.result = []
        while True:
            if self.shutdown:
                break
            try:
                result = next(self.iterator)
                self.result.append(result)
            except StopIteration:
                break
            except:
                self.error = sys.exc_info()
                self.signals.error.emit(self.error)
                break
            else:
                if self.shutdown:
                    break
                self.signals.result.emit(result)

        self.running = False
        self.finished = True
        self.signals.wait.wakeAll()
        self.signals.finished.emit()


class AsyncTask(object):

    def __init__(self, qrunnable, qthreadpool):
        self.qrunnable = qrunnable
        self.qthreadpool = qthreadpool

    def start(self):
        self.qthreadpool.start(self.qrunnable)

    def stop(self):
        self.qrunnable.stop()

    def stop_later(self):
        self.qrunnable.stop_later()

    def started(self):
        return self.qrunnable.started()

    def stopped(self):
        return self.qrunnable.stopped()

    def wait(self):
        self.qrunnable.wait()

    def on_result(self, callback):
        self.qrunnable.signals.result.connect(callback)

    def on_error(self, callback):
        self.qrunnable.signals.error.connect(callback)

    def on_started(self, callback):
        self.qrunnable.signals.started.connect(callback)

    def on_finished(self, callback):
        self.qrunnable.signals.finished.connect(callback)
