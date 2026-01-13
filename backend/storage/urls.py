from django.urls import path
from . import views

urlpatterns = [
    path('presigned-url/', views.generate_presigned_url, name='presigned-url'),
    path('presigned-urls/', views.generate_presigned_urls_batch, name='presigned-urls-batch'),
    path('folder/check/', views.check_folder_exists, name='check-folder'),
    path('folder/create/', views.create_folder, name='create-folder'),
    path('files/', views.list_files, name='list-files'),
]
