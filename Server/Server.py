from socket import AF_INET, SOCK_STREAM, socket, SHUT_WR
import ClientHandler, TextFile
import logging
logging.basicConfig(level=logging.DEBUG,\
                    format='%(asctime)s (%(threadName)-2s) %(message)s',)

class Server():

    def __init__(self):
        self.file = TextFile.TextFile()

    def listen(self,sock_addr,backlog=1):
        self.sock_addr = sock_addr
        self.backlog = backlog
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.sock_addr)
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
                c = ClientHandler(client_socket, client_addr,self.file)
                handlers.append(c)
                c.handle()
        except KeyboardInterrupt:
            logging.warn('Ctrl+C issued closing server ...')
        finally:
            if client_socket != None:
                client_socket.close()
            self.socket.close()
        map(lambda x: x.join(), handlers)

if __name__ == '__main__':
    logging.info( 'Application started' )
    server = Server()
    server.listen(('127.0.0.1',7777))
    server.loop()
    logging.info ( 'Terminating ...' )

