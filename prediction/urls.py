from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name = 'index'),
    path('show_result/', views.show_result, name = 'show_result')
]
