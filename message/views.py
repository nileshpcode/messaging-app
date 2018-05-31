# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.views.generic import ListView, CreateView
from django.views import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from push_notifications.models import GCMDevice
from message.models import Message


# Create your views here.

class UserView(ListView):
    template_name = 'users.html'
    queryset = User.objects.all()

    def get_queryset(self):
        qs = super(UserView, self).get_queryset()
        return qs.exclude(pk=self.request.user.pk)


class MessageView(CreateView):
    template_name = 'chatting.html'
    model = Message
    fields = ['message', 'sender', 'receiver']

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        reciever_id = self.kwargs.pop('user_id')
        context['reciever'] = reciever = self.get_reciever(reciever_id)
        context['sender'] = sender = self.get_sender()
        context['messages'] = Message.objects.filter(
            Q(receiver=reciever, sender=sender) | Q(sender=reciever, receiver=sender))
        return context

    def get_reciever(self, reciever_id):
        return User.objects.get(pk=reciever_id)

    def get_sender(self):
        return User.objects.get(pk=self.request.user.id)

    def post(self, request, *args, **kwargs):
        msg = self.request.POST.get('message')
        reciever_id = self.request.POST.get('reciever_id')
        sender_id = self.request.POST.get('sender_id')
        Message.objects.create(message=msg, sender_id=sender_id, receiver_id=reciever_id)

        return HttpResponseRedirect(reverse_lazy('chat', args=(reciever_id,)))

    # def form_valid(self, form):
    #     print form.cleaned_data
    #     message = form.cleaned_data['message']
    #     # Message.objects.create()


class TokenCreateView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TokenCreateView, self).dispatch(request)

    def post(self, request, *args, **kwargs):
        device_id = request.POST.get('device_id')
        GCMDevice.objects.get_or_create(registration_id=device_id, cloud_message_type="FCM")
        return HttpResponse('success')
