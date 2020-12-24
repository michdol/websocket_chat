import logging

from autobahn.twisted.websocket import (
    WebSocketServerFactory,
    WebSocketServerProtocol,
    listenWS
)
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File


"""
Message format:
{
    "username": "string",
    "message": "string",
}
"""

class BroadcastServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onConnect(self, request):
        logging.debug("BroadcastServerProtocol.onConnect <request>:\n\n{}\n\ntype: {}\n".format(request, type(request)))
        logging.info("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = payload.decode("utf-8")
            logging.debug("BroadcastServerProtocol.onMessage <msg>:\n\n{}\n".format(msg))
            self.factory.broadcast(msg)

    def connectionLost(self, reason):
        logging.debug("BroadcastServerProtocol.connectionLost <reason>:\n\n{}\n".format(reason))
        super().connectionLost(reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        super().__init__(url)
        self.clients = []

    def register(self, client):
        logging.debug("BroadcastServerFactory.register <client>:\n\n{}\n\ntype: {}\n".format(client, type(client)))
        if client not in self.clients:
            logging.info("Registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        logging.debug("BroadcastServerFactory.unregister <client>:\n\n{}\n".format(client))
        self.clients.remove(client)

    def broadcast(self, message):
        logging.info("Broadcasting message: {}".format(message))
        encoded_message = message.encode("utf-8")
        for client in self.clients:
            client.sendMessage(encoded_message)


if __name__ == '__main__':
    format_ = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(format=format_, level=logging.DEBUG, datefmt="%H:%M:%S")

    factory = BroadcastServerFactory("ws://0.0.0.0:9000")
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    webdir = File(".")
    web = Site(webdir)
    reactor.listenTCP(80, web)
    reactor.run()

