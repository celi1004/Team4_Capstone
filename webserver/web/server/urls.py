# from django.urls import path, include
from django.urls import path
# from rest_framework.routers import DefaultRouter
from . import views
#from server import views

# router = DefaultRouter()
# router.register('', views.ServerViewSet)

urlpatterns = [
    path('', views.ServerList.as_view()),
    #path('show/', views.ServerShow.as_view()),
]