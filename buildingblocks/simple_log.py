from datetime import datetime as d
import os


class SimpleLog(object):
    ts = d.now().strftime('%Y-%m-%d-%H-%M-%S')

    def __init__(self, path='./', name='debug.log'):
        if self._file is None:
            if not os.path.isdir(path):
                os.mkdir(path)
            self._file = open('{0}\\{1}_{2}'.format(path.rstrip('\\'), SimpleLog.ts, name), 'w')

    def __del__(self):
        self.close()

    def info(self, str):
        stamp = d.now().strftime('%Y-%m-%d-%H-%M-%S')
        fmt_str = '[Info] [%s] %s\n' % (stamp, str)
        self._file.write(fmt_str)
        self._file.flush()
        print (fmt_str)

    def error(self, str):
        stamp = d.now().strftime('%Y-%m-%d-%H-%M-%S')
        fmt_str = '[Error] [%s] %s\n' % (stamp, str)
        self._file.write(fmt_str)
        self._file.flush()
        print (fmt_str)

    def close(self):
        if not(self._file is None):
            self._file.close()

