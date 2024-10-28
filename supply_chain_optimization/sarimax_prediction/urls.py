from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/<str:filename>/', views.show_file, name='show_file'),
    path('use_model/', views.use_model, name='use_model'),
    path('view_plots/', views.view_plots, name='view_plots'),
    path('delete_plots/', views.delete_plots, name='delete_plots'),
    path('is_model_done/', views.is_model_done, name='is_model_done'),
    path('download_plots/', views.download_plots, name='download_plots'),
    path('download_csv/', views.download_csv, name='download_csv'),
]
