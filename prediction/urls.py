from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name = 'index'),
    path('show_result/', views.show_result, name = 'show_result'),
    path('show_result_of_database/', views.show_result_of_database, name = 'show_result_of_database')
]
