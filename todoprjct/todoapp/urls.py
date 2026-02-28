from django.urls import path
from . import views
urlpatterns = [
    path('' , views.home , name= 'homepage'),
    path('register/' , views.register , name='register'),
    path('login/' , views.login_view , name='login'),
    path('delete/<str:name>' , views.delete_task , name='delete'),
    path('update/<str:name>' , views.update_task , name='update')

]