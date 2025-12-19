from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('view/<str:post_id>/', views.view_post, name='view_post'),
    path('timeline/<int:number>/', views.timeline, name='timeline'),
    path('like/<str:post_id>/', views.like_post, name='like_post'),
    
    # Authenticated endpoints
    path('post/', views.create_post, name='create_post'),
    path('edit/<str:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<str:post_id>/', views.delete_post, name='delete_post'),
    
    # Authentication endpoints
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]