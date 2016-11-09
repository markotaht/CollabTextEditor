from socket import AF_INET, SOCK_STREAM, socket, SHUT_WR
from socket import error as soc_err
from base64 import decodestring, encodestring

import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='%(asctime)s (%(threadName)-2s) %(message)s', )
LOG = logging.getLogger()
from threading import Thread, Lock
MSG_SEP = ';'
DEFAULT_RCV_BUFSIZE = 1024


MSG_SEP = ";"
REQ_SEND_LETTER = "l"
MSG_FIELD_SEP = ":"

def serialize(msg):
    return encodestring(msg)

def deserialize(msg):
    return decodestring(msg)

class ClientHandler(Thread):
    def __init__(self, client_socket, client_addr, file):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.file = file
        self.lock = Lock()

    def run(self):
        while 1:
            m = self.receive()
            if len(m) <= 0:
                break
            rsp = self.protocol(m)
            if not self.send(rsp):
                break

    def handle(self):
        self.start()

    def receive(self):
        message, bits = '', ''
        try:
            bits = self.client_socket.recv(DEFAULT_RCV_BUFSIZE)
            message += bits
            while len(bits) > 0 and not (bits.endswith(MSG_SEP)):
                bits = self.client_socket.recv(DEFAULT_RCV_BUFSIZE)
                message += bits
            if len(bits) <= 0:
                self.client_socket.close()
                LOG.info('Client %s:%d disconnected' % self.client_addr)
                message = ''
            message = message[:-1]
        except KeyboardInterrupt:
            self.client_socket.close()
            LOG.info('Ctrl+C issued, disconnecting client %s:%d' % self.client_addr)
            message = ''
        except soc_err as e:
            if e.errno == 107:
                LOG.warn('Client %s:%d left before server could handle it' \
                         '' % self.client_addr)
            else:
                LOG.error('Error: %s' % str(e))
            self.client_socket.close()
            LOG.info('Client %s:%d disconnected' % self.client_addr)
            message = ''
        return message

    def protocol(self, message):
        if message.startswith(REQ_SEND_LETTER + MSG_FIELD_SEP):
            blocks = message.split(MSG_FIELD_SEP)
            data = decodestring(blocks[1])
            self.file.addLetter(data)
        #Kirjuta protocol
        return 4

    def send(self,response):
        m = response + MSG_SEP
        with self.lock:
            r = False
            try:
                self.client_s.sendall(m)
                r = True
            except KeyboardInterrupt:
                self.client_s.close()
                LOG.info('Ctrl+C issued, disconnecting client %s:%d' \
                         '' % self.client_addr)
            except soc_err as e:
                if e.errno == 107:
                    LOG.warn('Client %s:%d left before server could handle it' \
                             '' % self.client_addr)
                else:
                    LOG.error('Error: %s' % str(e))
                self.client_s.close()
                LOG.info('Client %s:%d disconnected' % self.client_addr)
            return r

