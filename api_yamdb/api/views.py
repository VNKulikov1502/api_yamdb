from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Category, Genre, Title
from rest_framework import filters, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from reviews.models import Comment, Review

from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


def get_update():
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_partial_update(self, request):
    instance = self.get_object()
    serializer = self.get_serializer(
        instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')  # Добавьте order_by
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return get_update()

    def update(self, request, *args, **kwargs):
        return get_update()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')  # Добавьте order_by
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return get_update()

    def update(self, request, *args, **kwargs):
        return get_update()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return (
            Title.objects
            .annotate(rating=Avg('reviews__score'))
            .order_by('id')
        )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer

    def update(self, request, *args, **kwargs):
        return get_update()

    def partial_update(self, request, *args, **kwargs):
        return get_partial_update(self, request)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title__id=title_id).order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)

        if Review.objects.filter(
            title=title,
            author=self.request.user
        ).exists():
            raise ValidationError('You have already reviewed this title.')

        serializer.save(title=title, author=self.request.user)

    def update(self, request, *args, **kwargs):
        return get_update()

    def partial_update(self, request, *args, **kwargs):
        return get_partial_update(self, request)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review__id=review_id).order_by('id')

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)

    def update(self, request, *args, **kwargs):
        return get_update()

    def partial_update(self, request, *args, **kwargs):
        return get_partial_update(self, request)
