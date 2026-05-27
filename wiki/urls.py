from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('sections/create/', views.section_create, name='section_create'),
    path('sections/<slug:slug>/', views.section_detail, name='section_detail'),
    path('pages/create/', views.page_create, name='page_create'),
    path('pages/<slug:slug>/', views.page_detail, name='page_detail'),
    path('pages/<slug:slug>/edit/', views.page_edit, name='page_edit'),
    path('pages/<slug:slug>/delete/', views.page_delete, name='page_delete'),
    path('pages/<slug:slug>/history/', views.page_history, name='page_history'),
]
