"""IIC-IEM – Gallery URLs"""
from django.urls import path
from . import views
app_name = 'gallery'
urlpatterns = [
    path('', views.gallery_list, name='list'),
    path('<int:pk>/', views.album_detail, name='album_detail'),
    path('admin-panel/gallery/', views.admin_gallery_list, name='admin_list'),
    path('admin-panel/gallery/albums/add/', views.admin_album_add, name='admin_album_add'),
    path('admin-panel/gallery/albums/<int:pk>/edit/', views.admin_album_edit, name='admin_album_edit'),
    path('admin-panel/gallery/albums/<int:pk>/delete/', views.admin_album_delete, name='admin_album_delete'),
    path('admin-panel/gallery/albums/<int:pk>/upload/', views.admin_image_upload, name='admin_image_upload'),
    path('admin-panel/gallery/images/<int:img_pk>/delete/', views.admin_image_delete, name='admin_image_delete'),
]
