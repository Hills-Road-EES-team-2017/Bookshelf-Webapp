from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
#from website.consumers import WSConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # standard path() or url() entries to consumer classes
        # path('ws/', WSConsumer)
        ]),
    ),

})
