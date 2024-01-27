from django.urls import path
from . import views


urlpatterns = [
    #path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('', views.case_list, name='case_list'),  # URL for listing cases
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),  # URL for case details
    path('create/case', views.create_case, name='create_case'),  # URL for creating cases
    path('search/', views.search_cases, name='search_cases'),

    # Add other URL patterns for your views here
]

