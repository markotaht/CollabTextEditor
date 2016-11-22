from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from Commons import DEFAULT_PORT, MSG_FIELD_SEP, serialize
import ClientHandler, TextFile
import logging
logging.basicConfig(level=logging.DEBUG,\
                    format='%(asctime)s (%(threadName)-2s) %(message)s',)

class Server(Thread):

    def __init__(self, filename):
        Thread.__init__(self)
        self.setName("SERVER")
        self.file = TextFile.TextFile()
        self.file.openfile(filename)
        self.file.start()
        self.clientHandlers = []
        self.running = True
        self.server_addr = ("0.0.0.0", DEFAULT_PORT)

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

    def close(self):
        self.running = False

    def loop(self):
        logging.info( 'Server loop started' )
        handlers = []
        try:
            while self.running:
                client_socket = None
                logging.info('Awaiting new clients ...')
                #Server jaab siia kinni kui sulgeda. Kuidagi on vaja siit edais saada kui peaks sulgema...
                client_socket, client_addr = self.socket.accept()
                logging.info("Client joined from %s:%s"%client_addr)
                c = ClientHandler.ClientHandler(self, client_socket, client_addr,self.file)
                self.clientHandlers.append(c)
                handlers.append(c)
                c.handle()
        except KeyboardInterrupt:
            logging.warn('Ctrl+C issued closing server ...')
        finally:
            logging.info("Shutting down server...")
            if client_socket != None:
                client_socket.close()
            self.socket.close()
            map(lambda x: x.disconnect(), handlers)
            self.file.end()
            self.file.join()
        logging.info("Server loop ended")

if __name__ == '__main__':
    logging.info( 'Application started' )
    server = Server()
    server.start()
    server.join()
    logging.info ( 'Terminating ...' )
