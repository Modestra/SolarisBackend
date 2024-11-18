from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

class CreateListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """Оставить методы только создания и просмотра большой группы объектов"""
    pass

class ListViewSet(GenericViewSet, mixins.ListModelMixin):
    """Методы только для просмотра большой группы объектов"""
    pass