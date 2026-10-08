from django.urls import path
from .views import (
    CompanyListCreateView,
    CategoryListCreateView,
    JobListCreateView,
    JobDetailView,
    ApplicationListCreateView,
    ApplicationDetailView,
)

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),

    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    path('applications/', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
]