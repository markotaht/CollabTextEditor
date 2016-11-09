from threading import Thread, Lock
import Queue
class TextFile(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.content = ""
        self.queue = Queue.Queue()

    def run(self):
        while 1:
            if self.queue.empty():
                continue
            #Handli evente

    def addLetter(self,data):
        return