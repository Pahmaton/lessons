from django.urls import path

from . import views

app_name="voice"
urlpatterns = [
    path('', views.speech, name='speech'),
    path('recognize/', views.recognize, name='recognize'),
]