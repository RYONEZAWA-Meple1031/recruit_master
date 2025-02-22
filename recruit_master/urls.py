"""recruit_master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recruit_flow import views  # recruit_flow アプリの views をインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # 認証URLの追加

    path('', views.applicant_list, name='applicant_list'),
    path('applicant/<int:pk>/', views.applicant_detail, name='applicant_detail'),
    path('applicant/new/', views.applicant_create, name='applicant_create'),
    path('applicant/<int:pk>/edit/', views.applicant_edit, name='applicant_edit'),
    path('applicant/<int:pk>/delete/', views.applicant_delete, name='applicant_delete'),
    path('applicant/graph/', views.applicant_graph, name='applicant_graph'), 
]
