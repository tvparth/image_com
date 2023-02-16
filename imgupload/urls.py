from django.urls import path
from imgupload import views
from .views import admin_login, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',admin_login,name='login'),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(next_page = 'login'), name="logout"),
    path('',views.img_compresser,name='image_compress'),
    path('',views.photo_list,name='photo_list'),
    path('user/<int:id>/',views.update_user,name='upd'),
    path('del/<int:id>/',views.delete_user,name='del'),
    
    
    
    
]