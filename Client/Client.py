from socket import AF_INET, SOCK_STREAM, socket, SHUT_RD
from socket import error as soc_err

import ClientUI
import logging
FORMAT='%(asctime)s (%(threadName)-2s) %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

class Client():

    def __init__(self):
        self.file = ""
        self.createUI()

    def connect(self,srv_addr):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.__s.connect(srv_addr)
            logging.info('Connected to MessageBoard server at %s:%d' % srv_addr)
            return True
        except soc_err as e:
            logging.error('Can not connect to MessageBoard server at %s:%d' \
                          ' %s ' % (srv_addr + (str(e),)))
        return False

    def createUI(self):
        self.ui = ClientUI.ClienUI(self)
        self.ui.run();

if __name__ == '__main__':
    c = Client()