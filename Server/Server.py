from socket import AF_INET, SOCK_STREAM, socket, gethostname
from threading import Thread
import ClientHandler, TextFile
import logging
logging.basicConfig(level=logging.DEBUG,\
                    format='%(asctime)s (%(threadName)-2s) %(message)s',)

class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.file = TextFile.TextFile()
        self.file.openfile("Demo")
        self.file.start()
        self.server_addr = ("0.0.0.0", 7777)

    def run(self):
        logging.info('Application started')
        self.listen(self.server_addr)
        self.loop()
        logging.info('Terminating ...')

    def listen(self,sock_addr,backlog=1):
        self.server_addr = sock_addr
        self.backlog = backlog
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.server_addr)
        self.socket.listen(self.backlog)
        logging.debug( 'Socket %s:%d is in listening state'\
                       '' % self.socket.getsockname())


    def loop(self):
        logging.info( 'Falling to serving loop, press Ctrl+C to terminate ...' )
        handlers = []
        try:
            while 1:
                client_socket = None
                logging.info('Awaiting new clients ...')
                client_socket, client_addr = self.socket.accept()
                logging.info("Client joined from %s:%s"%client_addr)
                c = ClientHandler.ClientHandler(client_socket, client_addr,self.file)
                handlers.append(c)
                c.handle()
        except KeyboardInterrupt:
            logging.warn('Ctrl+C issued closing server ...')
        finally:
            if client_socket != None:
                client_socket.close()
            self.socket.close()
            map(lambda x: x.join(), handlers)
            self.file.end()
            self.file.join()

if __name__ == '__main__':
    logging.info( 'Application started' )
    server = Server()
    server.listen((gethostname(),7777))
    server.loop()
    logging.info ( 'Terminating ...' )
