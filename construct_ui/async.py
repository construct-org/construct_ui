# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import inspect
import sys
import time
import traceback
from Qt import QtCore, QtWidgets


POOL = None


def get_pool():
    global POOL
    if not POOL:
        POOL = AsyncPool()
    return POOL


def submit(fn, *args, **kwargs):

    pool = get_pool()
    return pool.submit(fn, *args, **kwargs)


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
            else:
                if self.shutdown:
                    break
                self.signals.result.emit(result)

        self.running = False
        self.finished = True
        self.signals.wait.wakeAll()
        self.signals.finished.emit()


class AsyncPool(QtCore.QThreadPool):

    def submit(self, task, *args, **kwargs):
        if inspect.isgeneratorfunction(task):
            qrunnable = AsyncIterator(task(*args, **kwargs))
        elif hasattr(task, '__iter__'):
            if args or kwargs:
                qrunnable = AsyncIterator(task(*args, **kwargs))
            else:
                qrunnable = AsyncIterator(task)
        elif callable(task):
            qrunnable = AsyncCallable(task, *args, **kwargs)
        else:
            raise TypeError('Unsupport type: %s %s' % (task, type(task)))
        return AsyncTask(qrunnable, self)


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


if __name__ == '__main__':
    import fsfs
    from Qt import QtWidgets

    def long_running_task(n):
        for i in xrange(n):
            time.sleep(1)
            yield i

    def print_results(value):
        print('Task result: ' + str(value))

    def print_finished():
        print('Task finished.')
        sys.exit()

    app = QtWidgets.QApplication([])

    task = async_task(
        fsfs.search(root='Z:/Active_Projects', depth=2, levels=4).tags('asset')
    )
    task.on_result(print_results)
    task.on_finished(print_finished)
    task.start()
    task.wait()

    timer = QtCore.QTimer.singleShot(1000, task.stop)

    sys.exit(app.exec_())
