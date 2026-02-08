# workosders/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('workorders.api.urls')),
]
