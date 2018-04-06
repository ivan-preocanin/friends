from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [
    path('api/', views.PersonList.as_view()),
    path('', views.IndexView.as_view(), name='index'),
    path('load_data/', views.load_data, name='load_data'),
    path('<pk>/', views.DetailView.as_view(), name='detail'),
]