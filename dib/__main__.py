from .bot import factory
import sys


from twisted.internet import reactor
startLogging(sys.stdout)
reactor.listenTCP(8080, factory)
reactor.run()

