from django.urls import path

from .views import IndexPageView, FormControlView


urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('form/control', FormControlView.as_view(), name='form-control'),
    path('form/layout', FormControlView.as_view(), name='form-layout'),
]
