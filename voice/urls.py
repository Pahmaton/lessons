from django.urls import path

from . import views

app_name="voice"
urlpatterns = [
    path('', views.speech, name='speech'),
    path('recognize/', views.recognize, name='recognize'),
    path('my_files/', views.my_files, name='my_files'),
    path('my_files/<int:file_id>', views.del_files, name='del_files'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('my_files/<int:file_id>/info', views.files_info, name='files_info'),
    path('my_files/<int:file_id>/rename', views.files_rename, name='files_rename'),
]