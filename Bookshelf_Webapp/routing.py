from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
#from website.consumers import WSConsumer

application = ProtocolTypeRouter({

})
