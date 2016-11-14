from threading import Thread, Lock
from collections import defaultdict
from time import time

import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='%(asctime)s (%(threadName)-2s) %(message)s', )
LOG = logging.getLogger()

class TextFile(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.content = [("1","")]
        self.queue = defaultdict(lambda:defaultdict(lambda:defaultdict(str)))
        self.lock = Lock()

    def run(self):
        while 1:
            if not self.queue.keys():
                continue
            keys = self.queue.keys()
            for i in keys:
                self.checkEvents(i)
                if len(self.queue[i]) == 0:
                    self.queue.pop(i,None)



    def applyEvent(self,event,id):
        if self.queue[event][id]["modification"] == "ADD_LETTER":
            line = self.findLine(event)
            index = self.content.index(line)
            carIndex = int(self.queue[event][id]["index"])
            data = line[1][:carIndex] + self.queue[event][id]["char"] + line[1][carIndex:]
            self.content[index] = (event,data)
        elif self.queue[event][id]["modification"] == "REMOVE_LETTER":
            line = self.findLine(event)
            index = self.content.index(line)
            carIndex = self.queue[event][id]["index"]
            data = line[1][:carIndex-1]+ line[1][carIndex:]
            self.content[index] = (event,data)
        return

    def checkEvents(self,event):
        events = self.queue[event].keys()
        events.sort()
        for i in events:
            if self.queue[event][i]["Done"]:
                self.applyEvent(event,i)
                self.queue[event].pop(i,None)
                #MErge vms siin
            else:
                return


    def addLetter(self,data):
        with self.lock:
            parts = data.split(":")
            lineId = parts[0]
            reqtime = parts[1]
            index = parts[2]
            char = parts[3]
            self.queue[lineId][reqtime]["index"] = index
            self.queue[lineId][reqtime]["char"] = char
            self.queue[lineId][reqtime]["modification"] = "ADD_LETTER"
            self.queue[lineId][reqtime]["Done"] = True
            return

    def removeLetter(self,data):
        with self.lock:
            parts = data.split(":")
            lineId = parts[0]
            reqtime = parts[1]
            index = parts[2]
            self.queue[lineId][reqtime]["index"] = index
            self.queue[lineId][reqtime]["modification"] = "REMOVE_LETTER"
            self.queue[lineId][reqtime]["Done"] = True
            return

    def addLine(self, data):
        return

    def removeLine(self,data):
        return

    def requestModification(self,data):
        with self.lock:
            now = int(time())
            ID = data + ":" + str(now)
            line = self.findLine(data)
            self.queue[data][str(now)]["Done"] = False
            self.queue[data][str(now)]["before"] = line[1]

            return ID

    def findLine(self,id):
        for i in self.content:
            if i[0] == id:
                return i

    def getContent(self):
        with self.lock:
            data = ""
            for i in self.content:
                data += i[1]
            return data