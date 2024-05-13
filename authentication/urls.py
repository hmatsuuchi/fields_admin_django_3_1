from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('logout/', views.LogoutView.as_view(), name='logout'),
     path('csrf/refresh/', views.CsrfRefreshView.as_view(), name='csrf_refresh'),
]