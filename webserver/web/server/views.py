# from rest_framework import viewsets
# from .models import Server
# from .serializer import ServerSerializer
#from django.http import HttpResponse, JsonResponse
import json

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Server
from .serializer import ServerSerializer
from . import naverlogin

import time

# from rest_framework.renderers import JSONRenderer

# CBV
# class ServerViewSet(viewsets.ModelViewSet):
#      queryset = Server.objects.all()
#      serializer_class = ServerSerializer

#     def show(request):
#         queryset = Server.objects

#         for sets in queryset.all():
#             ti = sets.title
#             bo = sets.body

#         return JsonResponse({
#             'title' : ti,
#             'body' : bo,
#         }, json_dumps_params = {'ensure_ascii':True})



class ServerList(APIView):
    def post(self, request, format=None):

        # for key, value in request.data.items():
        #     print(type(key), type(value))
        s = Server.objects.all()
        s.delete()

        start = time.time()
        return_data = naverlogin.naverStart(request.data['category'] , request.data['keyword'], request.data['number'])
        print(time.time() - start)
        
        for key, value in return_data.items():
            ser = Server()
            ser.number = key
            ser.newTitle = value
            ser.save()
            # Server(number=key, newTitle=value)
            # print(type(key), type(value))
            # print(key, value)
        
        # servers = Server.objects

        # print(return_data)
        # print(type(return_data))
        
        # serializer = ServerSerializer(data=return_data)

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

        # print(serializer)
        # print(type(serializer))

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer = ServerSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return_data = naverlogin.naverStart(request.data['category'] , request.data['keyword'], request.data['number'])
        #     # print(type(serializer.data))
        #     # diction = json.loads(request.data)
        #     # naverlogin.naverStart(request.data['title'], request.data['body'])
        #     # naverlogin.naverStart(1,2)
        #     # print(request.data['title'])
        #     # naverlogin.naverStart(request.data["title"],request.data["body"])
        #     # print(type(return_data))
        #     serializer = ServerSerializer(data=return_data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # json = JSONRenderer().render(serializer.data)
            # json

    # def get(self, request, format=None):
    #     queryset = Server.object.all()
    #     serializer = ServerSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)