from django.urls import path

from .views import FormControlView, IndexPageView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("form/control", FormControlView.as_view(), name="form-control"),
    path("form/layout", FormControlView.as_view(), name="form-layout"),
]
