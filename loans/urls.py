from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin, name='admin'),
    path('admin/edit/<int:id>/', views.edit_loan, name='edit_loan'),
    path('admin/delete/<int:id>/', views.delete_loan, name='delete_loan'),
]
