
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from posts.models import Category, Genre, Title
from rest_framework import serializers
from reviews.models import Comment, Review
from .constants import MAX_NAME_LENGTH


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(
        many=True,
        read_only=True,
        allow_empty=False,
        allow_null=False
    )
    category = CategorySerializer(
        read_only=True
    )
    rating = serializers.FloatField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)])
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, data):
        request = self.context.get('request')
        title = self.context.get('title')
        if request and request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise serializers.ValidationError(
                    'You have already reviewed this title.'
                )
        return data

    def create(self, validated_data):
        review = Review.objects.create(
            **validated_data
        )
        return review

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
