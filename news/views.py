from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from news.models import News
from user.permissions import *
from news.filter import NewsFilter
from news.serializers import NewsSerializer


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ('title', 'text')
    filterset_class = NewsFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsProducer, ]

        return super(self.__class__, self).get_permissions()


class CheckView(ListAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    permission_classes = [IsProducer]
