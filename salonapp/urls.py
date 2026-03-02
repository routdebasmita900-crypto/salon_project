from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('appointments/',views.appointment_list,name='appointment_list'),
    path('delete/<int:id>/', views.delete_appointment, name='delete'),
    path('update-status/<int:id>/<str:status>/', views.update_status, name='update_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete/<int:id>/',views.mark_completed,name='mark_completed'),
    path('cancel/<int:id>/', views.mark_cancelled, name='mark_cancelled'),
    path('complete/<int:id>/', views.complete_appointment, name='complete_appointment'),
    path('cancel/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
]