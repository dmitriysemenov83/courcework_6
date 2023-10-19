from django.urls import path

from blogpost.apps import BlogpostConfig
from blogpost.views import BlogpostListView, BlogpostDetailView

app_name = BlogpostConfig.name


urlpatterns = [
    path('', BlogpostListView.as_view(), name='blogpost_list'),
    path('view/<int:pk>', BlogpostDetailView.as_view(), name='view'),
]