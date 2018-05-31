from django.conf.urls import url

from message.views import UserView, MessageView, TokenCreateView

urlpatterns = [
    url(r'^$', UserView.as_view(), name='messages'),
    url(r'^chat/(?P<user_id>\d+)/$', MessageView.as_view(), name='chat'),
    url(r'^token/create/$', TokenCreateView.as_view(), name='token-create')
]
