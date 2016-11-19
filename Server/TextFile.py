from threading import Thread, Lock
from collections import defaultdict
from time import time

import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='%(asctime)s (%(threadName)-2s) %(message)s', )
LOG = logging.getLogger()

from settings import PROJECT_ROOT
FILES_DIR = PROJECT_ROOT + "/Files"

import os.path
#TODO voimalik et vaja parandada threadide syncimist
class TextFile(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setName("SERVER-FILE")
        self.content = ""
        self.collaborators = defaultdict(str)
        self.queue = defaultdict(lambda:defaultdict(str))
        self.done = False
        self.lock = Lock()
        self.idCounter = 0;

    def openfile(self, name):
        if os.path.isfile(name + "_content.txt"):
            file = open(name+"_content.txt")
            self.content = file.read()
            file.close()
            collabs = open(name+"_collaborators.txt")
            for line in collabs:
                parts = line.strip().split(":")
                self.collaborators[parts[0]] = parts[1]
            file.close()
        self.name = name
        self.collaborators["me"] = "admin"

    def savefile(self):
        file = open(self.name + "_content.txt","w")
        file.write(self.content)
        file.close()

        collabs = open(self.name+"_collaborators.txt")
        for k,v in self.collaborators.iteritems():
            collabs.write(k+":"+v+"\n")
        collabs.close()

    def addCollaborator(self,name,password):
        self.collaborators[name] = password

    def checkCollaborator(self,name,password):
        if name in self.collaborators and self.collaborators[name] == password:
            LOG.info(name + " joined the server")
            return True
        return False

    def end(self):
        self.done = True

    def run(self):
        while 1:
            if not self.queue.keys():
                if self.done:
                    break
                continue
            self.checkEvents()
        self.savefile()


    def applyEvent(self,id):
        if self.queue[id]["modification"] == "ADD_LETTER":
            LOG.info("Adding a letter")
            carIndex = int(self.queue[id]["index"])
            self.content = self.content[:carIndex] + self.queue[id]["char"] + self.content[carIndex:]
        elif self.queue[id]["modification"] == "REMOVE_LETTER":
            carIndex = int(self.queue[id]["index"])
            LOG.info("Removing a letter")
            self.content = self.content[:carIndex]+ self.content[carIndex+1:]
        return

    def checkEvents(self):
        events = self.queue.keys()
        events.sort()
        for i in events:
            if self.queue[i]["done"]:
                self.applyEvent(i)
                self.queue.pop(i,None)
                #Merge vms siin
            else:
                if time() - int(self.queue[i]["time"]) >= 1000:
                    self.queue.pop(i,None)
                return


    def addLetter(self,data):
        with self.lock:
            parts = data.split(":")
            ID = parts[0]
            index = parts[1]
            char = parts[2]
            if not ID in self.queue:
                return False
            self.queue[ID]["index"] = index
            self.queue[ID]["char"] = char
            self.queue[ID]["modification"] = "ADD_LETTER"
            self.queue[ID]["done"] = True
            return True

    def removeLetter(self,data):
        with self.lock:
            parts = data.split(":")
            ID = parts[0]
            index = parts[1]
            if not ID in self.queue:
                return False
            self.queue[ID]["index"] = index
            self.queue[ID]["modification"] = "REMOVE_LETTER"
            self.queue[ID]["done"] = True
            return True

    def requestModification(self):
        with self.lock:
            ID = "ID" + str(self.idCounter)
            self.idCounter += 1
            self.queue[ID]["done"] = False
            self.queue[ID]["before"] = self.content
            self.queue[ID]["time"] = str(int(time()))
            return ID

    def getChanges(self):
        return self.content

    def getContent(self):
        with self.lock:
            data = ""
            for i in self.content:
                data += i[1]
            return data