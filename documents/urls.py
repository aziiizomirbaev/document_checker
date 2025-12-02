from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document-list'),
    path('create/', views.document_create, name='document-create'),
    path('<int:pk>/', views.document_detail, name='document-detail'),
    path('<int:pk>/add-version/', views.version_create, name='document-add-version'),
    path('dashboard/data/', views.dashboard_data, name='dashboard-data'),
]