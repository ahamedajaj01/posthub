from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),  
    path('register/',views.register,name='register'),
    path('login_view/',views.login_view,name='login_view'),
    path('create_post/',views.create_post,name='create_post'),
    path('view_post/',views.view_post,name='view_post'),  #logged in user post page
    path('logout/', views.logout_view, name='logout_view'),
    path('explore_post/', views.explore_post, name='explore_post'),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post')
] 