from django.urls import path
from . import views

urlpatterns = [
    path('<username>/update/', views.profile_update, name = 'profile_update'),
    path('<username>/', views.profile_view, name = 'view_profile'),
]

