# -*- coding: utf-8 -*-
from __future__ import absolute_import
import threading
from Qt import QtCore


class QuerySignals(QtCore.QObject):

    result = QtCore.Signal(object)


class AsyncQuery(threading.Thread):

    def __init__(self, query):
        super(AsyncQuery, self).__init__()
        self.daemon = True
        self.query = query
        self._shutdown = threading.Event()
        self._stopped = threading.Event()
        self._started = threading.Event()

        self._signals = QuerySignals()
        self.result = self._signals.result

    def started(self):
        return self._started.is_set()

    def stopped(self):
        return self._stopped.is_set()

    def running(self):
        return self.started and not self.stopped

    def shutdown(self):
        return self._shutdown.is_set()

    def stop(self):
        self._shutdown.set()
        self._stopped.wait()
        if self.isAlive():
            self.join()

    def run(self):
        self._started.set()
        try:
            while True:
                if self._shutdown.is_set():
                    break
                try:
                    entry = next(self.query)
                except StopIteration:
                    break
                else:
                    self.result.emit(entry)
        finally:
            self._stopped.set()
