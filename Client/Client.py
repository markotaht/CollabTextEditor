from socket import AF_INET, SOCK_STREAM, socket, SHUT_RD
from socket import error as soc_err
from threading import Thread, Lock
from Queue import Queue
import ClientUI
from Commons import *

import logging
FORMAT='%(asctime)s (%(threadName)-2s) %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

class Client():

    def __init__(self):
        self.lock = Lock()
        self.file = ""
        self.socket = None
        self.queue = Queue()
        self.queue.put((self._synchronise,[]))
        self.createUI()
        self.loop()
        #TESTIB Tahe saatmist ja eemaldamist.
        self.connect(('127.0.0.1',7777))
        self.sendLetter("a",0)
    #    print self.removeLetter(0)

    def connect(self,srv_addr):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect(srv_addr)
            logging.info('Connected to ConcurrentEditing server at %s:%d' % srv_addr)
            return True
        except soc_err as e:
            logging.error('Can not connect to MessageBoard server at %s:%d' \
                          ' %s ' % (srv_addr + (str(e),)))
        return False

    def requestModification(self):
        req = REQ_MODIFICATION + MSG_FIELD_SEP
        rsp = self.send(req)
        return rsp[rsp.find(":")+1:]

    def sendLetter(self, letter, index):
        logging.info("Sending letter: " + letter + " index " + str(index))
        args = [letter,index]
        self.queue.put((self._sendLetter, args))

    def _sendLetter(self,args):
        ID = self.requestModification()
        logging.info("Change letter changeID: " + ID)
        data = ID + ":" + str(args[1]) + ":" +args[0]
        data = serialize(data)
        req = REQ_SEND_LETTER + MSG_FIELD_SEP + data
        return self.send(req)

    def removeLetter(self, index):
        logging.info("Remove letter from index: " + str(index))
        args = [index]
        self.queue.put((self._removeLetter, args))

    def _removeLetter(self,args):
        ID = self.requestModification()
        data = serialize(ID +":"+str(args[0]))
        req = REQ_REMOVE_LETTER + MSG_FIELD_SEP + data
        return self.send(req)

    def _synchronise(self,args):

        #Syncimne
        req = REQ_SYNCHRONIZE + MSG_FIELD_SEP
        data = self.send(req)
        content = deserialize(data[2:])
        self.queue.put((self._synchronise, []))

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
        self.queue.put(None)

    def createUI(self):
        self.ui = ClientUI.ClienUI(self)
        self.ui.start();

    def loop(self):
        func = Thread(target=self._loop, args=(self,))
        func.start()
        return func

    def _loop(self, parent):
        logging.info("Receiver loop...")
        while not parent.queue.empty():
            event = parent.queue.get()
            try:
                if event == None:
                    break
                event[0](event[1])
            except soc_err:
                break

if __name__ == '__main__':
    c = Client()

    t = c.loop()

    t.join()