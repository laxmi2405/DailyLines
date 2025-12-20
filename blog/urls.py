from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_post, name='add_post'),
    path('post/<int:id>/', views.post_details, name='post_details'),
    path('category/<int:category_id>/', views.category_filter, name='category_filter'),
    path('post/<int:id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('myposts/', views.my_posts, name='my_posts'),
    path('post/<int:id>/like/', views.toggle_like, name='toggle_like'),

]
