from socket import AF_INET, SOCK_STREAM, socket, SHUT_RD
from socket import error as soc_err
from threading import Thread, Lock

import ClientUI
from Commons import *

import logging
FORMAT='%(asctime)s (%(threadName)-2s) %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

class Client():

    def __init__(self):
        self.lock = Lock()
        self.file = ""
        self.createUI()
        self.loop()

    def connect(self,srv_addr):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect(srv_addr)
            logging.info('Connected to MessageBoard server at %s:%d' % srv_addr)
            return True
        except soc_err as e:
            logging.error('Can not connect to MessageBoard server at %s:%d' \
                          ' %s ' % (srv_addr + (str(e),)))
        return False

    def sendLetter(self,letter):
        data = serialize(letter)
        #Lisda positsioon
        req = REQ_SEND_LETTER + MSG_FIELD_SEP + data
        return self.send(req)

    def addNewLine(self,lineId):
        data = serialize(lineId)
        req = REQ_ADD_NEW_LINE + MSG_FIELD_SEP + data
        return self.send(req)

    def addRemoveLine(self, lineId):
        data = serialize(lineId)
        req = REQ_REMOVE_LINE + MSG_FIELD_SEP + data
        return self.send(req)

    def addMoveCaret(self, lineId,index,subsStart,subsEnd):
        data = serialize([lineId,index,subsStart,subsEnd])
        req = REQ_MOVE_CARET + MSG_FIELD_SEP + data
        return self.send(req)

    def send(self,msg):
        m = msg + MSG_SEP
        with self.lock:
            r = False
            try:
                self.socket.sendall(m)
                r = True
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

    def receive(self, msg):
        logging.info("Received %d bytes in total"%len(msg))
        if len(msg) < 2:
            logging.debug("Not enough data")
            return
        if msg.startswith(RSP_SEND_LETTER_OK + MSG_FIELD_SEP):
            self.on_LetterSent()
        elif msg.startswith(RSP_ADD_NEW_LINE_OK + MSG_FIELD_SEP):
            self.on_NewLineAdded()
        elif msg.startswith(RSP_REMOVE_LINE_OK + MSG_FIELD_SEP):
            self.on_Lineemoved()
        elif msg.startswith(RSP_MOVE_CARET_OK + MSG_FIELD_SEP):
            self.on_CaretMoved()
        else:
            #UNKONW CONTROL CODE
            return 0


    def set_onLetterSentCallback(self, func):
        self.on_LetterSent = func

    def set_onNewLineAddedCallback(self,func):
        self.on_NewLineAdded = func

    def set_onLineeMovedCallback(self,func):
        self.on_Lineemoved = func

    def set_onCaretMovedCallback(self,func):
        self.on_CaretMoved = func

    def close(self):
        self.socket.shutdown(SHUT_RD)
        self.socket.close()

    def createUI(self):
        self.ui = ClientUI.ClienUI(self)
        self.ui.run();

    def loop(self):
        func = Thread(target=self._loop).start()
        func.join()

    def _loop(self):
        logging.info("Receiver loop...")
        while 1:
            if self.receive() == 0:
                break;

if __name__ == '__main__':
    c = Client()