from socket import AF_INET, SOCK_STREAM, socket, SHUT_RD
from socket import error as soc_err
from threading import Lock
from base64 import decodestring, encodestring

import ClientUI
import logging
FORMAT='%(asctime)s (%(threadName)-2s) %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

MSG_SEP = ";"
REQ_SEND_LETTER = "l"
RSP_SEND_LETTER_OK = "1"
MSG_FIELD_SEP = ":"

def serialize(msg):
    return encodestring(msg)

def deserialize(msg):
    return decodestring(msg)

class Client():

    def __init__(self):
        self.lock = Lock()
        self.file = ""
        self.createUI()

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
        req = REQ_SEND_LETTER + MSG_FIELD_SEP + data
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

        else:
            #UNKONW CONTROL CODE
            return 0

    def on_LetterSent(self):
        #Do something
        return

    def close(self):
        self.socket.shutdown(SHUT_RD)
        self.socket.close()

    def createUI(self):
        self.ui = ClientUI.ClienUI(self)
        self.ui.run();

if __name__ == '__main__':
    c = Client()