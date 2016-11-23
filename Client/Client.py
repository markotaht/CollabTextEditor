from socket import AF_INET, SOCK_STREAM, socket, SHUT_RD
from socket import error as soc_err
from threading import Thread, Lock
from Queue import Queue
import ClientUI
from Commons import *
import time
import Tkinter

from Server.Server import Server

import logging
FORMAT='%(asctime)s (%(threadName)-2s) %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

class Client():

    def __init__(self):
        self.lock = Lock()
        self.file = ""
        self.socket = None
        self.server = None
        self.createUI()
        #TESTIB Tahe saatmist ja eemaldamist.
    #    self.connect(('192.168.56.1',7777))
   #     self.sendLetter("a",0)
    #    print self.removeLetter(0)

    def connect(self,srv_addr,name,password):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect(srv_addr)
            logging.info('Connected to ConcurrentEditing server at %s:%d' % srv_addr)
            content = self.sendIntroduction(name,password)
            rsp, filename = content.split(":")
            if rsp == RSP_INTRODUCTION_NOTOK:
                self.socket.close()
                return False
            return deserialize(filename)
        except soc_err as e:
            logging.error('Can not connect to the server at %s:%d' \
                          ' %s ' % (srv_addr + (str(e),)))
        except ValueError as e:
            logging.error("Need more than 1 value to unpack rsp, filename")
        return False

    def sendIntroduction(self,name,password):
        data = name + ":" + password
        data = serialize(data)
        req = INTRODUCTION+MSG_FIELD_SEP+data
        return self.send(req)

    def processLocalChange(self, textField, oldVersion, newVersion, changeType, changeIndex, changeChar):
        print(oldVersion + " -> " + newVersion)
        print(changeType + "" + changeChar + " at " + str(changeIndex))

        if changeType == "+":
            self.sendLetter(changeChar, changeIndex)
        elif changeType == "-":
            self.removeLetter(changeIndex)


    def sendLetter(self, letter):
        logging.info("Sending letter: " + letter)
        data = serialize(letter)
        req = REQ_SEND_LETTER + MSG_FIELD_SEP + data
        return self.send(req)

    def removeLetter(self):
        req = REQ_REMOVE_LETTER + MSG_FIELD_SEP
        return self.send(req)

    def moveCaret(self,movement):
        data = serialize(str(movement))
        req = REQ_MOVE_CARET + MSG_FIELD_SEP + data
        return self.send(req)

    def _synchronise(self,args):

        #Synchronization
        req = REQ_SYNCHRONIZE + MSG_FIELD_SEP
        data = self.send(req)
        content = deserialize(data[3:])
        try:
            content,caret,online = content.split(":")
        except:
            self.socket.close()
            self.socket = None
            return "CLOSE","",""

        return content,int(caret),online

    def addCollaborator(self,name,password):
        self.server.file.addCollaborator(name,password)

    def getCollaborators(self):
        return self.server.file.getCollaborators()

    def removeCollaborator(self, name):
        self.server.file.removeCollaborator(name)

    def editCollaborator(self, oldname, newname, pw):
        self.server.file.editCollaborator(oldname, newname, pw)

    def openLocally(self, filename):
        #run server
        self.server = Server(filename)
        self.server.start()
        time.sleep(0.01)
        self.connect(("127.0.0.1", 7777),"me","admin")
        logging.info("Connected to server.")

    def closeServer(self):
        self.server.close()
        self.connect(("127.0.0.1", 7777), "sulgeja", "DIE")

    def send(self,msg):
        m = msg + MSG_SEP
        with self.lock:
            r = False
            try:
                self.socket.sendall(m)
                r = self._receive()
            except KeyboardInterrupt:
                self.socket.close()
                logging.info('Ctrl + C issued, terminating...')
            except soc_err as e:
                if e.errno == 107:
                    logging.warn('Server closed connection, terminating ...')
                else:
                    logging.error('Connection error: %s' % str(e))
                self.socket.close()
                logging.info('Disconnected')
            return r

    def _receive(self):
        message, bits = '', ''
        try:
            bits = self.socket.recv(DEFAULT_RCV_BUFSIZE)
            message += bits
            while len(bits) > 0 and not (bits.endswith(MSG_SEP)):
                bits = self.socket.recv(DEFAULT_RCV_BUFSIZE)
                message += bits
            if len(bits) <= 0:
                self.socket.close()
                message = ''
            message = message[:-1]
        except KeyboardInterrupt:
            self.socket.close()
            message = ''
            return 0
        except soc_err as e:
            if e.errno == 107:
            #    logging.warn('Client %s:%d left before server could handle it' \
            #             '' % self.client_addr)
                message = ""
            else:
                logging.error('Error: %s' % str(e))
            self.socket.close()
            message = ''
            return 0
        return message

    def close(self):
        if not self.socket == None:
            self.socket.shutdown(SHUT_RD)
            self.socket.close()
            self.socket = None

    def createUI(self):
        self.ui = ClientUI.ClientUI(self)
        self.ui.start();

if __name__ == '__main__':
    c = Client()