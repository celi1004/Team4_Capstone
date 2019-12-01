import json

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Server
from .serializer import ServerSerializer
from . import naverlogin

import time

class ServerList(APIView):
    def post(self, request, format=None):
        s = Server.objects.all()
        s.delete()

        # print(request.data['category'])
        # print(request.data['keyword'])
        # print(request.data['crawlingData'])

        #start = time.time()
        return_data = naverlogin.naverStart(request.data['category'] , request.data['keyword'], request.data['crawlingData'])
        #print(time.time() - start)


        for key, value in return_data.items():
            ser = Server()
            ser.number = key
            ser.newTitle = value
            ser.save()

        # queryset = {}
        # for ser in Server.objects.all():
        #     queryset[ser.number] = ser.newTitle
        # print(queryset)
        # serializer = ServerSerializer(data=queryset, many=True)

        queryset = []
        for key, value in return_data.items():
            queryset.append(Server(number=key, newTitle=value))
        serializer = ServerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)