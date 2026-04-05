from django.urls import path

from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_list, name='list'),
    path('nouveau/', views.staff_create, name='create'),
    path('<int:pk>/modifier/', views.staff_edit, name='edit'),
    path('<int:pk>/supprimer/', views.staff_delete, name='delete'),
]
