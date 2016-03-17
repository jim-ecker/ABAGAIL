__author__ = 'Jimmy'
import threading
import time

from FourPeaksRunner import FourPeaksRunner

threadLock = threading.Lock()
threads = []
class FourThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        threadLock.aquire()
        fourJob(self.package)
        threadLock.release()

def fourJob(package):
    threadLock.aquire()
    four = FourPeaksRunner()
    four.packageBuilder(package)
    four.four()
    threadLock.release()

