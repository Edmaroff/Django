from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer

class AdvertisementFilter(FilterSet):
    created_at = DateFromToRangeFilter()
    class Meta:
        model = Advertisement
        fields = ['created_at']

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['creator', 'status']
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []
