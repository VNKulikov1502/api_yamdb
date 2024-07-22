from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from posts.models import Category, Genre, Title
from rest_framework import filters, status, viewsets
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


def get_title_id(self):
    return self.kwargs.get('title_id')


def get_review_id(self):
    return self.kwargs.get('review_id')


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


class CategoryGenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering = ['id']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return get_update()

    def update(self, request, *args, **kwargs):
        return get_update()


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['name', 'slug']
    search_fields = ['name']


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    ordering_fields = ['name', 'slug']
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    ordering = ['name']
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return (
            Title.objects
            .annotate(rating=Avg('reviews__score'))
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
        title_id = get_title_id(self)
        return Review.objects.filter(title__id=title_id).order_by('id')

    def perform_create(self, serializer):
        title_id = get_title_id(self)
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        title_id = get_title_id(self)
        context['title'] = get_object_or_404(Title, id=title_id)
        return context

    def update(self, request, *args, **kwargs):
        return get_update()

    def partial_update(self, request, *args, **kwargs):
        return get_partial_update(self, request)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = get_review_id(self)
        return Comment.objects.filter(review__id=review_id).order_by('id')

    def perform_create(self, serializer):
        review_id = get_review_id(self)
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)

    def update(self, request, *args, **kwargs):
        return get_update()

    def partial_update(self, request, *args, **kwargs):
        return get_partial_update(self, request)
