from socket import AF_INET, SOCK_STREAM, socket, SHUT_WR
from socket import error as soc_err

from Commons import *
import logging

logging.basicConfig(level=logging.DEBUG, \
                    format='%(asctime)s (%(threadName)-2s) %(message)s', )
LOG = logging.getLogger()
from threading import Thread, Lock


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
            #sendUpdates

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
        action,data = self.handlePackage(message)
        if action == REQ_MODIFICATION:
            id = self.file.requestModification(data)
            return RSP_MODIFICATION_OK + MSG_FIELD_SEP + id
        elif action == REQ_REMOVE_LETTER:
            self.file.removeLetter(data)
            return RSP_REMOVE_LETTER_OK
        elif action == REQ_SEND_LETTER:
            self.file.addLetter(data)
            return RSP_SEND_LETTER_OK
        elif action == REQ_ADD_NEW_LINE:
            self.file.addLine(data)
            return RSP_ADD_NEW_LINE_OK
        elif action == REQ_REMOVE_LINE:
            self.file.removeLine(data)
            return RSP_REMOVE_LINE_OK
        elif action == REQ_SYNCHRONIZE:
            changes = self.file.getChanges()
            data = ":".join(map(lambda x: serialize(x[0] + ":-:" + x[1]), changes))
            data = serialize(data)
            return RSP_SYNCHRONIZE_OK + MSG_FIELD_SEP + data
        else:
            #Migi viga
            return 0

    def handlePackage(self,package):
        blocks = package.split(MSG_FIELD_SEP)
        data = decodestring(blocks[1])
        return blocks[0],data

    def send(self,response):
        m = response + MSG_SEP
        with self.lock:
            r = False
            try:
                self.client_socket.sendall(m)
                r = True
            except KeyboardInterrupt:
                self.client_socket.close()
                LOG.info('Ctrl+C issued, disconnecting client %s:%d' \
                         '' % self.client_addr)
            except soc_err as e:
                if e.errno == 107:
                    LOG.warn('Client %s:%d left before server could handle it' \
                             '' % self.client_addr)
                else:
                    LOG.error('Error: %s' % str(e))
                self.client_socket.close()
                LOG.info('Client %s:%d disconnected' % self.client_addr)
            return r

