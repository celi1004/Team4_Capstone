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
from .crawling import naverlogin


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
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            diction = json.loads(serializer.data)
            crawling.naverlogin.naverStart(diction["title"], diction["body"])
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # json = JSONRenderer().render(serializer.data)
            # json

    # def get(self, request, format=None):
    #     queryset = Server.object.all()
    #     serializer = ServerSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)