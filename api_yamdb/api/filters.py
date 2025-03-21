from django_filters import rest_framework as filters
from posts.models import Title


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
