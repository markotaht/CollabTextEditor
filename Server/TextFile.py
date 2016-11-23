from threading import Thread, Lock
from collections import defaultdict
from time import time

import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='%(asctime)s (%(threadName)-2s) %(message)s', )
LOG = logging.getLogger()

from settings import PROJECT_ROOT
FILES_DIR = PROJECT_ROOT + "/Files/"

import os.path
#TODO voimalik et vaja parandada threadide syncimist
class TextFile(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setName("SERVER-FILE")
        self.content = ""
        self.collaborators = defaultdict(str)
        self.carets = defaultdict(int)
        self.queue = defaultdict(lambda:defaultdict(str))
        self.running = True
        self.lock = Lock()
        self.idCounter = 0
        self.connectedcollaborators = [""] #TODO remove if offline also

    def openfile(self, name):
        if os.path.isfile(FILES_DIR + name + "_content.txt"):
            file = open(FILES_DIR + name+"_content.txt")
            self.content = file.read()
            file.close()
        if os.path.isfile(FILES_DIR + name + "_content.txt"):
            collabs = open(FILES_DIR + name+"_collaborators.txt")
            for line in collabs:
                parts = line.strip().split(":")
                self.collaborators[parts[0]] = parts[1]
            file.close()
        self.name = name
        self.collaborators["admin"] = "admin"

    def removeOnline(self,name):
        self.connectedcollaborators.remove(name)
        LOG.info("%s went offline" % name)

    def savefile(self):
        file = open(FILES_DIR + self.name + "_content.txt","w")
        file.write(self.content)
        file.close()

        collabs = open(FILES_DIR + self.name+"_collaborators.txt", "w")
        for k,v in self.collaborators.iteritems():
            collabs.write(k+":"+v+"\n")
        collabs.close()

    def addCollaborator(self,name,password):
        with self.lock:
            self.collaborators[name] = password
            self.savefile()

    def checkCollaborator(self,name,password):
        with self.lock:
            if name in self.collaborators and self.collaborators[name] == password:
                LOG.info(name + " joined the server")
                self.carets["name"] = 0
                return True
            return False

    def getCollaborators(self):
        return self.collaborators

    def removeCollaborator(self, name):
        with self.lock:
            self.collaborators.pop(name)

    def editCollaborator(self, oldname, newname, password):
        with self.lock:
            self.collaborators.pop(oldname)
        self.addCollaborator(newname, password)

    def end(self):
        self.running = False

    def run(self):
        while self.running:
            if not self.queue.keys():
                continue
            self.checkEvents()
            self.savefile()
        self.savefile()

    def move_caret(self,name, index, movement):
        for i in self.carets:
            if i == name:
                self.carets[i] += movement
            elif self.carets[i] >= index:
                self.carets[i] += movement
            if self.carets[i] <= 0:
                self.carets[i] = 0
            if self.carets[i] > len(self.content):
                self.carets[i] = len(self.content)-1

    def applyEvent(self,id):
        if self.queue[id]["modification"] == "ADD_LETTER":
            LOG.info("Adding a letter")
            carIndex = self.carets[self.queue[id]["name"]]
            self.content = self.content[:carIndex] + self.queue[id]["char"] + self.content[carIndex:]
            self.move_caret(self.queue[id]["name"],carIndex,1)
        elif self.queue[id]["modification"] == "REMOVE_LETTER":
            carIndex =  self.carets[self.queue[id]["name"]]
            LOG.info("Removing a letter")
            self.content = self.content[:carIndex-1]+ self.content[carIndex:]
            self.move_caret(self.queue[id]["name"], carIndex, -1)
        return

    def checkEvents(self):
        events = self.queue.keys()
        events.sort()
        for i in events:
            self.applyEvent(i)
            self.queue.pop(i,None)


    def addLetter(self,data,name):
        ID = "ID" + str(self.idCounter)
        self.idCounter += 1
        self.queue[ID]["char"] = data
        self.queue[ID]["modification"] = "ADD_LETTER"
        self.queue[ID]["name"] = name
        return True

    def removeLetter(self,name):
        ID = "ID" + str(self.idCounter)
        self.idCounter += 1
        self.queue[ID]["modification"] = "REMOVE_LETTER"
        self.queue[ID]["name"] = name
        return True

    def moveCaret(self,name,movement):
        print name
        print self.carets[name]
        with self.lock:
            if self.carets[name] <= len(self.content) and self.carets[name] >= 0:
                self.carets[name] += movement
                if self.carets[name] < 0:
                    self.carets[name] = 0
                if self.carets[name] > len(self.content):
                    self.carets[name] = len(self.content)
        print self.carets[name]

    def getContent(self,name):
        return self.content, self.carets[name], ",".join(self.connectedcollaborators)