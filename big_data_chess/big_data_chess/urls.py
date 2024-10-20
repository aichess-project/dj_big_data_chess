"""big_data_chess URL Configuration

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
from django.urls import path
from chess.views import check_new_lichess_file_view, decom_file, get_next_db_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/check-new-lichess-file/', check_new_lichess_file_view, name='check_new_lichess_file'),
    path('api/decom-lichess-file/', decom_file, name='decom_file'),
    # New APIs
    path('api/get_next_db/', get_next_db_view, name='get_next_db_view'),
]
