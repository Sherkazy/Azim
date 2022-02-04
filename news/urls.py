from django.urls import path, include
from rest_framework.routers import DefaultRouter

from news.views import NewsViewSet, CheckView

router = DefaultRouter()
router.register('news', NewsViewSet),
urlpatterns = [
    path('check/', CheckView.as_view()),
]

urlpatterns += router.urls
