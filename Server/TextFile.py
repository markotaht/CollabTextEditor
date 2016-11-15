from threading import Thread, Lock
from collections import defaultdict
from time import time

import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='%(asctime)s (%(threadName)-2s) %(message)s', )
LOG = logging.getLogger()

#TODO voimalik et vaja parandada threadide syncimist
class TextFile(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.content = ""
        self.queue = defaultdict(lambda:defaultdict(str))
        self.lock = Lock()

    def run(self):
        while 1:
            if not self.queue.keys():
                continue
            self.checkEvents()


    def applyEvent(self,id):
        if self.queue[id]["modification"] == "ADD_LETTER":
            carIndex = int(self.queue[id]["index"])
            self.content = self.content[:carIndex] + self.queue[id]["char"] + self.content[carIndex:]
        elif self.queue[id]["modification"] == "REMOVE_LETTER":
            carIndex = int(self.queue[id]["index"])
            self.content = self.content[:carIndex]+ self.content[carIndex+1:]
        return

    def checkEvents(self):
        events = self.queue.keys()
        events.sort()
        for i in events:
            if self.queue[i]["Done"]:
                self.applyEvent(i)
                self.queue.pop(i,None)
                #MErge vms siin
            else:
                if time() - int(i) >= 1000:
                    self.queue.pop(i,None)
                return


    def addLetter(self,data):
        with self.lock:
            parts = data.split(":")
            ID = parts[0]
            index = parts[1]
            char = parts[2]
            self.queue[ID]["index"] = index
            self.queue[ID]["char"] = char
            self.queue[ID]["modification"] = "ADD_LETTER"
            self.queue[ID]["Done"] = True
            return

    def removeLetter(self,data):
        with self.lock:
            parts = data.split(":")
            ID = parts[0]
            index = parts[1]
            self.queue[ID]["index"] = index
            self.queue[ID]["modification"] = "REMOVE_LETTER"
            self.queue[ID]["Done"] = True
            return

    def requestModification(self,data):
        with self.lock:
            now = int(time())
            ID = str(now)
            self.queue[ID]["Done"] = False
            self.queue[ID]["before"] = self.content

            return ID

    def getChanges(self):
        return self.content

    def getContent(self):
        with self.lock:
            data = ""
            for i in self.content:
                data += i[1]
            return data