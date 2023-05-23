from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'cloud'

urlpatterns = [
    path('', views.cloud_home, name='cloud_home'),
    path('save_project/', views.save_project, name='save_project'),
    
    path('delete_server/', views.delete_server, name='delete_server'),
    
    path('create-server', views.create_server, name='create-server'),
    path('clone_vm', views.clone_vm, name='clone_vm'),
    path('wait' , views.wait , name='wait'),
    path('my_form_view', views.my_form_view, name='my_form_view'),
    path('deneme' , views.deneme , name='deneme'),
    path('project-view/<int:project_id>', views.view_server, name='project-view'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)