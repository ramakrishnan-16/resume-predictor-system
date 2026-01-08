from django.contrib import admin
from django.urls import path
from .views import ResumePredictView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/predict/", ResumePredictView.as_view(), name="predict"),
]